# Evolution of Todo

> **Hackathon II**: The Evolution of Todo - A journey from console app to cloud-native, AI-powered task management system

**Status**: 🟡 Phase Pre-Setup (Framework)
**Points**: 0/1000 (Target: 1700 with bonuses)
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

## 🎯 Current Phase: Pre-Phase I (Setup)

**Current Focus**: Constitutional framework setup

**Completed**:
- ✅ Comprehensive constitution created
- ✅ Context preservation system (SESSION_HANDOFF.md)
- ✅ Enforcement mechanisms (scripts, hooks, checklists)
- ✅ Repository structure planned

**Next Steps**:
1. Create Phase I specification
2. Set up Python project with UV
3. Implement 5 Basic operations
4. Submit Phase I (Deadline: Dec 7, 2025)

---

## 🏗️ Architecture by Phase

### Phase I: Console App (Dec 1-7)
**Technology**: Python 3.13+, UV
**Features**: Add, Delete, Update, View, Mark Complete
**Storage**: In-Memory
**Points**: 100

### Phase II: Web Application (Dec 8-14)
**Technology**: Next.js 16+, FastAPI, Neon PostgreSQL, Better Auth
**Features**: All Phase I features + Multi-user + Authentication
**Storage**: PostgreSQL
**Points**: 150

### Phase III: AI Chatbot (Dec 15-21)
**Technology**: OpenAI Agents SDK, MCP Python SDK, ChatKit
**Features**: Natural language task management
**Storage**: PostgreSQL + Conversation history
**Points**: 200

### Phase IV: Local Kubernetes (Dec 22 - Jan 4)
**Technology**: Docker, Minikube, Helm, kubectl-ai, kagent
**Features**: Phase III app in containers
**Storage**: Same as Phase III
**Points**: 250

### Phase V: Cloud + Advanced (Jan 5-18)
**Technology**: DigitalOcean Kubernetes, Kafka, Dapr
**Features**: Priorities, Tags, Search, Recurring Tasks, Reminders
**Storage**: PostgreSQL + Kafka events
**Points**: 300

**Total Core Points**: 1000

---

## 🎁 Bonus Features (If Time Permits)

- 🔧 **Reusable Intelligence** (Subagents/Skills): +200 points
- 🏗️ **Cloud-Native Blueprints**: +200 points
- 🌍 **Urdu Language Support**: +100 points
- 🎤 **Voice Commands**: +200 points

**Maximum Points**: 1700

---

## 🚀 Quick Start

### Prerequisites

**Phase I**:
- Python 3.13+
- UV package manager
- Git

**Phase II** (additional):
- Node.js 18+
- npm/pnpm/yarn
- Neon account (free tier)

**Phase III** (additional):
- OpenAI API key
- MCP SDK

**Phase IV** (additional):
- Docker Desktop
- Minikube
- Helm

**Phase V** (additional):
- DigitalOcean account
- Redpanda Cloud account (free tier)

### Installation (Phase I)

```bash
# Clone repository
git clone https://github.com/[your-username]/evolution_to_do.git
cd evolution_to_do

# Set up Python environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Run application
uv run python backend/src/main.py
```

---

## 📚 Documentation

### Essential Documents (Read First)

- **[Constitution](.specify/memory/constitution.md)** - Project principles and enforcement (78KB, READ FIRST)
- **[Session Handoff](docs/SESSION_HANDOFF.md)** - Current context (updated daily)
- **[Project Status](docs/PROJECT_STATUS.md)** - Overall progress (updated weekly)
- **[Daily Checklist](docs/DAILY_CHECKLIST.md)** - Pre-work routine
- **[Quick Reference](QUICK_REFERENCE.md)** - Common commands

### SpecKit Plus Integration

- **[SpecKit Config](.specify/config.yaml)** - Configuration
- **[PHR Records](history/prompts/)** - Prompt History Records (auto-created)
- **[ADR Records](history/adr/)** - Architecture Decision Records
- **[Templates](.specify/templates/)** - Spec/Plan/Tasks/ADR/PHR templates

### Phase Specifications

- Phase I: `specs/phase-1/` (To be created)
- Phase II: `specs/phase-2/` (To be created)
- Phase III: `specs/phase-3/` (To be created)
- Phase IV: `specs/phase-4/` (To be created)
- Phase V: `specs/phase-5/` (To be created)

### Development Guides

- [Before New Tool](docs/BEFORE_NEW_TOOL.md) - 30-min reading checklist
- Weekly Cleanup: `scripts/weekly-cleanup.sh`
- Phase Gates: `scripts/check-phase-*-complete.sh`
- Feature Necessity: `scripts/check-feature-necessity.sh`

---

## 🎓 Learning from Previous Project

This project incorporates lessons from a previous project that achieved only 20% completion due to:

1. **No enforcement** → Constitution ignored
2. **Premature features** → Started authentication before finishing content
3. **Skipped documentation** → 6-8 hours wasted debugging better-auth
4. **Context loss** → 30-60 min/session reloading context
5. **Repository mess** → Build artifacts committed, documentation sprawl

### This Time We're Different

- ✅ **Triple enforcement**: Automated (scripts/hooks) + Manual (checklists) + AI (Claude reminders)
- ✅ **Phase discipline**: Hard gates between phases, cannot skip
- ✅ **Documentation first**: 30-min reading before any new tool
- ✅ **Context preservation**: SESSION_HANDOFF.md updated after every session
- ✅ **Repository hygiene**: .gitignore from Day 1, weekly cleanup

**Efficiency Target**: >80% (vs. 50% in previous project)

---

## 🛠️ Development Workflow

### Daily Routine

**Morning** (10 min):
1. Read `docs/SESSION_HANDOFF.md`
2. Run `docs/DAILY_CHECKLIST.md`
3. Verify phase alignment
4. Start working

**During Work**:
1. Follow current phase spec
2. If new tool: Run `docs/BEFORE_NEW_TOOL.md` (30 min)
3. Let Claude Code generate code from specs
4. Test thoroughly

**Evening** (10 min):
1. Commit changes
2. Update `docs/SESSION_HANDOFF.md`
3. Plan tomorrow's work

### Weekly Routine

**Every Friday** (30 min):
1. Run `scripts/weekly-cleanup.sh`
2. Update `docs/PROJECT_STATUS.md`
3. Review phase progress
4. Plan next week

---

## 🎯 Success Metrics

### Phase Completion
- Phase I: ❌ (Deadline: Dec 7)
- Phase II: ❌ (Deadline: Dec 14)
- Phase III: ❌ (Deadline: Dec 21)
- Phase IV: ❌ (Deadline: Jan 4)
- Phase V: ❌ (Deadline: Jan 18)

### Points Accumulation
- Current: 0/1000 (core)
- Bonus: 0/700
- Total: 0/1700

### Constitutional Compliance
- Phase boundaries: ✅ 100%
- Documentation first: ✅ 100%
- Context updates: ✅ 100%
- Repository clean: ✅ 100%
- One thing at a time: ✅ 100%

**Overall: 100% compliance** (5/5 checks)

---

## 🔗 Links

**Hackathon**:
- Main Page: https://lu.ma/theanvil-hackathon-II-evolution-of-todo
- Submission Form: https://forms.gle/CQsSEGM3GeCrL43c8

**Project** (To be created):
- Repository: [GitHub URL]
- Demo Video (Phase I): [YouTube URL]
- Live App (Phase II+): [Deployment URL]

**Technology Documentation**:
- [Python UV](https://docs.astral.sh/uv/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/docs)
- [Better Auth](https://www.better-auth.com/docs)
- [OpenAI Agents](https://platform.openai.com/docs/guides/agents)
- [MCP SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Dapr](https://docs.dapr.io/)

---

## 🤝 Contributing

This is a solo hackathon project. However, the constitutional framework and lessons learned are designed to be reusable.

**Reusable Components**:
- Constitutional framework
- Enforcement mechanisms (scripts, hooks, checklists)
- Spec-driven development workflow
- Context preservation system

---

## 📄 License

MIT License - See LICENSE file for details

---

## 👤 Author

[Your Name]
- GitHub: [@your-username]
- Email: your.email@example.com

---

## 🙏 Acknowledgments

**Lessons Learned From**:
- Previous project post-mortem (270+ pages of analysis)
- Spec-Driven Development methodology
- Constitutional enforcement patterns

**Technologies Used**:
- Python, UV, FastAPI, Next.js, PostgreSQL
- OpenAI, MCP, Docker, Kubernetes, Helm
- Kafka, Dapr, Better Auth
- And many more...

---

## 📊 Project Status

**Last Updated**: December 4, 2025

**Health**: 🟢 Excellent (setup phase, learned from past)

**Next Milestone**: Complete framework setup → Start Phase I

**Days to Phase I Deadline**: 3 days

---

**Note**: This README will be updated as the project progresses through each phase.

**Constitution**: All development follows `specs/CONSTITUTION.md` with triple enforcement (automated + manual + AI).

**Success Formula**: Quality × Efficiency × Consistency = 1700 Points

---

*Generated with Claude Code as part of Spec-Driven Development hackathon*
