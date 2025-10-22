# inference.py
import json
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.llms.bedrock import Bedrock
from langchain.embeddings import BedrockEmbeddings
from langchain.vectorstores import FAISS

# --- AWS Configuration and Models ---
import boto3

bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")

llm = Bedrock(
    model_id="mistral.mistral-small-2402-v1:0",
    client=bedrock_runtime,
    model_kwargs={
        "temperature": 0.0,
        "top_p": 0.5,
        "max_tokens": 400
    }
)

bedrock_embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v2:0",
    client=bedrock_runtime
)

# --- Load your FAISS vector index (created in your notebook)---
vectorstore_faiss = FAISS.load_local("/opt/ml/model/faiss_index", bedrock_embeddings)

retriever = vectorstore_faiss.as_retriever(search_kwargs={"k": 3})
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

rag_chat = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory
)

# --- The main function called by SageMaker ---
def predict_fn(input_data, model=None):
    """Executed on every API request"""
    question = input_data["question"]
    response = rag_chat.run(question)
    return {"answer": response}

def input_fn(request_body, content_type):
    """Converts the HTTP request into JSON"""
    return json.loads(request_body)

def output_fn(prediction, accept):
    """Return the HTTP response"""
    return json.dumps(prediction)


