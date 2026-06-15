TutorMind Deployment Guide
==========================

This document provides recommended deployment steps for the TutorMind stack.

Overview
--------
Technology requirements (strict):
- Frontend: React + Vite, Tailwind CSS
- Backend: FastAPI (uvicorn)
- Database: MongoDB (MongoDB Atlas recommended)
- Authentication: Firebase Authentication
- Vector Store / RAG: MongoDB Atlas Vector Search or external vector DB
- Agents/Orchestration: LangGraph + MCP tool layer (deployed separately)

High-level architecture
-----------------------
- Frontend (Vite/React) served on Vercel or static hosting
- Backend (FastAPI) served on Render / Railway / AWS (use HTTPS)
- MongoDB Atlas for production database and vector search
- Firebase project for Authentication and credentials
- LangGraph orchestrator + MCP servers deployed as separate services (Docker or cloud VMs)

Environment variables
---------------------
Frontend (.env for Vite)
- VITE_FIREBASE_API_KEY=
- VITE_FIREBASE_AUTH_DOMAIN=
- VITE_FIREBASE_PROJECT_ID=
- VITE_API_BASE_URL=https://api.yourdomain.com

Backend (`backend/.env`)
- MONGODB_URI= (use MongoDB Atlas connection string)
- FIREBASE_CREDENTIALS= (JSON string or file path to Firebase service account)
- GOOGLE_API_KEY= (for Gemini embeddings)
- LANGCHAIN_API_KEY= (if used)
- COMPOSIO_API_KEY=
- TAVILY_API_KEY=
- EMAIL_SERVICE_KEY=
- JWT_SECRET=

Infrastructure & hosting recommendations
----------------------------------------
- MongoDB Atlas: Create a cluster, enable IP whitelisting and create a database `tutormind`. Use Atlas Vector Search for embeddings if available.
- Firebase: Create a project, enable Email & Google sign-in, generate a service account JSON and store it securely (set `FIREBASE_CREDENTIALS`).
- Frontend: Deploy `frontend` to Vercel. Set environment variables in Vercel using the Vite prefixes.
- Backend: Deploy `backend` to Render / Railway / AWS. Configure environment variables and ensure network access to MongoDB Atlas and MCP servers.
- LangGraph & MCP: Deploy LangGraph orchestrator and each MCP server (email, search, youtube, document, calendar, notification, analytics) as separate services behind an internal network or API gateway. Agents must call MCP endpoints rather than external APIs directly.

Quick deployment steps (local dev)
---------------------------------
1. Start MongoDB (local or Atlas). For local: run MongoDB or use Docker.

2. Backend

```powershell
cd backend
python -m venv .venv
. .venv\Scripts\activate
pip install -r requirements.txt
# create .env from .env.example and fill values
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

3. Frontend

```bash
cd frontend
npm install
# create .env with VITE_* variables
npm run dev
```

Production deployment notes
---------------------------
- Use HTTPS and enable HSTS.
- Use a secret manager for env vars (Render secrets, Vercel env vars, AWS Secrets Manager).
- Configure firewall and IP allowlists on MongoDB Atlas.
- Configure monitoring and alerts (Uptime, Sentry, Prometheus/Grafana).
- Implement rate limiting and a WAF for the API gateway.

LangGraph & MCP specifics
-------------------------
- LangGraph: run the orchestrator as a separate service. Use the `backend/app/agents` code as the starting point for agent implementations.
- MCP servers: implement production MCP endpoints that act as proxies to external services. Agents call MCP endpoints; MCP handles authentication, rate-limiting, filtering, and logging.

Rollback & migrations
---------------------
- Version your database migrations (use a migration tool or scripts) and backup data before schema changes.

Security checklist
------------------
- Enforce HTTPS
- Use strong JWT_SECRET
- Limit CORS to trusted origins
- Validate file uploads and scan for malware
- Protect Firebase service account and limit scope

Support
-------
For questions about deployment steps or adjustments for your cloud provider, ask and I can provide a tailored script or `Dockerfile` and `docker-compose` setup.

Docker deployment (optional)
----------------------------
The repository includes Dockerfiles for the backend and frontend and a `docker-compose.yml` to run a minimal stack locally (FastAPI backend, Vite-built frontend served by nginx, and MongoDB).

Quick local docker run

```bash
docker-compose build
docker-compose up -d
# Backend: http://localhost:8000
# Frontend: http://localhost:3000
```

Notes
- Ensure `backend/.env` and `frontend/.env` are present with production values before starting.
- For production use, run services behind a reverse proxy (Traefik / Nginx) and secure env vars via a secret manager.
