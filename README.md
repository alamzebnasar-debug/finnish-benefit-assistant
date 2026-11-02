# 🇫🇮 Finnish Benefits & Tax AI Assistant

An enterprise-grade, containerized Retrieval-Augmented Generation (RAG) system designed to provide accurate, grounded guidance on Finnish public benefits (**Kela**) and tax deduction guidelines (**Vero**). 

Built as a production portfolio project showcasing modern AI engineering, clean microservice architecture, and full **MLOps observability**.

---

## 🏗️ Architecture & Tech Stack

* **Orchestration:** LangChain (LCEL)
* **LLM & Embeddings:** Google Gemini 3.5 Flash-Lite (`models/gemini-3.5-flash-lite`) & Google Generative AI Embeddings (`models/gemini-embedding-001`)
* **Vector Database:** ChromaDB (Local persistent vector store)
* **Backend API:** FastAPI (Asynchronous REST backend)
* **Frontend UI:** Streamlit (Interactive web chat interface)
* **Observability & Tracing:** LangSmith (Production telemetry & tracing)
* **Containerization:** Docker & Docker Compose

---

## 📁 Project Structure

```text
finnish-benefit-assistant/
│
├── backend/
│   ├── __init__.py
│   ├── main.py            # FastAPI application & endpoints
│   ├── agent.py           # LangChain RAG chain & Gemini configuration
│   ├── ingest.py          # Document loading, chunking, & ChromaDB indexing
│   └── chroma_db/         # Local persistent vector store
│
├── frontend/
│   ├── __init__.py
│   └── app.py             # Streamlit chat interface
│
├── data/
│   ├── kela_guidelines.txt
│   ├── kela_student_benefits.txt
│   ├── kela_unemployment_benefits.txt
│   └── vero_guidelines.txt
│
├── .env                   # Local secure environment variables
├── .env.example           # Environment variable template
├── Dockerfile             # Multi-stage/shared container build configuration
├── docker-compose.yml     # Multi-container orchestration (FastAPI + Streamlit)
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation