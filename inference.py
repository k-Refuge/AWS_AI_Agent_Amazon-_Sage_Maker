# inference.py
import os
import json
import re
import boto3
import requests

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import BedrockEmbeddings
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain.agents import initialize_agent, Tool
from langchain.llms.bedrock import Bedrock

# -------------------------------
# AWS Configuration 
# -------------------------------
AWS_REGION = "us-east-1"
bedrock_runtime = boto3.client("bedrock-runtime", region_name=AWS_REGION)
S3_BUCKET = "sagemaker-us-east-1-745039059599"
S3_PREFIX = "faiss_index/"
LOCAL_FAISS_FOLDER = "/tmp/faiss_index"
os.makedirs(LOCAL_FAISS_FOLDER, exist_ok=True)

# -------------------------------
# LLM Settings
# -------------------------------
model_parameters = {
    "temperature": 0.0,
    "top_p": 0.5,
    "top_k": 200,
    "max_tokens": 800,
}

llm = Bedrock(
    model_id="mistral.mistral-small-2402-v1:0",
    model_kwargs=model_parameters,
    client=bedrock_runtime
)

# -------------------------------
# Download FAISS from S3
# -------------------------------
s3 = boto3.client("s3", region_name=AWS_REGION)
for obj in s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=S3_PREFIX).get("Contents", []):
    file_name = obj["Key"].split("/")[-1]
    s3.download_file(S3_BUCKET, obj["Key"], os.path.join(LOCAL_FAISS_FOLDER, file_name))
    print(f"Téléchargé : {file_name}")

# -------------------------------
# Embeddings & VectorStore
# -------------------------------
bedrock_embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v2:0",
    client=bedrock_runtime
)

vectorstore_faiss = FAISS.load_local(
    LOCAL_FAISS_FOLDER,
    embeddings=bedrock_embeddings,
    allow_dangerous_deserialization=True
)
retriever = vectorstore_faiss.as_retriever(search_kwargs={"k": 3})

# -------------------------------
# RAG Configuration 
# -------------------------------
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
rag_chat = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory
)

# -------------------------------
# NER Prompt 
# -------------------------------
ner_prompt = """[INST]
Analyse la situation juridique décrite par l'utilisateur et extrais les éléments nécessaires pour une analyse de cas et une recherche documentaire.

### Instructions :
- Retourne uniquement un objet JSON entre les balises <attributes></attributes>.
- Réponds en français.

### Extrais les attributs pertinents : 
- domaine_du_droit : string
- type_de_probleme : string
- statut_de_l_utilisateur : string
- partie_adverse : string
- date_evenement : ISO date (si connue)
- montants : objet {{"montant": nombre, "devise": string}}
- mots_cles : liste de courtes chaînes
- juridiction_potentielle : string

### Exemple d'entrée :
{customer_input}

### Réponse :
[/INST]
"""

# -------------------------------
# Official web search function
# -------------------------------
def search_serper(query):
    SERPER_API_KEY = "YOUR_SERPER_API_KEY"
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
    payload = {"q": query + " site:legifrance.gouv.fr OR site:service-public.fr OR site:travail-emploi.gouv.fr"}
    res = requests.post(url, headers=headers, json=payload)
    if res.status_code != 200:
        return f"Erreur lors de la recherche : {res.text}"
    data = res.json()
    links = [r["link"] for r in data.get("organic", [])[:3]]
    return "\n".join(links) if links else "Aucun lien officiel trouvé."

# -------------------------------
# Function for the agent
# -------------------------------
def ask_agent(question, agent, ner_prompt=ner_prompt, llm=llm):
    """
    Envoie la question à l’agent et récupère la réponse.
    """
    # Extraction NER
    entity_json = llm(ner_prompt.format(customer_input=question)).strip()
    result = re.search('<attributes>(.*)</attributes>', entity_json, re.DOTALL)
    attributes = json.loads(result.group(1)) if result else {}

    # Build the enriched query
    query = f"""
Domaine du droit : {attributes.get('domaine_du_droit', '')}
Type de problème : {attributes.get('type_de_probleme', '')}
Statut : {attributes.get('statut_de_l_utilisateur', '')}
Question : {question}
"""
    response = agent.run(query)
    return response

# -------------------------------
# Initialize the agent with the tools
# -------------------------------
tools = [
    Tool(
        name="Recherche juridique locale",
        func=lambda q: rag_chat.run(q),
        description="Utilise la base locale (Code du travail, lois) pour répondre aux questions juridiques."
    ),
    Tool(
        name="Recherche web officielle",
        func=search_serper,
        description="Recherche des liens officiels (Legifrance, Service-Public) liés à la question."
    )
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type="zero-shot-react-description",
    memory=memory,
    verbose=True
)

# -------------------------------
# Functions for SageMaker
# -------------------------------
def model_fn(model_dir):
    """
    Called by SageMaker to load the model.
    """
    return agent

def predict_fn(input_data, model):
    """
    Called for each inference request.
    """
    question = input_data.get("question", "")
    result = ask_agent(question, model)
    return {"response": result}

def input_fn(request_body, request_content_type):
    """
    Convert the HTTP request into a Python dictionary.
    """
    if request_content_type == "application/json":
        return json.loads(request_body)
    return {"question": request_body}

def output_fn(prediction, response_content_type):
    """
    Convert the Python response into JSON.
    """
    return json.dumps(prediction)

