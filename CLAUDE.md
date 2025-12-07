# Claude Code Instructions: Evolution of Todo

**Project**: Hackathon II - The Evolution of Todo
**Role**: Constitutional Guardian + Code Generator
**Version**: 2.0.0
**Last Updated**: 2025-12-06

---

## Quick Navigation

### Essential Context (Read First)

| Document | Purpose | Location |
|----------|---------|----------|
| **Constitution** | Project principles & phase rules | `.specify/memory/constitution.md` |
| **SpecKit Guide** | DOs and DON'Ts for workflow | `docs/SPECKIT_DOS_AND_DONTS.md` |
| **Current Phase Spec** | Feature requirements | `specs/phase-{N}/spec.md` |
| **Current Phase Plan** | Technical design | `specs/phase-{N}/plan.md` |
| **Current Phase Tasks** | Implementation checklist | `specs/phase-{N}/tasks.md` |

### Subproject Context

| Location | Purpose |
|----------|---------|
| `backend/CLAUDE.md` | Python/FastAPI patterns and conventions |
| `frontend/CLAUDE.md` | Next.js/React patterns and conventions |

---

## Project Overview

A todo application that evolves through 5 phases:

| Phase | Focus | Technology | Status |
|-------|-------|------------|--------|
| **I** | Console App | Python 3.13+, UV, in-memory | ✅ Complete |
| **II** | Web App | Next.js 16+, FastAPI, Neon, Better Auth | 🔄 In Progress |
| **III** | AI Chatbot | OpenAI Agents SDK, MCP, ChatKit | ⏳ Pending |
| **IV** | Local K8s | Docker, Helm, Minikube | ⏳ Pending |
| **V** | Cloud + Advanced | DOKS, Kafka, Dapr | ⏳ Pending |

---

## SpecKit Workflow

```
Constitution → Spec → Clarify → Plan → Tasks → Implementation → Capstone
```

### Commands Reference

| Command | Purpose | Output |
|---------|---------|--------|
| `/sp.specify` | Create feature specification | `specs/{feature}/spec.md` |
| `/sp.clarify` | Resolve ambiguities | Updates `spec.md` |
| `/sp.plan` | Create technical design | `specs/{feature}/plan.md` |
| `/sp.tasks` | Generate task list | `specs/{feature}/tasks.md` |
| `/sp.adr` | Record architecture decision | `history/adr/` |
| `/sp.phr` | Record prompt history | `history/prompts/` |

---

## Specs Navigation

### Phase I (Complete)

```
specs/001-phase1-console-todo/
├── spec.md          # Feature requirements (4 user stories)
├── plan.md          # Technical design
├── tasks.md         # 39 tasks (all complete)
├── capstone.md      # Validation & completion
├── research.md      # Phase 0 research
├── data-model.md    # Task entity definition
├── quickstart.md    # Setup guide
└── contracts/
    └── cli-interface.md  # CLI contract
```

### Phase II (In Progress)

```
specs/phase-2/
├── spec.md          # Web app requirements
├── plan.md          # (To be created via /sp.plan)
└── tasks.md         # (To be created via /sp.tasks)
```

---

## Directory Structure

```
evolution_to_do/
├── .specify/                    # SpecKit configuration
│   ├── memory/
│   │   └── constitution.md      # Project principles (v1.2.1)
│   └── templates/               # Spec/plan/task templates
│
├── specs/                       # All specifications
│   ├── 001-phase1-console-todo/ # Phase I (complete)
│   └── phase-2/                 # Phase II (in progress)
│
├── backend/                     # Python backend
│   ├── src/                     # Source code
│   │   ├── models/              # Data models
│   │   ├── services/            # Business logic
│   │   ├── cli/                 # CLI handlers
│   │   └── lib/                 # Utilities
│   ├── tests/                   # pytest tests
│   └── CLAUDE.md                # Backend-specific context
│
├── frontend/                    # Next.js frontend (Phase II+)
│   └── CLAUDE.md                # Frontend-specific context
│
├── history/                     # Traceability
│   ├── adr/                     # Architecture Decision Records
│   └── prompts/                 # Prompt History Records
│
├── CLAUDE.md                    # This file (root context)
├── GEMINI.md                    # Gemini agent context
└── SPECKIT_DOS_AND_DONTS.md     # Workflow rules
```

---

## Constitutional Duties

As Claude Code, you have dual roles:

### 1. Code Generator
- Implement features from specifications
- Follow spec exactly - no scope creep
- Use only allowed technologies per phase

### 2. Constitutional Guardian
- Enforce phase boundaries
- Require documentation-first for new tools
- Remind about SESSION_HANDOFF updates
- Check feature necessity before implementation

### Phase Rules Summary

| Phase | Allowed | Prohibited |
|-------|---------|------------|
| **I** | Python, UV, standard lib, in-memory | DB, web, AI, Docker |
| **II** | +Next.js, FastAPI, Neon, Better Auth | AI, MCP, K8s, Kafka |
| **III** | +OpenAI SDK, MCP, ChatKit | K8s, Kafka, Dapr |
| **IV** | +Docker, Helm, Minikube | NEW features, Kafka |
| **V** | +DOKS, Kafka, Dapr, all features | Nothing prohibited |

---

## Before Starting Any Work

```bash
# 1. Check current phase
ls -1 specs/phase-* 2>/dev/null | tail -1

# 2. Read current spec
cat specs/phase-{N}/spec.md

# 3. Check if previous task is 100% complete
# Only ONE major task in progress at a time

# 4. For new tools, read docs first (30-minute rule)
```

---

## Active Technologies

### Phase I (Complete)
- Python 3.13+ with UV package manager
- Standard library only (no external dependencies)
- In-memory storage (Dict[int, Task])
- pytest for testing

### Phase II (Current)
- **Frontend**: Next.js 16+ (App Router)
- **Backend**: FastAPI + SQLModel
- **Database**: Neon PostgreSQL
- **Auth**: Better Auth (JWT)
- **Deployment**: Vercel (frontend)

---

## Code Standards

See `.specify/memory/constitution.md` for:
- Type safety requirements
- Error handling patterns
- Security principles
- Testing strategy

---

## Recent Changes

| Date | Change |
|------|--------|
| 2025-12-06 | Phase I complete, capstone validated |
| 2025-12-06 | Constitution updated to v1.2.1 (Capstone step) |
| 2025-12-06 | Phase II spec created |

---

**Remember**: You are a Constitutional Guardian. Enforce principles while supporting progress.
