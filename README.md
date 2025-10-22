# AWS_AI_Agent_Amazon-_Sage_Maker
# LexiAgent — AI Agent for administrative information - AWS_AI_Agent_Hackathon_LexiAgent
### AWS AI Agent Hackathon 2025  

 **Delivering accurate, quick and context-aware answers & informations to legal and administrative questions through AI.**

---

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![AWS](https://img.shields.io/badge/AWS-Bedrock-orange)
![LangChain](https://img.shields.io/badge/LangChain-0.2+-green)
![Status](https://img.shields.io/badge/Project-Hackathon%202025-beta)

---

## Overview

**LexiAgent** is an intelligent **LLM-based legal agent** designed for the **AWS AI Agent Hackathon 2025**.  
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
git clone https://github.com/yourusername/lexibot-aws-agent.git](https://github.com/k-Refuge/AWS_AI_Agent_Amazon-_Sage_Maker.git
cd AWS_AI_Agent_Amazon-_Sage_Maker
```
## 2. Create an IAM account on AWS
## 3.
## 4. Set your Serper API key
```python
def search_serper(query):
    SERPER_API_KEY = "your_API_key"  # meke sure to put your key here
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
```
## 5. Run

---
## Contribution
We’re open to all contributions and ideas! 🙌

You can help by for example:
- Suggesting better LLMs or embeddings models
- Expanding the legal corpus
- Translating the system into other languages
- Improving performance or UX

Submit a Pull Request or open an Issue to share your ideas.



