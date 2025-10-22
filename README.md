
# ZK_Agent — AI Agent for administrative information
### AWS AI Agent Hackathon 2025  

 **Delivering accurate, quick and context-aware answers & informations to legal and administrative questions through an AI agent.**

---

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-orange)
![AWS SageMaker](https://img.shields.io/badge/AWS-SageMaker-ff69b4)  
![AWS S3](https://img.shields.io/badge/AWS-S3-purple) 
![LangChain](https://img.shields.io/badge/LangChain-0.2+-green)
![LLM](https://img.shields.io/badge/LLM-Mistral%20Small-lightblue)
![Agent](https://img.shields.io/badge/Agent-Yes-yellow)


---

## Overview

**ZK_Agent** is an intelligent **LLM-based legal agent** designed for the **AWS AI Agent Hackathon 2025**, that decides to search for information either on official documentation or official websites.  
It helps users — especially foreigners or citizens unfamiliar with a certain country bureaucracy (France as example in our project) — get **clear, accurate, and context-aware answers** to legal and administrative questions such as:

- Residency permits and visa procedures  
- Work contracts and labor law (CERFA forms, rights and obligations)  
- Interactions with public services (Service-Public, Légifrance, etc.)

---

## The Problem

Finding reliable information about administrative or legal procedures in a new country (France as example in our project) can be **confusing, time-consuming, and fragmented**.  

Even official websites can be difficult to navigate — especially for non-native speakers or people unfamiliar with the country legal jargon.

>  “How can I renew my residency permit in Cergy?”  
>  “Is my employer allowed to terminate my contract during trial period?”  
>  “Which court handles housing disputes?”

These are **real, complex questions** that users ask every day — and our agent is here to answer them, **clearly and accurately**.

---

##  Our Goal

To **democratize access to legal and administrative information** by combining:
- **Language understanding (LLMs)**  
- **Document retrieval** from official sources (Légifrance, Service-Public, Travail-Emploi)  
- **Reasoning and contextual memory**

We aim to **deliver accurate, contextualized, and referenced answers** — bridging the gap between **raw data** and **actionable knowledge**.

##  Inspiration

This project was inspired by our **own experiences as foreign students in France**, navigating complex procedures such as residency permits, labor law, and administrative rights.  

We realized how difficult it is to find **reliable information tailored to one’s personal situation**, so we built a system that does exactly that — and could scale to **other countries** facing similar challenges.

---

##  Architecture Diagram


---

## ⚙️ Tech Stack

| Layer | Technology | Description |
|-------|-------------|-------------|
| **Agent Layer** | 🤖 [LangChain Agent](https://python.langchain.com/docs/modules/agents/) (Zero-Shot ReAct) | Core reasoning component that decides which tool to call (RAG or web search) |
| **LLM** | 🧠 [Mistral Small](https://aws.amazon.com/bedrock/) (via Amazon Bedrock) | Generates and understands text |
| **Embeddings** | 🔢 [Amazon Titan Embeddings](https://aws.amazon.com/bedrock/titan/) | Converts legal documents into vector representations |
| **Vector Store** | 🧮 [FAISS](https://github.com/facebookresearch/faiss) | Enables semantic similarity search |
| **Framework** | 🔗 [LangChain](https://www.langchain.com/) | Orchestrates the RAG pipeline and agent tools |
| **Data Source** | 📄 PDFs stored in [AWS S3](https://aws.amazon.com/s3/) | Legal texts (Code du travail, circulaires, etc.) |
| **Execution Environment** | 🧪 [Amazon SageMaker](https://aws.amazon.com/sagemaker/) | Runs and manages the AI agent securely |
| **Web Search** | 🌐 [Serper API](https://serper.dev/) | Fetches official references (Légifrance, Service-Public) |
| **Memory** | 🧩 `ConversationBufferMemory` | Maintains chat context and continuity |
| **Environment** | ☁️ [AWS Bedrock Runtime](https://aws.amazon.com/bedrock/) | Executes LLM inference securely |
| **Language** | 🇫🇷 French (extendable to multilingual) | Focused on French administrative/legal use cases |
| **Dev Tools** | 🐍 Python 3.10+, [Boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html) | Core development environment |


--- 
## Get Started 
### 1. Clone repository
```bash
git clone https://github.com/k-Refuge/ZK_Agent-AWS_AI_Agent_Hackathon.git
cd ZK_Agent-AWS_AI_Agent_Hackathon
```
## 2.  Environment Setup

This project is designed to run in Amazon SageMaker Studio.
You can also run it locally if your environment has valid AWS credentials (with permissions to access S3 and Bedrock).

## 3. Data Configuration

The project uses data stored in an S3 bucket specific to our AWS account.
Before running the notebooks or scripts, update any S3 paths in the code to point to your own S3 bucket.

We used the file **"LEGITEXT000006072050.pdf"** for the demonstration. You can access it in the data folder.
You can easily expand your dataset by downloading additional code files from:
https://www.legifrance.gouv.fr/liste/codeetatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF

### 4. Using the Vector Store

You can run inference.py or reference.py directly without regenerating the embeddings —
just make sure to upload the pre-built FAISS vector store (index.faiss and index.pkl) to your S3 bucket,
and update the corresponding S3 path variables in the scripts.



## 5. Set your Serper API key 
The agent integrates a web search feature using the Serper API.
To enable it, open the file inference.py, locate the function search_serper, and replace the placeholder key with your own:
```python
def search_serper(query):
    SERPER_API_KEY = "your_API_key"  # create one and add it here
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
```
You can create your free API key on https://serper.dev
or you can use the function :   os.getenv()

### 6. Deployment

To deploy your model to SageMaker, run:
```python
python deployement.py
```

If successful, the terminal will display the name of your deployed endpoint.
You can also verify its status in the AWS SageMaker Console → Endpoints section.

---
## Contribution
We’re open to all contributions and ideas! 🙌

You can help for example by:
- Suggesting better LLMs or embeddings models
- Expanding the legal corpus
- Deployment approach
- Any remarks/feeedback about our work are welcome

Submit a Pull Request or open an Issue to share your ideas.

## What still doesn't work correctly
**InvokEndpoint Error** 
We attempted to deploy our model using SageMaker and received a successful output in the terminal. However, when we try to call the endpoint, we encounter a runtime error, as shown below:
<img width="1231" height="157" alt="image" src="https://github.com/user-attachments/assets/f61d9b6a-48b4-4f63-a70b-9d9beec7f47c" />
Please refer to our error file for detailed explanations. We would greatly appreciate your guidance and contribution on this issue.



