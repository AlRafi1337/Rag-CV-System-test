# 📄 RAG CV System (FastAPI + Postgres/pgvector + React + IMAP)

An enterprise-grade, containerized **Retrieval-Augmented Generation (RAG)** system to:

- Store and manage CVs
- Enable **natural-language semantic search**
- Visualize search results as an **interactive graph**
- Auto-ingest CVs directly from your **mail server**

---

## ✨ Features

- 📂 **RAG store:**  
  Chunked CV documents with **pgvector semantic search** + Postgres **full-text hybrid ranking**

- 📥 **Ingestion:**

  - Upload API
  - Directory pipeline CLI
  - **IMAP mail ingestion** for automatic CV capture

- 🔎 **Search:**

  - Semantic + keyword hybrid search
  - Graph API for **visual exploration**

- 🖥️ **Frontend:**  
  React app with **graph canvas** + results list

- ⚙️ **Configurable embeddings:**
  - Local `SentenceTransformers` by default
  - Switch to **OpenAI embeddings** with `.env`

---

## 🏗️ Architecture

```plaintext
              ┌───────────────┐
              │     Email     │
              │ (IMAP Server) │
              └───────┬───────┘
                      │
                      ▼
              ┌─────────────────┐
              │   Ingestion     │
              │  (FastAPI API)  │
              └───┬─────────┬───┘
                  │         │
          ┌───────▼───┐   ┌─▼──────────────┐
          │ PostgreSQL │   │ Embeddings     │
          │ + pgvector │◀──▶ (ST / OpenAI) │
          └────────────┘   └──────┬────────┘
                                  │
                          ┌───────▼────────┐
                          │   React UI     │
                          │ Graph + Search │
                          └────────────────┘
🚀 Quick Start
1️⃣ Setup Environment
Copy .env.example → .env and adjust values:

cp .env.example .env
2️⃣ Start with Docker
docker compose up --build
Backend → http://localhost:8000

Frontend → http://localhost:5173

3️⃣ Switch to OpenAI embeddings
Edit .env:

environment.OPENAI_API_KEY=sk-xxxx
4️⃣ Start with Docker
docker compose up --build
```

EMBEDDINGS_PROVIDER=openai
OPENAI_API_KEY=sk-xxxx
⚙️ API Endpoints
Method Endpoint Description
POST /upload Upload file(s), ingest, chunk, embed, store
GET /documents List latest ingested CVs
POST /search Hybrid search ({"query":"…","k":20})
POST /search/graph Returns nodes + edges for force graph
GET /health Health check


Required .env vars:
env
Copy code
IMAP_HOST=imap.yourmail.com
IMAP_PORT=993
IMAP_USER=hr-inbox@example.com
IMAP_PASSWORD=changeme
