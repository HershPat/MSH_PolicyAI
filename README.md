# PolicyPal

## Tech Stack
- **Frontend:** React + Tailwind CSS + Axios  
- **Backend:** Python 3.10 + FastAPI + Uvicorn + PostgreSQL  
- **Cloud DB:** Supabase (current), AWS (future)  
- **RAG & DB querying:** LangChain  
  - SQLDatabaseChain for direct structured-data lookups  
  - RetrievalQA over unstructured docs in FAISS  
- **Embeddings:** sentence-transformers (all-MiniLM-L6)  
- **LLM:** Llama 2 (7B) via transformers or llama.cpp  
- **Vector Store:** faiss-cpu (LangChain wrapper)  
- **Testing:** pytest + HTTPX; Jest + React Testing Library  
- **CI/CD:** GitHub Actions  
- **Deployment:** Vercel  

## Timeline

### Weeks 1–2: Planning & Foundations
- Finalize detailed requirements & success criteria  
- Identify & catalog all data sources (Top 100 points, ER diagram)  
- Spin up dev environments (Python 3.10, FastAPI, React/Tailwind)  
- Lock in tech stack and cloud DB (Supabase or AWS)  
- Scaffold repo, CI (lint/tests), branch strategy  

### Weeks 3–4: Backend & RAG MVP
- Develop core backend services (asyncpg pool, yoyo migrations)  
- Integrate internal APIs (policy, billing)  
- Build RAG pipelines:  
  - SQLDatabaseChain for structured lookups  
  - RetrievalQA over FAISS for docs  
- Wire up initial LLM chat endpoint (LangChain + Llama 2)  

### Weeks 5–6: Frontend & End-to-End Flow
- Build React + Tailwind chat UI (components: input, message list, typing state)  
- Connect frontend → `/chat` via Axios  
- Run full end-to-end tests (FastAPI ↔ LangChain ↔ FAISS ↔ React)  
- Refine prompts & retrieval logic for accuracy, add citations in UI  

### Weeks 7–8: Final Testing & Deployment
- Internal beta testing with real users/agents  
- Add analytics (usage metrics) & logging (Sentry)  
- Security review (RBAC, secrets, CORS)  
- Containerize (Docker + Docker-Compose)  
- Deploy frontend (Vercel) & backend (AWS/Supabase functions or ECS)
