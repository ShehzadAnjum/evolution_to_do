# Evolution of Todo

> **Hackathon II**: A progressive todo application that evolves from console app to cloud-native, AI-powered system

**Status**: 🟢 Phase I Complete | 🟡 Phase II In Progress  
**Points**: 100/1000 (10%)  
**Started**: December 4, 2025  
**Deadline**: January 18, 2026

---

## 📋 Project Overview

This project demonstrates **Spec-Driven Development** by building a Todo application that evolves through 5 progressive phases, each introducing new technologies and architectural patterns.

### The Evolution Path

```
Phase I    →    Phase II     →    Phase III    →    Phase IV    →    Phase V
Console         Web App           AI Chatbot       Local K8s         Cloud + Advanced
Python          Next.js           OpenAI           Docker            DigitalOcean
In-Memory       FastAPI           MCP              Minikube          Kafka
UV              PostgreSQL        ChatKit          Helm              Dapr
                Better Auth                                          Events
```

---

## 🎯 Current Phase: Phase II (Web Application)

**Status**: 85% Complete  
**Deadline**: December 14, 2025  
**Focus**: Full-stack web application with authentication and persistent storage

### What's Complete
- ✅ Backend API (FastAPI with all CRUD endpoints)
- ✅ Frontend (Next.js with Better Auth)
- ✅ Database connection (Neon PostgreSQL)
- ✅ Multi-user task isolation
- ✅ All 5 Basic operations in web UI

### What's Remaining
- ⚠️ Phase II capstone validation
- ⚠️ Demo video recording
- ⚠️ Deployment verification
- ⚠️ Form submission

---

## 🚀 Quick Start

### Prerequisites
- Python 3.13+ with [UV](https://docs.astral.sh/uv/)
- Node.js 20+ with npm
- Neon PostgreSQL account (free tier)
- Vercel account (free tier)

### Phase I (Console App) - Complete ✅

```bash
cd backend
uv sync
uv run python -m src.main
```

See [backend/README.md](backend/README.md) for details.

### Phase II (Web App) - In Progress 🟡

**Backend**:
```bash
cd backend
uv sync
# Create .env file (see backend/.env.example)
uv run uvicorn src.api.main:app --reload --port 8000
```

**Frontend**:
```bash
cd frontend
npm install
# Create .env.local file (see frontend/.env.example)
npm run dev
```

See [backend/README.md](backend/README.md) and [frontend/README.md](frontend/README.md) for details.

---

## 📁 Project Structure

```
evolution_to_do/
├── .specify/              # SpecKit configuration
│   ├── memory/
│   │   └── constitution.md
│   └── templates/
│
├── specs/                 # All specifications
│   ├── 001-phase1-console-todo/  # Phase I (complete)
│   └── phase-2/                  # Phase II (in progress)
│
├── backend/               # Python backend
│   ├── src/              # Source code
│   └── tests/            # Test suite
│
├── frontend/             # Next.js frontend
│   ├── app/              # App Router pages
│   └── components/       # React components
│
├── docs/                 # Documentation
│   ├── SESSION_HANDOFF.md
│   ├── DAILY_CHECKLIST.md
│   └── PROJECT_STATUS.md
│
├── scripts/              # Automation scripts
│   ├── check-phase-*-complete.sh
│   └── weekly-cleanup.sh
│
├── history/              # Traceability
│   ├── adr/             # Architecture Decision Records
│   └── prompts/         # Prompt History Records
│
├── CLAUDE.md             # AI agent context
├── GEMINI.md             # AI agent context
└── README.md             # This file
```

---

## 🧪 Testing

### Backend Tests
```bash
cd backend
uv run pytest              # Run all tests
uv run pytest --cov=src    # With coverage
```

**Current Status**: 52/52 tests passing ✅

### Frontend Tests
```bash
cd frontend
npm run test
```

---

## 📊 Phase Status

| Phase | Status | Points | Deadline |
|-------|--------|--------|----------|
| **I** - Console App | ✅ Complete | 100/100 | Dec 7 |
| **II** - Web App | 🟡 85% | 0/150 | Dec 14 |
| **III** - AI Chatbot | ⏳ Pending | 0/200 | Dec 21 |
| **IV** - Local K8s | ⏳ Pending | 0/250 | Jan 4 |
| **V** - Cloud + Advanced | ⏳ Pending | 0/300 | Jan 18 |

**Total**: 100/1000 points (10%)

---

## 📚 Documentation

- **[Constitution](.specify/memory/constitution.md)** - Project principles and rules
- **[SpecKit Guide](docs/SPECKIT_DOS_AND_DONTS.md)** - Workflow DOs and DON'Ts
- **[Project Status](docs/PROJECT_STATUS.md)** - Current state and metrics
- **[Session Handoff](docs/SESSION_HANDOFF.md)** - Context preservation
- **[Backend README](backend/README.md)** - Backend setup and API docs
- **[Frontend README](frontend/README.md)** - Frontend setup and usage

---

## 🛠️ Technology Stack

### Phase I (Complete)
- Python 3.13+ with UV
- Standard library only
- In-memory storage
- pytest for testing

### Phase II (Current)
- **Frontend**: Next.js 16+ (App Router)
- **Backend**: FastAPI + SQLModel
- **Database**: Neon PostgreSQL
- **Auth**: Better Auth (JWT)
- **Deployment**: Vercel (frontend)

### Phase III (Planned)
- OpenAI Agents SDK
- MCP Python SDK
- ChatKit UI

### Phase IV (Planned)
- Docker
- Helm
- Minikube

### Phase V (Planned)
- DigitalOcean Kubernetes (DOKS)
- Kafka (Redpanda Cloud)
- Dapr

---

## 🎯 Goals

- **Core Phases**: 1000 points (all 5 phases)
- **Bonus Features**: Up to 700 additional points
- **Total Target**: 1700 points

---

## 🤝 Contributing

This is a hackathon project following strict SpecKit workflow principles. See the [Constitution](.specify/memory/constitution.md) for development guidelines.

---

## 📝 License

Part of Hackathon II - The Evolution of Todo

---

**Last Updated**: 2025-12-07  
**Version**: 0.2.0

