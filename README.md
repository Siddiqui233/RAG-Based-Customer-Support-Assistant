# 🤖 RAG-Based Customer Support Assistant
> A powerful AI-powered customer support system built with LangGraph, ChromaDB, Groq LLM, and Streamlit — featuring Human-in-the-Loop (HITL) escalation.
---
📌 Project Overview
This project implements a Retrieval-Augmented Generation (RAG) system that:
Processes any PDF knowledge base
Retrieves relevant information using HuggingFace embeddings
Answers user queries using Groq's LLaMA model
Routes complex queries to a human agent via LangGraph HITL
Built as part of an AI internship final project evaluation.
---
🚀 Features
Feature	Description
💬 Q&A Chat	Ask questions about your uploaded PDF
📝 Summary	Auto-generate a summary of the document
🧠 Quiz	Generate interactive MCQ quiz from content
🃏 Flashcards	Create study flashcards from key concepts
🤖 Support Agent	LangGraph-powered agent with HITL escalation
---
🏗️ Architecture
```
User Query
    │
    ▼
┌─────────────┐
│  Streamlit  │  ← Frontend UI
│    App      │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌──────────────┐
│  PDF Loader │────▶│   Chunker    │
└─────────────┘     └──────┬───────┘
                           │
                           ▼
                   ┌──────────────┐
                   │  ChromaDB    │  ← Vector Store
                   │ (Embeddings) │
                   └──────┬───────┘
                           │
                           ▼
                   ┌──────────────┐
                   │  LangGraph   │
                   │    Agent     │
                   └──────┬───────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
       ┌─────────────┐         ┌─────────────────┐
       │ Answer Node │         │  Escalate Node  │
       │ (Groq LLM)  │         │  (Human Agent)  │
       └─────────────┘         └─────────────────┘
```
---
🛠️ Tech Stack
Layer	Technology
Frontend	Streamlit
LLM	Groq (LLaMA 3.1 8B Instant)
Embeddings	HuggingFace (`all-MiniLM-L6-v2`)
Vector Store	ChromaDB
Orchestration	LangGraph
PDF Parsing	pdfplumber
Language	Python 3.11+
---
📁 Project Structure
```
rag-project/
├── app.py                  # Main Streamlit app
├── main.py                 # Entry point
├── requirements.txt        # Dependencies
├── .env                    # API keys (not committed)
├── data/                   # Sample PDF files
└── src/
    ├── loader.py           # PDF loading with pdfplumber
    ├── chunker.py          # Text splitting
    ├── embeddings.py       # ChromaDB vector store
    ├── retriever.py        # Semantic search
    ├── llm.py              # Groq LLM integration
    ├── rag_pipeline.py     # Core RAG pipeline
    └── graph_pipeline.py   # LangGraph HITL agent
```
---
⚙️ Setup & Installation
1. Clone the repository
```bash
git clone https://github.com/your-username/rag-customer-support.git
cd rag-customer-support
```
2. Create virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Set up environment variables
Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get your free Groq API key at: https://console.groq.com
5. Run the app
```bash
streamlit run app.py
```
Open your browser at: http://localhost:8501
---
🔁 How It Works
RAG Pipeline
User uploads a PDF
PDF is parsed and split into chunks
Chunks are embedded using HuggingFace and stored in ChromaDB
User query is embedded and matched against stored chunks
Relevant context is passed to Groq LLM for answer generation
LangGraph HITL Flow
```
User Query → Process Node → Intent Router
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
             Answer Node            Escalate Node
           (AI Response)          (Human Agent Panel)
```
answer → Query is within scope, LLM responds
escalate → Complex/emotional query, routed to human agent
---
📦 Requirements
```
streamlit
langchain
langchain-community
langchain-chroma
langchain-huggingface
langchain-text-splitters
langgraph
chromadb
pdfplumber
sentence-transformers
python-dotenv
requests
```
---
🖼️ Screenshots
> Upload your own screenshots to a `screenshots/` folder and update the paths below.
Feature	Preview
Q&A Chat	`screenshots/qa.png`
Summary	`screenshots/summary.png`
Quiz	`screenshots/quiz.png`
Support Agent	`screenshots/agent.png`
---
🔑 API Keys Required
Service	Purpose	Link
Groq	LLM inference (free)	https://console.groq.com
---
📄 License
This project is for educational purposes as part of an AI internship program.
---
👤 Author
Majeed Siddiqui  
AI/ML Intern  
📧 Connect on LinkedIn
---
⭐ If this project helped you, give it a star!
