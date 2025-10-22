# AWS_AI_Agent_Amazon-_Sage_Maker
# 🇫🇷 LexiBot — AI Legal Assistant for France  
### AWS AI Agent Hackathon 2025  

> 💡 **Empowering access to legal and administrative information through AI.**

---

## 🧠 Overview

**LexiBot** is an intelligent **LLM-based legal assistant** designed for the **AWS AI Agent Hackathon 2025**.  
It helps users — especially foreigners or citizens unfamiliar with French bureaucracy — get **clear, accurate, and context-aware answers** to legal and administrative questions such as:

- Residency permits and visa procedures  
- Work contracts and labor law (CERFA forms, rights and obligations)  
- Interactions with public services (Service-Public, Légifrance, etc.)

---

## 🚨 The Problem

Finding reliable information about administrative or legal procedures in France can be **confusing, time-consuming, and fragmented**.  

Even official websites can be difficult to navigate — especially for non-native speakers or people unfamiliar with French legal jargon.

> ❓ “How can I renew my residency permit in Cergy?”  
> ❓ “Is my employer allowed to terminate my contract during trial period?”  
> ❓ “Which court handles housing disputes?”

These are **real, complex questions** that users ask every day — and our agent is here to answer them, **clearly and accurately**.

---

## 🎯 Our Goal

To **democratize access to legal and administrative information** by combining:
- **Language understanding (LLMs)**  
- **Document retrieval** from official sources (Légifrance, Service-Public, Travail-Emploi)  
- **Reasoning and contextual memory**

We aim to **deliver accurate, contextualized, and referenced answers** — bridging the gap between **raw data** and **actionable knowledge**.

---

## 🌍 Inspiration

This project was inspired by our **own experiences as foreign residents in France**, navigating complex procedures such as residency permits, labor law, and administrative rights.  

We realized how difficult it is to find **reliable information tailored to one’s personal situation**, so we built a system that does exactly that — and could scale to **other countries** facing similar challenges.

---

## 🏗️ Architecture Diagram

```text
                          ┌───────────────────────────────┐
                          │           User Query           │
                          │  (in French, e.g. legal issue) │
                          └───────────────────────────────┘
                                        │
                                        ▼
                ┌────────────────────────────────────────────┐
                │  Entity Extraction (NER) via Mistral LLM   │
                │  → Extracts: domain, user status, problem  │
                └────────────────────────────────────────────┘
                                        │
                                        ▼
             ┌──────────────────────────────────────────────┐
             │   LangChain Agent (AWS Bedrock + Tools)      │
             │   • Chooses best source dynamically          │
             │   ├─ Local RAG (PDF laws from S3)            │
             │   └─ Web Search (Serper API on official sites)│
             └──────────────────────────────────────────────┘
                                        │
                                        ▼
             ┌──────────────────────────────────────────────┐
             │   Vector Store (FAISS + Amazon Titan Embeds) │
             │   • Semantic search on legal texts           │
             │   • Context retrieval for LLM                │
             └──────────────────────────────────────────────┘
                                        │
                                        ▼
                 ┌────────────────────────────────────┐
                 │   AWS Bedrock Runtime (Mistral LLM)│
                 │   Generates final contextual answer │
                 └────────────────────────────────────┘
                                        │
                                        ▼
                           ┌─────────────────────────────┐
                           │     Clear French Answer     │
                           │  + References + Explanation │
                           └─────────────────────────────┘
