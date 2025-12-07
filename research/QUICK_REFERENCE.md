# Quick Reference Guide

**Project**: Evolution of Todo
**Purpose**: Fast lookup for common commands and procedures

---

## 📋 Daily Workflow

### Morning (Start Session) - 10 minutes

```bash
# 1. Read context
cat docs/SESSION_HANDOFF.md

# 2. Check current status
git status
git log -1 --oneline

# 3. Verify phase alignment
ls -1 specs/phase-* | tail -1

# 4. Run daily checklist
cat docs/DAILY_CHECKLIST.md
# (Fill out a copy for today)
```

### Evening (End Session) - 10 minutes

```bash
# 1. Commit changes
git add <files>
git commit -m "type: description"

# 2. Update context
vim docs/SESSION_HANDOFF.md
# Update: Last Updated, accomplishments, next steps

# 3. Plan tomorrow
# Update "What's Next" in SESSION_HANDOFF.md
```

---

## 🚀 Phase-Specific Commands

### Phase I: Console App

```bash
# Set up Python environment
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
uv pip install -r requirements.txt

# Run application
uv run python backend/src/main.py

# Check phase complete
bash scripts/check-phase-1-complete.sh
```

### Phase II: Web App

```bash
# Frontend (Next.js)
cd frontend
npm install
npm run dev              # Development server
npm run build            # Production build
npm run lint             # Linting

# Backend (FastAPI)
cd backend
uv run uvicorn src.main:app --reload

# Database (Neon)
# Set in .env:
# DATABASE_URL=postgresql://...

# Better Auth Setup (CRITICAL: Use CLI)
npx @better-auth/cli migrate
# DO NOT create schema manually!

# Check phase complete
bash scripts/check-phase-2-complete.sh
```

### Phase III: AI Chatbot

```bash
# Install OpenAI SDK
uv pip install openai

# Install MCP SDK
uv pip install mcp

# Set API key in .env
# OPENAI_API_KEY=sk-...

# Run MCP server
uv run python backend/mcp_server/main.py

# Test chat endpoint
curl -X POST http://localhost:8000/api/user123/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'

# Check phase complete
bash scripts/check-phase-3-complete.sh
```

### Phase IV: Local Kubernetes

```bash
# Build Docker images
docker build -t todo-frontend:latest -f docker/Dockerfile.frontend frontend/
docker build -t todo-backend:latest -f docker/Dockerfile.backend backend/

# Start Minikube
minikube start

# Deploy with Helm
helm install todo-app helm/todo-app/

# Check deployment
kubectl get pods
kubectl get services

# Access application
minikube service todo-app-frontend

# kubectl-ai usage
kubectl-ai "deploy the todo frontend with 2 replicas"
kubectl-ai "check why the pods are failing"

# Check phase complete
bash scripts/check-phase-4-complete.sh
```

### Phase V: Cloud + Advanced

```bash
# Set up DigitalOcean Kubernetes
doctl kubernetes cluster kubeconfig save <cluster-name>

# Set up Redpanda Cloud
# Get bootstrap server and credentials from console

# Deploy Dapr components
kubectl apply -f dapr-components/

# Deploy application
helm upgrade todo-app helm/todo-app/ --values helm/todo-app/values-prod.yaml

# Check Kafka topics
rpk topic list --brokers <redpanda-url>

# Check Dapr sidecars
kubectl get pods -o=custom-columns=NAME:.metadata.name,CONTAINERS:.spec.containers[*].name

# Check phase complete
bash scripts/check-phase-5-complete.sh
```

---

## 🛡️ Constitutional Enforcement

### Before Starting Any Work

```bash
# Run daily checklist
cat docs/DAILY_CHECKLIST.md

# Check phase alignment
ls -1 specs/phase-* | tail -1
# Are you working on features from this phase only?
```

### Before Using New Tool

```bash
# Copy template
cp docs/BEFORE_NEW_TOOL.md docs/tools/<tool-name>-checklist.md

# Fill out (30 min minimum)
vim docs/tools/<tool-name>-checklist.md

# Read official documentation:
# - Quick start guide (10 min)
# - Version compatibility (5 min)
# - Common issues (5 min)
# - API reference (10 min)
```

### Before Starting New Feature

```bash
# Run feature necessity test
bash scripts/check-feature-necessity.sh

# Answer 4 questions (all must be YES):
# 1. In current phase spec?
# 2. Have all dependencies?
# 3. Delivers value NOW?
# 4. Spec defined?
```

### Before Moving to Next Phase

```bash
# Check current phase complete
bash scripts/check-phase-<N>-complete.sh

# Verify manual checks:
# - All features working
# - Demo video recorded
# - Form submitted
# - Confirmation received

# Only then proceed to next phase
```

---

## 🧹 Maintenance

### Weekly Cleanup (Every Friday)

```bash
# Run automated cleanup
bash scripts/weekly-cleanup.sh

# Manually check:
# - PROJECT_STATUS.md updated
# - No uncommitted changes
# - No documentation at root
# - Repository size healthy
```

### Git Hygiene

```bash
# Check status
git status

# Stage files explicitly (NEVER use git add .)
git add <specific-files>

# Commit with conventional commits
git commit -m "feat: add task deletion"
git commit -m "fix: correct update logic"
git commit -m "docs: update SESSION_HANDOFF"

# Check for build artifacts before commit
# (pre-commit hook should catch this)
git diff --cached --name-only | grep -E "build/|dist/|node_modules/"

# Delete merged branches
git branch --merged main | grep -v "main" | xargs git branch -d
```

---

## 📝 Spec-Driven Development

### Create New Spec

```bash
# Create phase spec directory
mkdir -p specs/phase-<N>

# Create spec files
touch specs/phase-<N>/spec.md
touch specs/phase-<N>/plan.md
touch specs/phase-<N>/tasks.md

# Edit spec
vim specs/phase-<N>/spec.md
```

### Implement from Spec

```
# Ask Claude Code:
@specs/phase-<N>/feature.md

Please implement this feature exactly as specified.
Use <technology> and follow phase rules.
```

### Update Spec

```bash
# If spec is wrong, fix spec first
vim specs/phase-<N>/spec.md

# Then ask Claude to re-implement
# Never edit generated code directly
```

---

## 🔍 Troubleshooting

### If Blocked on Technical Issue

```bash
# 1. Stop after 30 minutes of debugging
# (30-minute rule)

# 2. Re-read documentation
# Don't assume you understood correctly

# 3. Search GitHub issues
# Someone else probably hit this

# 4. Ask in official community
# Discord, forums, etc.

# 5. Document solution
vim docs/troubleshooting/<issue-name>.md
```

### If Behind Schedule

```bash
# Option A: Cut scope within phase
# Keep quality, reduce features

# Option B: Extend work hours
# If healthy and sustainable

# Option C: Skip bonus features
# Focus on core 1000 points

# Option D: Request extension
# Last resort, check rules first
```

### If Constitutional Violation

```bash
# 1. STOP immediately

# 2. Document why
vim WHY.md
# Include: what, why, impact, prevention

# 3. Choose: revert or continue
# Revert preferred, continue requires justification

# 4. Update constitution if rule needs changing
vim specs/CONSTITUTION.md
```

---

## 📊 Status Checks

### Current Phase

```bash
ls -1 specs/phase-* | tail -1
```

### Phase Completion

```bash
# Automated check
bash scripts/check-phase-<N>-complete.sh

# Manual check
cat specs/phase-<N>/tasks.md
# Are all tasks marked complete?
```

### Points Accumulated

```bash
# Check PROJECT_STATUS.md
grep "Points" docs/PROJECT_STATUS.md
```

### Constitutional Compliance

```bash
# Self-assessment
# Phase boundaries: Yes/No
# Docs read first: Yes/No
# SESSION_HANDOFF updated: Yes/No
# WIP limit (≤1): Yes/No
# Repository clean: Yes/No

# Target: 100% (5/5 Yes)
```

---

## 📚 Documentation Locations

### Essential Files

- Constitution: `specs/CONSTITUTION.md`
- Session Handoff: `docs/SESSION_HANDOFF.md`
- Project Status: `docs/PROJECT_STATUS.md`
- Daily Checklist: `docs/DAILY_CHECKLIST.md`
- Before New Tool: `docs/BEFORE_NEW_TOOL.md`
- This File: `QUICK_REFERENCE.md`

### Phase Specs

- Phase I: `specs/phase-1/`
- Phase II: `specs/phase-2/`
- Phase III: `specs/phase-3/`
- Phase IV: `specs/phase-4/`
- Phase V: `specs/phase-5/`

### Scripts

- Phase gates: `scripts/check-phase-*-complete.sh`
- Feature check: `scripts/check-feature-necessity.sh`
- Weekly cleanup: `scripts/weekly-cleanup.sh`

### Hooks

- Pre-commit: `.git/hooks/pre-commit`

---

## 🔗 Important Links

### Hackathon

- Main Page: https://lu.ma/theanvil-hackathon-II-evolution-of-todo
- Submission Form: https://forms.gle/CQsSEGM3GeCrL43c8

### Technology Docs

- Python UV: https://docs.astral.sh/uv/
- FastAPI: https://fastapi.tiangolo.com/
- Next.js: https://nextjs.org/docs
- Better Auth: https://www.better-auth.com/docs
- Neon: https://neon.tech/docs
- OpenAI: https://platform.openai.com/docs
- MCP: https://github.com/modelcontextprotocol/python-sdk
- Docker: https://docs.docker.com/
- Kubernetes: https://kubernetes.io/docs/
- Helm: https://helm.sh/docs/
- Dapr: https://docs.dapr.io/
- Redpanda: https://docs.redpanda.com/

---

## ⚡ Emergency Contacts

### If Claude Code Confused

```
Read these in order:
1. CLAUDE.md (your instructions)
2. specs/CONSTITUTION.md (project rules)
3. docs/SESSION_HANDOFF.md (current context)
```

### If You're Confused

```
Read these in order:
1. QUICK_REFERENCE.md (this file)
2. docs/SESSION_HANDOFF.md (what's happening now)
3. docs/PROJECT_STATUS.md (overall progress)
4. specs/CONSTITUTION.md (why we do things this way)
```

### If Something's Wrong

```bash
# Check git status
git status

# Check constitutional compliance
bash scripts/weekly-cleanup.sh
# (Runs checks even if not Friday)

# Review recent decisions
tail -20 docs/SESSION_HANDOFF.md
```

---

## 💡 Pro Tips

1. **Read SESSION_HANDOFF first** - Saves 30-60 min context loading
2. **30-min rule** - Always read docs before new tools
3. **One thing at a time** - 100% complete > 95% complete
4. **Phase discipline** - Finish phase before next
5. **Weekly cleanup** - Friday routine prevents mess

---

## 🎯 Success Shortcuts

### Fastest Path to Points

1. Follow phase order strictly
2. Read specs carefully
3. Let Claude Code generate code
4. Test thoroughly
5. Submit on time

### Avoid These Time Sinks

1. ❌ Skipping documentation (costs 6+ hours)
2. ❌ Starting new before finishing current (0% value)
3. ❌ Out-of-phase features (wasted effort)
4. ❌ Manual coding (defeats Spec-Driven Development)
5. ❌ Not updating SESSION_HANDOFF (costs 30-60 min)

---

## 📞 Quick Help

### "What should I do next?"

```bash
cat docs/SESSION_HANDOFF.md
# Look at "What's Next" section
```

### "What phase am I in?"

```bash
ls -1 specs/phase-* | tail -1
```

### "Is my work ready to submit?"

```bash
bash scripts/check-phase-<N>-complete.sh
```

### "Did I violate constitution?"

```bash
bash scripts/weekly-cleanup.sh
# Check compliance section
```

### "How much time do I have?"

```bash
grep "Deadline" docs/PROJECT_STATUS.md
```

---

**Last Updated**: December 4, 2025
**Version**: 1.0.0
**Keep This Handy**: Bookmark or print for fast reference

**Remember**: Quality × Efficiency × Consistency = Success
