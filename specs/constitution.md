<!--
================================================================================
SYNC IMPACT REPORT - Constitution v1.3.0 Reusable Intelligence Transparency
================================================================================
Date: 2025-12-10
Version: 1.2.1 → 1.3.0 (MINOR bump)
Action: Add Principle IX requiring Claude to announce RI artifacts being used

VERSION CHANGES:
- Previous Version: 1.2.1
- Current Version: 1.3.0
- Version Bump Type: MINOR (new principle added)

CHANGES MADE:
1. Added Principle IX: Reusable Intelligence Transparency
2. Claude must announce which agents/subagents/skills are being used before tasks
3. Claude must proactively suggest knowledge updates when discovering new patterns
4. Claude must request permission before modifying any RI artifact

PREVIOUS CHANGES (v1.2.1):
1. Added Step 9: Capstone (Validation & Completion) to workflow
2. Capstone step includes: validation against Spec, Plan, Constitution
3. Aligns with SPECKIT_DOS_AND_DONTS.md workflow requirements

PRINCIPLES (9 Non-Negotiable):
1. Phase Boundaries Are HARD GATES
2. Finish One Thing Before Starting Next
3. Read Documentation First (30-Minute Rule)
4. Context Preservation Protocol
5. Repository Cleanliness from Day 1
6. Spec-Driven Development (AI Writes Code)
7. Value-Driven Feature Development
8. Quality Over Speed (But Achieve Both)
9. Reusable Intelligence Transparency

SPECKIT WORKFLOW:
Constitution → Spec → Clarify (optional) → Plan → Tasks → Implementation → Capstone

TEMPLATE SYNCHRONIZATION STATUS:
✅ .specify/templates/spec-template.md - Use via /sp.specify
✅ .specify/templates/plan-template.md - Use via /sp.plan
✅ .specify/templates/tasks-template.md - Use via /sp.tasks
✅ .specify/templates/phr-template.prompt.md - Use via /sp.phr
✅ .specify/templates/adr-template.md - Use via /sp.adr

FILES UPDATED:
✅ specs/constitution.md - This file (Principle IX added)

COMMIT MESSAGE SUGGESTION:
docs: amend constitution to v1.3.0 (add Principle IX - RI Transparency)

- Added Principle IX: Reusable Intelligence Transparency
- Claude must announce which agents/subagents/skills are being used
- Claude must suggest knowledge updates when discovering new patterns
- Version bump: 1.2.1 → 1.3.0 (MINOR - new principle)

================================================================================
-->

# Evolution of Todo: Project Constitution

**Created**: December 4, 2025
**Version**: 1.3.0
**Last Amended**: 2025-12-10
**Project**: Hackathon II - The Evolution of Todo
**Objective**: Master Spec-Driven Development & Cloud Native AI (1000 points target)

---

## Table of Contents

1. [Meta-Constitution: Why This Document Exists](#meta-constitution-why-this-document-exists)
2. [The Learning: What Went Wrong Last Time](#the-learning-what-went-wrong-last-time)
3. [Core Philosophy](#core-philosophy)
4. [Non-Negotiable Principles](#non-negotiable-principles)
5. [Phase-Specific Rules](#phase-specific-rules)
6. [Enforcement Mechanisms](#enforcement-mechanisms)
7. [Repository Structure & Hygiene](#repository-structure--hygiene)
8. [Daily & Weekly Workflows](#daily--weekly-workflows)
9. [Emergency Protocols](#emergency-protocols)
10. [Success Metrics](#success-metrics)
11. [Governance](#governance)

---

## Meta-Constitution: Why This Document Exists

### The Paradox

Previous project: **Excellent planning (570-line constitution, comprehensive specs), poor execution (20% completion, 50% efficiency)**.

**Root Cause**: Created great plans, then ignored them during implementation. No enforcement mechanism.

**This Time**: Constitution has **teeth** - automated checks, manual gates, AI reminders. Violation is **not possible** without explicit override.

### The Stakes

- **Deadline**: 5 phases × 7 days = 35 days (Dec 1 - Jan 18, 2026)
- **Time Available**: 20-30 hours/week × 5 weeks = 100-150 hours
- **Time Required**: ~120-140 hours for all 5 phases (if efficient)
- **Points Target**: 1000 points (all phases) + bonus features
- **Risk**: Repeat past mistakes → incomplete phases, wasted time

### The Commitment

**I commit to following this constitution exactly as written.** If I deviate:
1. Document the deviation explicitly (WHY.md)
2. Update constitution if change is permanent
3. Accept the consequences (potential phase incompletion)

**This constitution is the contract I make with my future self.**

---

## The Learning: What Went Wrong Last Time

### Critical Mistakes from Previous Project

1. **Started Features Before Finishing Content** (SEVERITY: CRITICAL)
   - Built authentication after 20% of content (should be 100%)
   - Result: Neither content nor features complete
   - **Lesson**: Finish Phase N 100% before Phase N+1

2. **Didn't Read Documentation First** (SEVERITY: HIGH)
   - Skipped better-auth docs → 6-8 hours wasted debugging schema
   - **Lesson**: 30 minutes reading > 6 hours debugging

3. **Context Loss Between Sessions** (SEVERITY: HIGH)
   - 30-60 minutes per session reloading context
   - Total: 3-5 hours wasted across sessions
   - **Lesson**: SESSION_HANDOFF.md is non-negotiable

4. **Repository Organization Failures** (SEVERITY: MEDIUM)
   - Build artifacts committed (7.5M bloat)
   - 23+ docs at root level (sprawl)
   - **Lesson**: Structure and .gitignore from Day 1

5. **Ignored Own Plan** (SEVERITY: CRITICAL)
   - Spent 8-12 hours planning, then deviated
   - No enforcement, no accountability
   - **Lesson**: Constitution needs enforcement mechanisms

### The Four Priorities (From Old Project Analysis)

This constitution is built around preventing these four failures:

1. ✅ **No Premature Features**: Strict phase boundaries
2. ✅ **Context Preservation**: SESSION_HANDOFF system mandatory
3. ✅ **Documentation First**: 30-min reading rule before any tool
4. ✅ **Repository Cleanliness**: Structure and hooks from Day 1

---

## Core Philosophy

### 1. Spec-Driven Development

**Rule**: AI (Claude Code) writes code. Human writes specs **using SpecKit commands**.

**Process** (Using SpecKit Commands):
1. Human: Create spec using `/sp.specify` command
2. Human: Create plan using `/sp.plan` command
3. Human: Generate tasks using `/sp.tasks` command
4. Human: Reference spec: `@specs/phase-N/spec.md`
5. Claude: Read spec and implement
6. Human: Test result
7. If wrong: Update spec using `/sp.specify`, then re-implement
8. Repeat until correct

**MANDATORY**: All specs, plans, and tasks MUST be created via SpecKit `/sp.*` commands.
**PROHIBITED**: Manual `vim specs/...` file creation (bypasses SpecKit workflow)

### 2. Phase Discipline

**Rule**: Each phase is a HARD GATE. Cannot start Phase N+1 until Phase N is 100% complete and deployed.

**Why**: Previous project started Phase C (authentication) while Phase B (content) was only 20% complete. Result: Both incomplete.

**Enforcement**: Automated phase gate script (see Enforcement section)

### 3. Value-Driven Development

**Rule**: Every feature must deliver value **RIGHT NOW**, not theoretically in the future.

**Test Before Adding Feature**:
- Does this work with **current** functionality? (not future)
- Do I need this **today**? (not "might need later")
- Is this in **current phase**? (not future phase)

**Example**:
- ❌ Wrong: Add Kafka in Phase II (Kafka is Phase V)
- ✅ Right: Add Kafka in Phase V after Phase IV complete

### 4. One Thing at a Time

**Rule**: Work on exactly ONE major task. Complete to 100% (deployed, tested) before starting next.

**Definition of 100% Complete**:
- Code implemented and merged
- Tests passing
- Deployed (where applicable)
- Documented
- Spec marked complete
- No known blockers

**Prohibited**:
- ❌ Starting feature Y while feature X is 95% done
- ❌ "I'll finish X later, let's start Y now"
- ❌ Multiple parallel features

### 5. Documentation First, Always

**Rule**: Before using ANY new tool, library, or framework, spend 30 minutes reading official documentation.

**Checklist** (see Enforcement section):
- [ ] Quick start guide (10 min)
- [ ] Version compatibility (5 min)
- [ ] Common issues (5 min)
- [ ] API reference for features I'll use (10 min)

**Cost of Skipping**: 6-8 hours debugging (proven by better-auth experience)

**30-Minute Rule**: If debugging for 30 minutes, STOP and read documentation.

### 6. Context Preservation is Sacred

**Rule**: Update `docs/SESSION_HANDOFF.md` at the end of **every work session** (takes 5 minutes).

**Cost of Skipping**: 30-60 minutes next session reloading context.

**ROI**: 5 minutes invested → 30-60 minutes saved = 6-12x return.

**Enforcement**: Pre-commit hook warns if SESSION_HANDOFF.md not updated in 2+ hours.

### 7. Repository Cleanliness is Non-Negotiable

**Rules**:
1. Never commit build artifacts
2. Never commit secrets/env files
3. Keep docs organized (not at root)
4. No duplicate specs
5. Delete merged branches
6. Clean up weekly

**Enforcement**: Pre-commit hooks + weekly cleanup script

### 8. Quality Over Speed (But Aim for Both)

**Rule**: Each phase must be production-ready at its own level.

**Not Acceptable**:
- ❌ "Quick and dirty implementation to hit deadline"
- ❌ "We'll fix tech debt later"
- ❌ "Skip tests to move faster"

**Acceptable**:
- ✅ Phase I has no database (by design, not laziness)
- ✅ Phase II has no AI (by design, wait for Phase III)
- ✅ Intentional simplicity for current phase

**Principle**: Each phase is MVP for that level. Phase I = Console MVP. Phase II = Web MVP. Etc.

---

## Non-Negotiable Principles

### Principle I: Phase Boundaries Are HARD GATES

**Rule**: Complete Phase N 100% before starting ANY Phase N+1 work.

**Phase I (Console App) COMPLETE Means**:
- ✅ All 5 Basic features work (Add, Delete, Update, View, Mark Complete)
- ✅ Clean Python code generated by Claude Code from specs
- ✅ README.md with setup instructions
- ✅ CLAUDE.md with project context
- ✅ Specs in `specs/phase-1/` folder
- ✅ Repo pushed to GitHub
- ✅ Demo video recorded (< 90 seconds)
- ✅ Submitted via form

**Phase II (Web App) COMPLETE Means**:
- ✅ All Phase I features in web UI
- ✅ FastAPI backend with REST endpoints
- ✅ Next.js frontend deployed on Vercel
- ✅ Neon PostgreSQL connected
- ✅ Better Auth working (signup/signin/JWT)
- ✅ Multi-user isolation working
- ✅ Demo video recorded
- ✅ Submitted via form

**Phase III (AI Chatbot) COMPLETE Means**:
- ✅ OpenAI Agents SDK integrated
- ✅ MCP server with 5 tools (add/list/update/delete/complete)
- ✅ ChatKit UI for conversations
- ✅ Stateless chat endpoint with DB persistence
- ✅ Natural language task management working
- ✅ Demo video recorded
- ✅ Submitted via form

**Phase IV (Local K8s) COMPLETE Means**:
- ✅ Docker images for frontend/backend
- ✅ Helm charts created
- ✅ Minikube deployment working
- ✅ kubectl-ai and/or kagent usage demonstrated
- ✅ Demo video recorded
- ✅ Submitted via form

**Phase V (Cloud + Advanced) COMPLETE Means**:
- ✅ DOKS cluster deployed
- ✅ Kafka + Dapr integrated
- ✅ Intermediate features (priorities, tags, search, sort)
- ✅ Advanced features (recurring tasks, reminders)
- ✅ CI/CD pipeline working
- ✅ Demo video recorded
- ✅ Submitted via form

**Enforcement**: `scripts/check-phase-gate.sh` runs before starting new phase.

---

### Principle II: Finish One Thing Before Starting Next

**Rule**: Only ONE major task in progress at any time.

**In Progress Definition**: Started but not 100% complete.

**Maximum WIP (Work In Progress)**: 1 major task.

**Example Scenario**:
- ✅ Correct: Working on "Add Task" feature. Complete it 100%. Then start "Delete Task".
- ❌ Wrong: Working on "Add Task" (95% done). Start "Delete Task" because "Add is almost done".

**Why**: 95% done = 0% value delivered. Finish it.

**Enforcement**:
- Manual: Check `docs/SESSION_HANDOFF.md` → "In Progress" section should have max 1 item
- Automated: Pre-work checklist asks "Is previous task 100% done?"

---

### Principle III: Read Documentation First (30-Minute Rule)

**Rule**: Before using new tool, spend 30 minutes reading docs.

**Applies To**:
- New libraries (UV, FastAPI, Next.js, Better Auth, OpenAI SDK, MCP SDK)
- New frameworks
- New deployment platforms (Vercel, Neon, DigitalOcean, Minikube)
- New tools (Docker, Helm, kubectl-ai, Dapr)

**Checklist** (`docs/BEFORE_NEW_TOOL.md`):
```markdown
Tool: [Name]
Date: [Date]

[ ] Read quick start guide (10 min)
[ ] Check version compatibility with existing tools (5 min)
[ ] Review "Troubleshooting" or "Common Issues" section (5 min)
[ ] Read API reference for features I'll use (10 min)
[ ] Checked GitHub issues for recent problems (5 min)

Total Time: 30 minutes minimum

If stuck after 30 minutes of debugging:
[ ] Re-read documentation (don't assume I understood)
[ ] Search official GitHub issues
[ ] Ask in official community
```

**30-Minute Debugging Rule**: If debugging for 30 minutes without progress, STOP. Re-read docs.

**Enforcement**:
- Manual: Run checklist before using new tool
- AI reminder: Claude Code asks "Have you read the documentation for [tool]?"

---

### Principle IV: Context Preservation Protocol

**Rule**: Update `docs/SESSION_HANDOFF.md` at end of every work session.

**Cost of Skipping**: 30-60 minutes next session reloading context.

**SESSION_HANDOFF.md Structure**:
```markdown
# Session Handoff

**Last Updated**: [Timestamp]
**Updated By**: [Your name]
**Current Phase**: [I/II/III/IV/V]
**Current Branch**: [branch name]

---

## Quick Status (30-Second Read)

### Current State
- 🟢 Working: [What's deployed and functional]
- 🟡 In Progress: [Exactly ONE item]
- 🔴 Blocked: [What's waiting]

### Last Session Summary
- What accomplished: [Bullet list]
- What learned: [Key insights]
- What's next (prioritized):
  1. [Highest priority with time estimate]
  2. [Medium priority]
  3. [Low priority]

---

## Current Work Context

### Essential Files Changed
- [path/file1] - [What changed, why it matters]
- [path/file2] - [What changed, why it matters]

### Recent Decisions
- [Decision made] - [Why] - [Impact]

---

## For Next Session

### Before Starting Work
- [ ] Read this file (5 minutes)
- [ ] Check git status
- [ ] Review last commit
- [ ] Run pre-work checklist

### After This Session
- [ ] Update "Last Updated" timestamp
- [ ] Add what accomplished
- [ ] Update "What's Next"
- [ ] Commit changes
```

**Update Frequency**: After every work session (minimum once per day when working).

**Enforcement**:
- Pre-commit hook: Warns if SESSION_HANDOFF.md not modified in 2+ hours
- Manual: Checklist reminder at end of session

---

### Principle V: Repository Cleanliness from Day 1

**Rules**:

1. **Never Commit Build Artifacts**
   - ❌ `/build`, `/dist`, `/.next`, `/.docusaurus`
   - ❌ `/node_modules`, `/venv`
   - ❌ Compiled files
   - ✅ Add to `.gitignore` BEFORE first commit

2. **Never Commit Secrets**
   - ❌ `.env`, `.env.local`
   - ❌ API keys, passwords, tokens
   - ✅ Create `.env.example` (committed)
   - ✅ Add `.env*` to `.gitignore`

3. **Keep Documentation Organized**
   - ❌ 23+ markdown files at root
   - ✅ All docs in `docs/` subdirectories
   - ✅ Only README.md, CLAUDE.md, CONSTITUTION.md at root

4. **No Duplicate Specifications**
   - ❌ `specs/authentication/` AND `specs/001-authentication/`
   - ✅ Single source of truth: `specs/002-authentication/`

5. **Delete Merged Branches**
   - After PR merged, delete feature branch
   - Keep only `main` and active feature branches

**Enforcement**:
- Pre-commit hook: Blocks build artifacts, secrets, large files
- Weekly cleanup script: Organizes docs, deletes merged branches

---

### Principle VI: Spec-Driven Development (AI Writes Code)

**Rule**: Human writes specs **via SpecKit commands**. AI (Claude Code) implements from specs.

**Process** (Using SpecKit Commands):

1. **Create Specification** (via `/sp.specify`):
   ```bash
   # Run the SpecKit specify command
   /sp.specify "Phase I console todo app with 5 basic operations"

   # This creates: specs/phase-1/spec.md using the template
   ```

2. **Create Implementation Plan** (via `/sp.plan`):
   ```bash
   # Run the SpecKit plan command
   /sp.plan

   # This creates: specs/phase-1/plan.md with architecture decisions
   ```

3. **Generate Task List** (via `/sp.tasks`):
   ```bash
   # Run the SpecKit tasks command
   /sp.tasks

   # This creates: specs/phase-1/tasks.md with actionable items
   ```

4. **Ask Claude to Implement**:
   ```
   You: @specs/phase-1/spec.md
   Please implement the task CRUD operations as specified.
   Use Python 3.13, UV, and clean code principles.
   ```

5. **Claude Reads Spec and Generates Code**:
   - Claude reads spec
   - Generates Python code in `backend/src/`
   - Follows spec exactly

6. **Test Result**:
   ```bash
   uv run python backend/src/main.py
   # Test all 5 operations
   ```

7. **If Wrong**:
   - **DO NOT** manually edit code
   - **DO** update spec using `/sp.specify` or `/sp.clarify`
   - Ask Claude to re-implement from updated spec

8. **Repeat Until Correct**

9. **Capstone (Validation & Completion)**:
   - Create `capstone.md` in feature spec folder
   - Validate against Spec (all FRs met)
   - Validate against Plan (structure matches)
   - Validate against Constitution (principles followed)
   - Complete checklist and retrospective
   - Mark feature as complete

**MANDATORY SpecKit Commands**:
- `/sp.constitution` - Create/update this constitution
- `/sp.specify` - Create feature specifications
- `/sp.plan` - Create implementation plans
- `/sp.tasks` - Generate task lists
- `/sp.clarify` - Clarify ambiguities in specs
- `/sp.analyze` - Check cross-artifact consistency
- `/sp.adr` - Record architectural decisions
- `/sp.phr` - Record prompt history

**Prohibited**:
- ❌ Manually writing implementation code
- ❌ Editing generated code (except when fixing bugs Claude can't)
- ❌ Creating specs manually with `vim specs/...` (MUST use `/sp.specify`)
- ❌ Creating plans manually (MUST use `/sp.plan`)
- ❌ Creating tasks manually (MUST use `/sp.tasks`)

**Allowed**:
- ✅ Using SpecKit `/sp.*` commands for all specs/plans/tasks
- ✅ Writing configs (CLAUDE.md, .gitignore, etc.)
- ✅ Writing documentation
- ✅ Bug fixes when AI is blocked

---

### Principle VII: Value-Driven Feature Development

**Rule**: Only implement features that deliver value **RIGHT NOW**, not theoretically.

**Feature Necessity Test** (Run before starting any feature):

```markdown
# Feature: [Name]

## Necessity Test (ALL must be YES)

1. **Phase Alignment**: Is this in current phase spec?
   - [ ] YES - This is Phase [N] feature
   - [ ] NO - This is Phase [M] feature (defer)

2. **Dependency Met**: Do I have prerequisites?
   - [ ] YES - All dependencies exist
   - [ ] NO - Missing [dependency] (defer)

3. **Value Now**: Does this deliver value with current functionality?
   - [ ] YES - Works with what exists
   - [ ] NO - Needs future functionality (defer)

4. **Spec Defined**: Is this specified?
   - [ ] YES - In specs/phase-[N]/
   - [ ] NO - Not specified (write spec first)

## Decision

If ANY answer is NO: **DEFER THIS FEATURE**

Proceed only if **ALL are YES**.
```

**Examples**:

- ✅ Phase I: Add Task operation → YES (Basic feature, Phase I)
- ❌ Phase I: Kafka integration → NO (Kafka is Phase V)
- ✅ Phase II: Better Auth → YES (Authentication is Phase II)
- ❌ Phase II: MCP tools → NO (MCP is Phase III)
- ✅ Phase III: Chat endpoint → YES (Chatbot is Phase III)
- ❌ Phase III: Kubernetes → NO (K8s is Phase IV)

**Enforcement**:
- Manual: Run Feature Necessity Test before starting
- AI reminder: Claude asks "Is this in current phase spec?"

---

### Principle VIII: Quality Over Speed (But Achieve Both)

**Rule**: Each phase must be production-ready for its level.

**Production-Ready Means**:
- Code works as specified
- Tests pass (if tests required)
- Documentation complete
- Deployed (if deployment required)
- No known critical bugs
- Demo-able

**Not Production-Ready**:
- ❌ "Works on my machine"
- ❌ "Has some bugs but mostly works"
- ❌ "Need to add tests later"
- ❌ "Documentation TODO"

**Time Management**:
- **Available**: 7 days per phase × 20-30 hours/week ≈ 20-30 hours per phase
- **Phase I**: ~10-15 hours (console app is simple)
- **Phase II**: ~20-25 hours (web app is moderate)
- **Phase III**: ~25-30 hours (AI integration is complex)
- **Phase IV**: ~15-20 hours (K8s packaging, not new features)
- **Phase V**: ~30-40 hours (advanced features + cloud)

**If Running Behind**: Cut scope within phase, don't cut quality.

**Example**:
- ✅ Right: Phase V - implement recurring tasks but not voice commands (stay within scope)
- ❌ Wrong: Phase V - implement everything but with bugs (sacrifices quality)

---

## Phase-Specific Rules

### Phase I: In-Memory Python Console App (Dec 1-7)

**Objective**: Build Basic Level todo CLI with in-memory storage.

**Technology Stack**:
- Python 3.13+
- UV (package manager)
- Claude Code + Spec-Kit Plus

**Features** (Basic Level Only):
1. Add Task (title, description)
2. Delete Task (by ID)
3. Update Task (modify title/description)
4. View Task List (all tasks with status)
5. Mark Complete (toggle completion)

**Explicit Non-Goals** (DO NOT IMPLEMENT):
- ❌ Database (No PostgreSQL, SQLite, nothing)
- ❌ Web UI (No FastAPI, Next.js)
- ❌ Authentication (No users)
- ❌ AI/MCP (No chatbot)
- ❌ Intermediate/Advanced features (No priorities, tags, recurring tasks)

**Deliverables**:
- [ ] `specs/phase-1/` folder with specification
- [ ] `backend/src/` with Python implementation
- [ ] `README.md` with setup instructions
- [ ] `CLAUDE.md` with project context
- [ ] Demo video (< 90 seconds)
- [ ] GitHub repo public
- [ ] Submitted via form

**Time Budget**: 10-15 hours (Dec 1-7)

**Phase I Complete Checklist**:
- [ ] All 5 operations work in one run
- [ ] Clean Python code (no code smells)
- [ ] README instructions work for new user
- [ ] CLAUDE.md provides context for Claude
- [ ] Specs written and code matches specs
- [ ] Demo video recorded
- [ ] Submitted before Dec 7, 11:59 PM

**Phase Gate**: Run `scripts/check-phase-1-complete.sh` before starting Phase II.

---

### Phase II: Full-Stack Web Application (Dec 8-14)

**Objective**: Transform console app into multi-user web app with persistent storage.

**Technology Stack**:
- Frontend: Next.js 16+ (App Router)
- Backend: FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Auth: Better Auth (JWT for API)
- Deployment: Vercel (frontend), public backend URL

**Features** (Basic Level in Web):
1. All 5 Basic features from Phase I (now in web UI)
2. RESTful API endpoints
3. User authentication (signup/signin)
4. Multi-user task ownership (JWT isolation)

**Explicit Non-Goals**:
- ❌ AI chatbot (Phase III)
- ❌ MCP tools (Phase III)
- ❌ Kubernetes (Phase IV)
- ❌ Kafka/Dapr (Phase V)
- ❌ Intermediate/Advanced features (Phase V)

**New Concepts** (MUST READ DOCS FIRST):
- Better Auth (30 min reading): https://www.better-auth.com/docs
- Neon (15 min reading): https://neon.tech/docs
- FastAPI (30 min reading): https://fastapi.tiangolo.com/
- Next.js App Router (45 min reading): https://nextjs.org/docs

**Deliverables**:
- [ ] `specs/phase-2/` folder with specs
- [ ] `frontend/` with Next.js code
- [ ] `backend/` with FastAPI code
- [ ] API endpoints working (GET/POST/PUT/DELETE/PATCH)
- [ ] Better Auth signup/signin working
- [ ] JWT token verification working
- [ ] Multi-user isolation working
- [ ] Deployed on Vercel
- [ ] Demo video (< 90 seconds)
- [ ] Submitted via form

**Time Budget**: 20-25 hours (Dec 8-14)

**Critical: Better Auth**:
- **MUST** run official CLI: `npx @better-auth/cli migrate`
- **DO NOT** manually create schema (learned from previous project)
- **READ DOCS** for 30 minutes before implementing
- Save 6-8 hours debugging

**Phase II Complete Checklist**:
- [ ] Web UI deployed and accessible
- [ ] Backend API deployed and accessible
- [ ] User can signup, signin, logout
- [ ] JWT tokens working (auth header)
- [ ] User A cannot see User B's tasks
- [ ] All 5 Basic operations work in UI
- [ ] Demo video recorded
- [ ] Submitted before Dec 14, 11:59 PM

**Phase Gate**: Run `scripts/check-phase-2-complete.sh` before starting Phase III.

---

### Phase III: AI-Powered Todo Chatbot (Dec 15-21)

**Objective**: Add conversational interface using OpenAI Agents SDK and MCP tools.

**Technology Stack**:
- Frontend: OpenAI ChatKit
- Backend: Python FastAPI (existing)
- AI: OpenAI Agents SDK
- MCP: Official MCP Python SDK
- Database: Neon PostgreSQL (existing)
- Auth: Better Auth JWT (existing)

**Features**:
1. Conversational interface for all Basic operations
2. MCP server with 5 tools (add/list/update/delete/complete tasks)
3. Stateless chat endpoint (`POST /api/{user_id}/chat`)
4. Conversation persistence (conversations & messages tables)
5. Natural language task management

**Explicit Non-Goals**:
- ❌ Kubernetes deployment (Phase IV)
- ❌ Kafka/Dapr (Phase V)
- ❌ Intermediate/Advanced features (Phase V)

**New Concepts** (MUST READ DOCS FIRST):
- OpenAI Agents SDK (45 min reading): https://platform.openai.com/docs/guides/agents
- MCP SDK (60 min reading): https://github.com/modelcontextprotocol/python-sdk
- ChatKit (30 min reading): https://platform.openai.com/docs/guides/chatkit

**Architecture**:
```
ChatKit UI → /api/{user_id}/chat → Agent + Runner → MCP Tools → Database
                                    ↓
                              Conversation/Message tables
```

**MCP Tools** (5 required):
1. `add_task` (user_id, title, description)
2. `list_tasks` (user_id, status filter)
3. `update_task` (user_id, task_id, title?, description?)
4. `delete_task` (user_id, task_id)
5. `complete_task` (user_id, task_id)

**Deliverables**:
- [ ] `specs/phase-3/` folder with specs
- [ ] MCP server implementation (`backend/mcp_server/`)
- [ ] Chat endpoint (`POST /api/{user_id}/chat`)
- [ ] Conversation & Message models (database)
- [ ] ChatKit UI integrated
- [ ] Natural language commands working
- [ ] Stateless server (all state in DB)
- [ ] Demo video (< 90 seconds)
- [ ] Submitted via form

**Time Budget**: 25-30 hours (Dec 15-21)

**Phase III Complete Checklist**:
- [ ] ChatKit UI deployed and working
- [ ] Can send messages and get AI responses
- [ ] Natural language commands execute tasks:
  - "Add a task to buy groceries"
  - "Show me all my tasks"
  - "Mark task 3 as complete"
  - "Delete the meeting task"
- [ ] Conversation history persists
- [ ] Server restarts don't lose conversation state
- [ ] All 5 MCP tools working
- [ ] Demo video recorded
- [ ] Submitted before Dec 21, 11:59 PM

**Phase Gate**: Run `scripts/check-phase-3-complete.sh` before starting Phase IV.

---

### Phase IV: Local Kubernetes Deployment (Dec 22 - Jan 4)

**Objective**: Deploy Phase III app on local Minikube using Helm charts.

**Technology Stack**:
- Docker / Docker Desktop
- Docker AI Agent (Gordon) - if available in region
- Kubernetes: Minikube
- Helm Charts
- AI DevOps: kubectl-ai, kagent

**Scope**:
- **NO NEW FEATURES** - just packaging Phase III app
- Containerize frontend and backend
- Create Helm charts
- Deploy on Minikube
- Demonstrate kubectl-ai and/or kagent usage

**Explicit Non-Goals**:
- ❌ Kafka (Phase V)
- ❌ Dapr (Phase V)
- ❌ DigitalOcean Kubernetes (Phase V)
- ❌ New domain features

**New Concepts** (MUST READ DOCS FIRST):
- Docker (45 min reading): https://docs.docker.com/get-started/
- Kubernetes basics (60 min reading): https://kubernetes.io/docs/tutorials/
- Minikube (30 min reading): https://minikube.sigs.k8s.io/docs/start/
- Helm (45 min reading): https://helm.sh/docs/intro/quickstart/
- kubectl-ai (20 min reading): https://github.com/GoogleCloudPlatform/kubectl-ai
- kagent (20 min reading): https://github.com/kagent-dev/kagent

**Deliverables**:
- [ ] `specs/phase-4/` folder with specs
- [ ] `Dockerfile` for frontend
- [ ] `Dockerfile` for backend
- [ ] `helm/` directory with Helm charts
- [ ] `docs/deployment/minikube-guide.md`
- [ ] Working deployment on Minikube
- [ ] kubectl-ai or kagent usage demonstrated
- [ ] Demo video (< 90 seconds)
- [ ] Submitted via form

**Time Budget**: 15-20 hours (Dec 22 - Jan 4)

**Docker AI Agent (Gordon)** (if available):
```bash
# Use Gordon for intelligent Docker operations
docker ai "What can you do?"
docker ai "Build a Docker image for my Next.js app"
docker ai "Optimize my Dockerfile for production"
```

**kubectl-ai / kagent Usage**:
```bash
# Using kubectl-ai
kubectl-ai "deploy the todo frontend with 2 replicas"
kubectl-ai "check why the pods are failing"

# Using kagent
kagent "analyze the cluster health"
kagent "optimize resource allocation"
```

**Phase IV Complete Checklist**:
- [ ] Docker images built for frontend and backend
- [ ] Helm charts created
- [ ] Minikube started and accessible
- [ ] Helm install successful
- [ ] Pods running (kubectl get pods shows Running)
- [ ] Application accessible on localhost
- [ ] All Phase III features working same as before
- [ ] kubectl-ai or kagent usage documented
- [ ] Demo video recorded
- [ ] Submitted before Jan 4, 11:59 PM

**Phase Gate**: Run `scripts/check-phase-4-complete.sh` before starting Phase V.

---

### Phase V: Advanced Cloud Deployment (Jan 5-18)

**Objective**: Deploy to DOKS with Kafka + Dapr, add Intermediate + Advanced features.

**Technology Stack**:
- Cloud: DigitalOcean Kubernetes (DOKS)
- Event Bus: Kafka (Redpanda Cloud recommended)
- Dapr: Full stack (Pub/Sub, State, Bindings, Secrets, Service Invocation)
- CI/CD: GitHub Actions
- Monitoring: (optional for bonus)

**New Domain Features**:

**Intermediate Level**:
1. Priorities (high/medium/low)
2. Tags/Categories
3. Search & Filter
4. Sort Tasks

**Advanced Level**:
1. Recurring Tasks (auto-reschedule)
2. Due Dates & Time Reminders

**Event-Driven Architecture**:
- Kafka topics: `task-events`, `reminders`, `task-updates`
- Dapr pub/sub for Kafka abstraction
- Dapr state store for conversation state
- Dapr bindings (cron) for reminder checks
- Dapr secrets for API keys

**Explicit Non-Goals**:
- ❌ Voice commands (bonus feature, implement if time)
- ❌ Urdu support (bonus feature, implement if time)

**New Concepts** (MUST READ DOCS FIRST):
- DigitalOcean Kubernetes (45 min reading): https://docs.digitalocean.com/products/kubernetes/
- Redpanda Cloud (30 min reading): https://docs.redpanda.com/
- Dapr (90 min reading): https://docs.dapr.io/getting-started/
- Kafka concepts (45 min reading): https://kafka.apache.org/intro

**Architecture**:
```
DOKS Cluster
├── Frontend Pod (+ Dapr sidecar)
├── Backend Pod (+ Dapr sidecar)
├── Notification Service Pod (+ Dapr sidecar)
├── Recurring Task Service Pod (+ Dapr sidecar)
└── Dapr Components
    ├── kafka-pubsub (Redpanda Cloud)
    ├── statestore (Neon PostgreSQL)
    ├── reminder-cron (bindings)
    └── secretstores (Kubernetes secrets)
```

**Deliverables**:
- [ ] `specs/phase-5/` folder with specs
- [ ] Intermediate features implemented
- [ ] Advanced features implemented
- [ ] Kafka topics created (Redpanda Cloud)
- [ ] Dapr components configured
- [ ] DOKS cluster deployed
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Monitoring configured (optional)
- [ ] Demo video (< 90 seconds)
- [ ] Submitted via form

**Time Budget**: 30-40 hours (Jan 5-18)

**DigitalOcean Setup**:
1. Sign up at digitalocean.com (new accounts get $200 credit for 60 days)
2. Create DOKS cluster (small nodes okay)
3. Configure kubectl to connect to DOKS
4. Deploy using Helm charts from Phase IV

**Redpanda Cloud Setup**:
1. Sign up at redpanda.com/cloud
2. Create Serverless cluster (free tier)
3. Create topics: `task-events`, `reminders`, `task-updates`
4. Get bootstrap server URL and credentials
5. Configure Dapr pubsub component

**Dapr Components**:
```yaml
# kafka-pubsub.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "your-redpanda-url:9092"
    - name: authType
      value: "password"
    - name: saslUsername
      value: "your-username"
    - name: saslPassword
      secretKeyRef:
        name: kafka-secret
        key: password
```

**Phase V Complete Checklist**:
- [ ] All Intermediate features working (priorities, tags, search, sort)
- [ ] All Advanced features working (recurring tasks, due dates, reminders)
- [ ] Kafka topics created and events flowing
- [ ] Dapr pub/sub working (events published/consumed)
- [ ] Dapr state store working (conversation state)
- [ ] Dapr cron binding working (reminder checks)
- [ ] DOKS cluster deployed and accessible
- [ ] CI/CD pipeline working (push to main → deploy)
- [ ] Demo video recorded
- [ ] Submitted before Jan 18, 11:59 PM

**Bonus Features** (if time permits):
- [ ] Urdu language support (+100 points)
- [ ] Voice commands (+200 points)
- [ ] Reusable intelligence (subagents/skills) (+200 points)
- [ ] Cloud-Native blueprints (+200 points)

**Phase Gate**: Run `scripts/check-phase-5-complete.sh` to verify all complete.

---

## Enforcement Mechanisms

### Level 1: Automated Checks (Prevent Violations)

#### Pre-Commit Hook (`.git/hooks/pre-commit`)

```bash
#!/bin/bash
# .git/hooks/pre-commit
# Prevents constitutional violations

echo "🔒 Running pre-commit constitutional checks..."

# Check 1: No build artifacts
if git diff --cached --name-only | grep -E "^build/|^dist/|^\.next/|^\.docusaurus/|^node_modules/"; then
    echo "❌ BLOCKED: Attempting to commit build artifacts"
    echo "These files should not be in version control:"
    git diff --cached --name-only | grep -E "^build/|^dist/|^\.next/|^\.docusaurus/|^node_modules/"
    echo ""
    echo "Fix: Add to .gitignore and remove from commit"
    exit 1
fi

# Check 2: No secrets
if git diff --cached --name-only | grep -E "\.env$|\.env\.local$"; then
    echo "❌ BLOCKED: Attempting to commit environment files"
    echo "These files contain secrets and should not be committed"
    exit 1
fi

# Check 3: Large files
LARGE_FILES=$(git diff --cached --name-only | xargs -I {} du -k {} 2>/dev/null | awk '$1 > 1024 {print $2}')
if [ -n "$LARGE_FILES" ]; then
    echo "⚠️  WARNING: Large files detected (>1MB)"
    echo "$LARGE_FILES"
    read -p "Continue anyway? (yes/no): " CONTINUE
    if [ "$CONTINUE" != "yes" ]; then
        exit 1
    fi
fi

# Check 4: SESSION_HANDOFF updated recently
HANDOFF_FILE="docs/SESSION_HANDOFF.md"
if [ -f "$HANDOFF_FILE" ]; then
    LAST_MODIFIED=$(stat -c %Y "$HANDOFF_FILE" 2>/dev/null || stat -f %m "$HANDOFF_FILE" 2>/dev/null)
    CURRENT_TIME=$(date +%s)
    TIME_DIFF=$((CURRENT_TIME - LAST_MODIFIED))

    if [ "$TIME_DIFF" -gt 7200 ]; then  # 2 hours
        echo "⚠️  WARNING: SESSION_HANDOFF.md not updated in 2+ hours"
        echo "Have you updated the session handoff?"
        read -p "Continue without updating? (yes/no): " CONTINUE
        if [ "$CONTINUE" != "yes" ]; then
            exit 1
        fi
    fi
fi

echo "✅ Pre-commit checks passed"
exit 0
```

**Installation**:
```bash
# Make executable
chmod +x .git/hooks/pre-commit
```

---

#### Phase Gate Scripts

**Phase I → Phase II Gate** (`scripts/check-phase-1-complete.sh`):

```bash
#!/bin/bash
# scripts/check-phase-1-complete.sh
# Blocks Phase II start until Phase I is 100% complete

echo "🚪 Phase I → Phase II Gate Check"
echo ""

PHASE_1_COMPLETE=true

# Check 1: Specs exist
if [ ! -d "specs/phase-1" ]; then
    echo "❌ Missing: specs/phase-1/ directory"
    PHASE_1_COMPLETE=false
fi

# Check 2: Python source exists
if [ ! -d "backend/src" ]; then
    echo "❌ Missing: backend/src/ directory"
    PHASE_1_COMPLETE=false
fi

# Check 3: README exists
if [ ! -f "README.md" ]; then
    echo "❌ Missing: README.md"
    PHASE_1_COMPLETE=false
fi

# Check 4: CLAUDE.md exists
if [ ! -f "CLAUDE.md" ]; then
    echo "❌ Missing: CLAUDE.md"
    PHASE_1_COMPLETE=false
fi

# Check 5: Demo video mentioned in README
if ! grep -q "demo" README.md; then
    echo "⚠️  Warning: No demo video link in README.md"
fi

# Check 6: GitHub repo is public
if [ -d ".git" ]; then
    REMOTE=$(git remote get-url origin 2>/dev/null)
    if [ -z "$REMOTE" ]; then
        echo "⚠️  Warning: No git remote configured"
    fi
else
    echo "❌ Missing: .git directory (not a git repo)"
    PHASE_1_COMPLETE=false
fi

# Check 7: Submission form completed
echo ""
echo "📝 Manual Checks (verify yourself):"
echo "  [ ] All 5 Basic operations work (Add, Delete, Update, View, Mark Complete)"
echo "  [ ] Demo video recorded (< 90 seconds)"
echo "  [ ] Form submitted at https://forms.gle/CQsSEGM3GeCrL43c8"
echo ""

if [ "$PHASE_1_COMPLETE" = false ]; then
    echo "❌ GATE FAILED: Phase I is not complete"
    echo "Complete all checks above before starting Phase II"
    exit 1
else
    echo "✅ GATE PASSED: Phase I appears complete"
    echo ""
    echo "Proceed to Phase II only after manual checks completed"
    exit 0
fi
```

**Similar scripts for Phase II→III, III→IV, IV→V gates.**

---

#### Feature Necessity Check (`scripts/check-feature-necessity.sh`)

```bash
#!/bin/bash
# scripts/check-feature-necessity.sh
# Interactive checklist before starting new feature

echo "🎯 Feature Necessity Test"
echo ""
echo "Feature Name: "
read FEATURE_NAME
echo ""

echo "Answer YES/NO for each question:"
echo ""

echo "1. Phase Alignment: Is this in current phase spec?"
read -p "   Answer: " Q1
echo ""

echo "2. Dependency Met: Do I have all prerequisites?"
read -p "   Answer: " Q2
echo ""

echo "3. Value Now: Does this deliver value with current functionality?"
read -p "   Answer: " Q3
echo ""

echo "4. Spec Defined: Is this specified in specs/ folder?"
read -p "   Answer: " Q4
echo ""

# Check if all YES
if [[ "$Q1" =~ ^[Yy]$ ]] && [[ "$Q2" =~ ^[Yy]$ ]] && [[ "$Q3" =~ ^[Yy]$ ]] && [[ "$Q4" =~ ^[Yy]$ ]]; then
    echo "✅ PROCEED: All checks passed"
    echo "Feature '$FEATURE_NAME' is necessary and ready to implement"
    exit 0
else
    echo "❌ DEFER: One or more checks failed"
    echo "Feature '$FEATURE_NAME' should be deferred"
    echo ""
    echo "Recommended action:"
    if [[ ! "$Q1" =~ ^[Yy]$ ]]; then
        echo "  - Wait until correct phase"
    fi
    if [[ ! "$Q2" =~ ^[Yy]$ ]]; then
        echo "  - Implement missing dependencies first"
    fi
    if [[ ! "$Q3" =~ ^[Yy]$ ]]; then
        echo "  - Wait until prerequisite features exist"
    fi
    if [[ ! "$Q4" =~ ^[Yy]$ ]]; then
        echo "  - Write specification first"
    fi
    exit 1
fi
```

---

### Level 2: Manual Checklists (Human Verification)

#### Daily Pre-Work Checklist (`docs/DAILY_CHECKLIST.md`)

```markdown
# Daily Pre-Work Checklist

Run this checklist BEFORE starting work each day.

## Session Start

**Date**: [Today's date]
**Phase**: [I/II/III/IV/V]
**Time Available**: [Hours]

---

## 1. Context Loading (5-10 minutes)

- [ ] Read `docs/SESSION_HANDOFF.md` (5 min)
- [ ] Check git status for uncommitted changes
- [ ] Review last commit message
- [ ] Check for new issues/PRs (if team project)

---

## 2. Constitutional Review (2-3 minutes)

- [ ] What phase am I in? [Phase number]
- [ ] Is previous work 100% complete? [Yes/No]
- [ ] If No: Finish previous work before starting new work
- [ ] Am I following the phase-specific rules? [Yes/No]

---

## 3. Plan Check (2-3 minutes)

- [ ] What am I working on today? [Task name]
- [ ] Is this in current phase spec? [Yes/No]
- [ ] Do I have all dependencies? [Yes/No]
- [ ] Estimated time: [Hours]

---

## 4. Tool Check (if using new tool today)

- [ ] New tool: [Tool name, or "None"]
- [ ] If new tool: Read documentation first (30 min)
- [ ] Run `docs/BEFORE_NEW_TOOL.md` checklist

---

## 5. Ready to Start

- [ ] All checks above completed
- [ ] Clear goal for today
- [ ] Time blocked on calendar

**Ready**: [Yes/No]

If No, resolve blockers before starting.
If Yes, start working!

---

## Session End (After Work)

- [ ] Update `docs/SESSION_HANDOFF.md` (5 min)
- [ ] Commit changes with clear message
- [ ] Mark today's work in progress tracker
- [ ] Plan tomorrow's work (top 3 priorities)
```

---

#### Before New Tool Checklist (`docs/BEFORE_NEW_TOOL.md`)

```markdown
# Before Using New Tool Checklist

Tool: _______________
Date: [Date]

---

## Research Phase (30 minutes minimum)

- [ ] Read official quick start guide (10 min)
      URL: _______________
      Key takeaways: _______________

- [ ] Check version compatibility (5 min)
      My versions: _______________
      Compatible: [Yes/No]

- [ ] Review "Troubleshooting" or "Common Issues" (5 min)
      Common issues: _______________

- [ ] Read API reference for features I'll use (10 min)
      Features needed: _______________
      How to use: _______________

- [ ] Check GitHub issues for recent problems (5 min)
      Recent issues: _______________
      Workarounds: _______________

**Total Time**: _____ minutes (minimum 30)

---

## Implementation Phase

- [ ] Start with official example/template
      Example URL: _______________

- [ ] Test in isolation before integrating
      Test result: _______________

- [ ] Document any deviations from docs
      Deviations: _______________

---

## If Stuck After 30 Minutes

- [ ] Re-read documentation (don't assume I understood)
- [ ] Search official GitHub issues
- [ ] Ask in official community/Discord
- [ ] Only then: Debug on my own

---

**Lesson from Previous Project**:
Skipping this checklist for better-auth cost 6-8 hours debugging.
30 minutes reading > 6 hours debugging.
```

---

### Level 3: AI Agent Reminders (Claude Code Integration)

#### Principle IX: Reusable Intelligence Transparency

**Rule**: Claude MUST be transparent about which Reusable Intelligence artifacts are being used and MUST proactively suggest updates when new knowledge is discovered.

**Claude's Transparency Requirements**:

1. **Announce Before Tasks**: Before performing any significant task, Claude MUST state which agents, subagents, and/or skills are being utilized.

   Example:
   ```
   📋 Using: backend-service agent, api-endpoint-implementer subagent, neon-sqlmodel skill

   I'm about to implement the task list endpoint...
   ```

2. **Proactively Suggest Updates**: When Claude discovers new patterns, learns something reusable, or identifies gaps in existing knowledge artifacts, Claude MUST ask the user if they want to update the relevant artifact.

   Example:
   ```
   💡 Knowledge Update Opportunity

   I just discovered that SQLite requires StaticPool with check_same_thread=False
   for FastAPI testing.

   This pattern should be added to:
   - `.claude/skills/neon-sqlmodel.md` (testing section)
   - `.claude/subagents/test-generator.md` (database test patterns)

   Would you like me to update these artifacts?
   ```

3. **Request Before Modification**: Claude MUST NOT modify any Reusable Intelligence artifact (agents, subagents, skills, constitution) without explicit user approval.

**User's Role**:
- Review Claude's suggestions for relevance
- Approve or reject knowledge updates
- Trigger formal updates via `/sp.*` commands when appropriate

**Enforcement**: Claude will include artifact usage in task responses and prompt for updates when new knowledge emerges.

---

**Instructions for Claude Code** (added to `CLAUDE.md`):

```markdown
# Constitutional Enforcement for Claude Code

You are Claude Code working on the Evolution of Todo project.

## Your Constitutional Duties

### 1. Phase Boundary Guardian

Before implementing ANY feature, ask:

**"What phase are we in?"**

- If Phase I: Only implement console app features (no DB, no web, no AI)
- If Phase II: Only implement web app features (no AI, no K8s)
- If Phase III: Only implement AI features (no K8s, no Kafka)
- If Phase IV: Only implement K8s packaging (no new features)
- If Phase V: Only implement advanced features + Kafka/Dapr

**If user requests Phase N+1 feature while in Phase N:**

Response:
```
⚠️ Constitutional Alert: Phase Boundary Violation

You're requesting [Feature X] which is a Phase [N+1] feature.
We're currently in Phase [N].

Current phase rules:
- [List Phase N allowed features]
- [List Phase N prohibited features]

Recommended actions:
1. Complete Phase [N] first (run scripts/check-phase-[N]-complete.sh)
2. Then start Phase [N+1]
3. Then implement [Feature X]

Do you want to:
a) Continue with Phase [N] work
b) Override (document why in WHY.md)
```

### 2. Documentation-First Enforcer

Before implementing with a NEW tool, ask:

**"Have you read the documentation for [tool]?"**

If user says No:

Response:
```
⚠️ Constitutional Alert: Documentation-First Principle

You're about to use [Tool] without reading documentation.

Lesson from previous project:
- Skipped better-auth docs → 6-8 hours wasted debugging

Required reading (30 min):
- Quick start guide: [URL]
- Common issues: [URL]
- API reference: [URL]

Please complete docs/BEFORE_NEW_TOOL.md checklist first.

Estimated time saved: 6+ hours
```

### 3. Context Preservation Reminder

At end of implementation, remind:

**"Don't forget to update SESSION_HANDOFF.md"**

Response:
```
✅ Task Complete

Before ending this session:
- [ ] Update docs/SESSION_HANDOFF.md (5 min)
- [ ] Commit changes
- [ ] Mark task complete in progress tracker

Cost of skipping: 30-60 min next session reloading context
Time to update: 5 minutes
ROI: 6-12x return
```

### 4. Feature Necessity Checker

Before starting a new feature, ask:

**"Is this feature in the current phase spec?"**

If unclear:

Response:
```
⚠️ Constitutional Alert: Feature Necessity Test

Before implementing [Feature]:

Run: scripts/check-feature-necessity.sh

Questions to verify:
1. Is this in current phase spec?
2. Do I have all dependencies?
3. Does this deliver value NOW?
4. Is this specified?

Proceed only if ALL are YES.
```

### 5. One Thing at a Time Enforcer

If user starts new feature while previous incomplete, ask:

**"Is the previous task 100% complete?"**

Response:
```
⚠️ Constitutional Alert: WIP Limit Exceeded

Current in-progress tasks:
- [Task X] (95% complete)

Rule: Only ONE major task in progress at a time.

95% complete = 0% value delivered.

Please:
1. Finish [Task X] to 100%
2. Deploy and verify working
3. Then start new task

Definition of 100%:
- Code merged
- Deployed
- Tested
- Documented
- No blockers
```

---

## Your Role

You are not just a code generator. You are a **constitutional guardian**.

Your job:
1. Generate high-quality code from specs ✅
2. Enforce constitutional principles ✅
3. Remind human of rules when they deviate ✅
4. Ask clarifying questions ✅
5. Prevent past mistakes from repeating ✅

**Be firm but respectful when enforcing rules.**

Human can override, but must explicitly acknowledge violation.
```

---

## Repository Structure & Hygiene

### Directory Structure (From Day 1)

```
evolution_to_do/
├── .git/
│   └── hooks/
│       ├── pre-commit              # Automated checks
│       └── pre-push                # Additional checks
│
├── .github/
│   └── workflows/
│       ├── ci.yml                  # Run tests on all branches
│       ├── deploy.yml              # Deploy (manual or on tag)
│       └── phase-gate.yml          # Phase completion checks
│
├── specs/                          # All specifications
│   ├── CONSTITUTION.md             # This document
│   ├── overview.md                 # Project overview
│   ├── phase-1/                    # Phase I specs
│   │   ├── spec.md
│   │   ├── plan.md
│   │   └── tasks.md
│   ├── phase-2/                    # Phase II specs
│   │   ├── spec.md
│   │   ├── plan.md
│   │   └── tasks.md
│   ├── phase-3/                    # Phase III specs
│   ├── phase-4/                    # Phase IV specs
│   └── phase-5/                    # Phase V specs
│
├── history/                        # PHRs and ADRs
│   ├── adr/
│   │   └── 0001-[...].md
│   └── prompts/
│       ├── phase-1/
│       ├── phase-2/
│       └── [...]
│
├── docs/                           # All documentation
│   ├── SESSION_HANDOFF.md          # Context preservation (CRITICAL)
│   ├── PROJECT_STATUS.md           # Single source of truth
│   ├── DAILY_CHECKLIST.md          # Daily pre-work checklist
│   ├── BEFORE_NEW_TOOL.md          # Documentation-first checklist
│   ├── deployment/
│   │   ├── phase-2-vercel.md
│   │   ├── phase-4-minikube.md
│   │   └── phase-5-doks.md
│   └── development/
│       ├── phase-1-guide.md
│       ├── phase-2-guide.md
│       └── [...]
│
├── backend/                        # Python backend
│   ├── src/
│   │   ├── main.py                # Entry point
│   │   ├── models.py              # SQLModel models
│   │   ├── routes/                # FastAPI routes
│   │   └── mcp_server/            # MCP tools (Phase III)
│   ├── tests/
│   ├── pyproject.toml             # UV config
│   └── README.md
│
├── frontend/                       # Next.js frontend (Phase II+)
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── public/
│   ├── package.json
│   └── README.md
│
├── docker/                         # Docker configs (Phase IV+)
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
│
├── helm/                           # Helm charts (Phase IV+)
│   └── todo-app/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
│
├── dapr-components/                # Dapr configs (Phase V)
│   ├── kafka-pubsub.yaml
│   ├── statestore.yaml
│   ├── reminder-cron.yaml
│   └── secretstores.yaml
│
├── scripts/                        # Automation scripts
│   ├── check-phase-1-complete.sh
│   ├── check-phase-2-complete.sh
│   ├── check-phase-3-complete.sh
│   ├── check-phase-4-complete.sh
│   ├── check-phase-5-complete.sh
│   ├── check-feature-necessity.sh
│   └── weekly-cleanup.sh
│
├── .gitignore                      # Comprehensive (set up FIRST)
├── .env.example                    # Env vars template (committed)
├── README.md                       # Project overview
├── CLAUDE.md                       # Claude Code instructions
└── QUICK_REFERENCE.md              # Quick commands
```

### Key Principles:

1. **Flat root**: Only essential files at root (README, CLAUDE, CONSTITUTION)
2. **Organized docs**: Everything in `docs/` subdirectories
3. **Specs separated**: One folder per phase
4. **No duplicates**: Single source of truth for everything
5. **Clear separation**: Backend, frontend, deployment separated

---

### .gitignore (Set Up FIRST - Day 1)

```.gitignore
# Build outputs
/build
/dist
/.next
/.docusaurus
/.cache

# Dependencies
/node_modules
/.pnp
.pnp.js
/venv
/__pycache__
*.pyc
.uv/

# Testing
/coverage
/test-results
/.pytest_cache
.nyc_output
*.log

# Environment
.env
.env.local
.env.*.local
!.env.example
.DS_Store

# IDE
.vscode/*
!.vscode/extensions.json
!.vscode/settings.json
.idea
*.swp
*.swo
*~

# OS
Thumbs.db

# TypeScript
*.tsbuildinfo

# Python
*.egg-info/
.eggs/
dist/
.Python

# Temporary
*.tmp
*.temp
.temp/

# Database
*.db
*.sqlite

# Docker
.dockerignore (committed separately)

# Kubernetes
*.kubeconfig

# Secrets
*.pem
*.key
*.crt
```

**CRITICAL**: Create this BEFORE first commit. Once files are tracked, .gitignore won't help.

---

## Daily & Weekly Workflows

### Daily Workflow

**Morning (Session Start)** - 10 minutes:
1. Read `docs/SESSION_HANDOFF.md` (5 min)
2. Run `docs/DAILY_CHECKLIST.md` (3 min)
3. Check phase alignment (2 min)
4. Start working

**During Work** - Continuous:
1. Follow spec exactly
2. If new tool: Read docs first (30 min)
3. If stuck 30 min: Re-read docs
4. Update SESSION_HANDOFF as major milestones complete

**Evening (Session End)** - 10 minutes:
1. Commit changes with clear message
2. Update `docs/SESSION_HANDOFF.md` (5 min)
3. Update `docs/PROJECT_STATUS.md` if major milestone
4. Plan tomorrow's top 3 tasks (3 min)

**Total Overhead**: 20 minutes/day (10% of 3-hour session)
**Time Saved**: 30-60 min next session = Net gain 10-40 min

---

### Weekly Workflow

**Every Friday** - 30 minutes:

1. **Progress Review** (10 min):
   - Run phase completion check script
   - Compare actual vs. planned progress
   - Identify blockers

2. **Repository Cleanup** (10 min):
   - Run `scripts/weekly-cleanup.sh`
   - Delete merged branches
   - Organize new docs into proper folders
   - Check for accidental build artifacts

3. **Planning for Next Week** (10 min):
   - Review hackathon timeline
   - Adjust scope if behind schedule
   - Identify risks

**Weekly Cleanup Script** (`scripts/weekly-cleanup.sh`):

```bash
#!/bin/bash
# scripts/weekly-cleanup.sh
# Weekly repository maintenance

echo "🧹 Weekly Repository Cleanup"
echo ""

# 1. Delete merged branches
echo "1. Checking for merged branches..."
git fetch --prune
MERGED=$(git branch --merged main | grep -v "main" | grep -v "\*")
if [ -n "$MERGED" ]; then
    echo "Found merged branches:"
    echo "$MERGED"
    read -p "Delete these? (yes/no): " DELETE
    if [ "$DELETE" = "yes" ]; then
        echo "$MERGED" | xargs git branch -d
        echo "✅ Deleted merged branches"
    fi
else
    echo "✅ No merged branches to delete"
fi
echo ""

# 2. Check for uncommitted changes
echo "2. Checking for uncommitted changes..."
if [ -n "$(git status --short)" ]; then
    echo "⚠️  Warning: Uncommitted changes found"
    git status --short
    echo "Commit or stash before weekend"
else
    echo "✅ No uncommitted changes"
fi
echo ""

# 3. Check repository size
echo "3. Checking repository size..."
REPO_SIZE=$(du -sh .git | cut -f1)
echo "Repository size: $REPO_SIZE"
if [ $(du -s .git | cut -f1) -gt 100000 ]; then
    echo "⚠️  Warning: Repository larger than 100MB"
    echo "Consider cleaning large files"
fi
echo ""

# 4. Check for docs at root
echo "4. Checking for documentation sprawl..."
ROOT_DOCS=$(ls *.md 2>/dev/null | grep -v "README.md" | grep -v "CLAUDE.md" | grep -v "QUICK_REFERENCE.md")
if [ -n "$ROOT_DOCS" ]; then
    echo "⚠️  Warning: Extra markdown files at root:"
    echo "$ROOT_DOCS"
    echo "Move to docs/ directory"
else
    echo "✅ Root directory clean"
fi
echo ""

# 5. Update PROJECT_STATUS
echo "5. Update PROJECT_STATUS.md"
echo "Last updated: $(grep "Updated:" docs/PROJECT_STATUS.md)"
read -p "Update now? (yes/no): " UPDATE
if [ "$UPDATE" = "yes" ]; then
    vim docs/PROJECT_STATUS.md
fi
echo ""

echo "✅ Weekly cleanup complete"
```

---

## Emergency Protocols

### Protocol 1: Blocked on Technical Issue

**If stuck on technical problem for 30+ minutes:**

1. **STOP** - Don't keep debugging blindly
2. **Re-read Documentation** (15 min)
   - Official docs for the tool causing issue
   - Common issues section
   - GitHub issues search
3. **Check Knowledge Base** (5 min)
   - Do we have notes on this? (docs/troubleshooting/)
   - Did previous project hit this?
4. **Ask for Help** (10 min)
   - Official community/Discord for tool
   - Stack Overflow
   - GitHub issues
5. **Document the Issue** (5 min)
   - Add to docs/troubleshooting/
   - Include error message, what you tried, solution
6. **Move On if Still Blocked** (adjust scope)
   - If critical: Escalate, ask mentor, pay for consultation
   - If non-critical: Defer and continue with other work

**Time Box**: Max 1 hour debugging before seeking help or deferring.

---

### Protocol 2: Spec is Wrong or Incomplete

**If implementing from spec and realize spec has issues:**

1. **STOP Implementation** - Don't continue with bad spec
2. **Document the Issue**:
   - What's wrong/missing?
   - What should it be?
   - Why does this matter?
3. **Update Spec** (don't update code):
   - Fix the spec in `specs/phase-N/`
   - Commit spec change
4. **Ask Claude to Re-Implement** from updated spec
5. **Test Again**

**Never**: Continue implementing knowing spec is wrong.
**Always**: Fix spec first, then implement.

---

### Protocol 3: Running Behind Schedule

**If at risk of missing phase deadline:**

**Option A: Cut Scope (Preferred)**
- Implement core features only
- Defer bonus features
- Example: Phase V - implement recurring tasks, skip voice commands

**Option B: Extend Work Hours (Carefully)**
- If physically possible and healthy
- Don't burn out - hackathon lasts 5 weeks
- Max 40 hours/week recommended

**Option C: Skip Bonus Features**
- Focus on core 5 phases (1000 points)
- Skip bonus features (+600 points)
- Bonus is optional

**Option D: Request Extension (Last Resort)**
- Check hackathon rules
- Contact organizers if genuine emergency
- Document reason

**Never**: Sacrifice quality to hit deadline. Better to submit 4 excellent phases than 5 buggy phases.

---

### Protocol 4: Constitution Violation Detected

**If you catch yourself violating constitution:**

**Immediate Actions**:
1. **STOP** - Don't continue the violation
2. **Acknowledge**: "I am violating Principle X"
3. **Document Why**: Create `WHY.md` explaining:
   - What principle violated?
   - Why did I violate it?
   - Was it intentional or accidental?
   - What's the impact?
   - How to prevent next time?
4. **Choose**:
   - **Option A: Revert** - Undo the violation, follow constitution
   - **Option B: Continue** - Explicitly override constitution with justification
5. **Update Constitution** if rule needs changing

**Example WHY.md**:
```markdown
# Constitutional Violation: [Date]

## Principle Violated
Principle II: Finish One Thing Before Starting Next

## What Happened
Started implementing "Delete Task" while "Add Task" was 95% complete.

## Why
Got excited about Delete feature, thought "Add is almost done".

## Impact
- "Add Task" now 95% (not deployed)
- "Delete Task" now 50% (not deployed)
- Total value delivered: 0%

## Lesson
95% complete = 0% value. Must finish to 100%.

## Action Taken
- Reverted Delete Task work
- Finished Add Task to 100%
- Deployed and verified
- Now starting Delete Task

## Prevention
Added reminder to DAILY_CHECKLIST: "Is previous task 100% done?"
```

---

## Success Metrics

### How to Know You're Succeeding

**Weekly Check** (Every Friday):

#### 1. Phase Completion Rate
- [ ] Phase I: Complete by Dec 7? [Yes/No]
- [ ] Phase II: Complete by Dec 14? [Yes/No]
- [ ] Phase III: Complete by Dec 21? [Yes/No]
- [ ] Phase IV: Complete by Jan 4? [Yes/No]
- [ ] Phase V: Complete by Jan 18? [Yes/No]

**Target**: 100% of phases on time.

#### 2. Constitutional Compliance Rate
- [ ] Followed phase boundaries? [Yes/No]
- [ ] Read docs before new tools? [Yes/No]
- [ ] Updated SESSION_HANDOFF.md daily? [Yes/No]
- [ ] Finished one thing before next? [Yes/No]
- [ ] Repository clean (no build artifacts)? [Yes/No]

**Target**: 100% compliance (or documented exceptions).

#### 3. Efficiency Metrics
- Time spent debugging avoidable issues: _____ hours
- Time spent reloading context: _____ hours
- Time wasted on out-of-phase work: _____ hours
- Total effective work time: _____ hours

**Target**: <10% time wasted (vs. 50% in previous project).

#### 4. Quality Metrics
- [ ] All features work as specified?
- [ ] All tests passing?
- [ ] All phases deployed?
- [ ] Demo videos recorded?
- [ ] Forms submitted on time?

**Target**: 100% quality (no "it mostly works").

#### 5. Point Accumulation
- Phase I: 100 points [Earned/Not Earned]
- Phase II: 150 points [Earned/Not Earned]
- Phase III: 200 points [Earned/Not Earned]
- Phase IV: 250 points [Earned/Not Earned]
- Phase V: 300 points [Earned/Not Earned]
- **Bonus Features**:
  - Reusable Intelligence: +200 [Earned/Not Earned]
  - Cloud-Native Blueprints: +200 [Earned/Not Earned]
  - Urdu Support: +100 [Earned/Not Earned]
  - Voice Commands: +200 [Earned/Not Earned]

**Target**: 1000 points (core) + up to 700 bonus = 1700 max.

---

### Red Flags (Warning Signs)

**If ANY of these occur, invoke emergency protocol:**

1. **Behind Schedule** (2+ days behind on any phase)
2. **Multiple WIP Tasks** (more than 1 major task in progress)
3. **No Context Updates** (SESSION_HANDOFF not updated 2+ days)
4. **Build Artifacts Committed** (pre-commit hook bypassed)
5. **Phase Boundary Violation** (working on Phase N+1 features in Phase N)
6. **Documentation Not Read** (starting tool without 30 min reading)
7. **Efficiency <80%** (more than 20% time wasted)
8. **Quality Issues** (features don't work as specified)

**Action on Red Flag**:
1. Stop immediately
2. Review constitution
3. Identify root cause
4. Correct course
5. Document lesson

---

## Governance

### Constitution Management

**Rule**: This constitution MUST be managed exclusively through SpecKit commands.

**Amendment Process**:

1. **Initiate Amendment** (via `/sp.constitution`):
   ```bash
   # All constitution changes MUST use this command
   /sp.constitution
   ```

2. **Document Changes**:
   - Update Sync Impact Report (HTML comment at top)
   - Increment version number appropriately
   - Document all changes made

3. **Create Traceability** (via `/sp.phr`):
   - Every amendment MUST have a PHR record
   - PHR stored in `history/prompts/constitution/`
   - Links amendment to context and reasoning

### Version Numbering

**Semantic Versioning** (MAJOR.MINOR.PATCH):

- **MAJOR** (X.0.0): Breaking changes to principles or workflow
  - Example: Removing or fundamentally changing a principle
  - Requires explicit justification

- **MINOR** (0.X.0): New guidance or materially expanded sections
  - Example: Adding SpecKit commands integration
  - Example: Adding Governance section

- **PATCH** (0.0.X): Clarifications, typo fixes, formatting
  - Example: Fixing broken links
  - Example: Clarifying ambiguous wording

### Prohibited Actions

- ❌ Manual editing with `vim .specify/memory/constitution.md`
- ❌ Changes without Sync Impact Report update
- ❌ Changes without version bump
- ❌ Changes without PHR documentation
- ❌ Removing principles without MAJOR version bump

### Allowed Actions

- ✅ Amendments via `/sp.constitution` command
- ✅ Adding new sections (MINOR bump)
- ✅ Clarifying existing content (PATCH bump)
- ✅ Updating examples and references (PATCH bump)

### Sync Requirements

**When Constitution Changes**:
1. Update `CLAUDE.md` if it references changed content
2. Update any template that references constitution
3. Run consistency check: `/sp.analyze`

**Sync Impact Report Format** (at top of file):
```html
<!--
================================================================================
SYNC IMPACT REPORT - Constitution v[VERSION] [TITLE]
================================================================================
Date: [DATE]
Version: [OLD] → [NEW] ([BUMP TYPE])
Action: [DESCRIPTION]

VERSION CHANGES:
- Previous Version: [OLD]
- Current Version: [NEW]
- Version Bump Type: [MAJOR/MINOR/PATCH] ([REASON])

CHANGES MADE:
1. [Change 1]
2. [Change 2]
...

FILES UPDATED:
✅ [File 1] - [Status]
✅ [File 2] - [Status]

COMMIT MESSAGE SUGGESTION:
[Suggested commit message]
================================================================================
-->
```

### PHR Requirements for Constitution

**Location**: `history/prompts/constitution/###-[short-name].constitution.prompt.md`

**Required Fields**:
- `id`: Sequential number
- `stage`: "constitution"
- `command`: "/sp.constitution"
- `files_created_or_modified`: Constitution and synced files

**Naming Convention**: `###-[action]-[description].constitution.prompt.md`
- Example: `002-update-constitution-to-v1-1-0-speckit-commands.constitution.prompt.md`
- Example: `003-add-governance-section.constitution.prompt.md`

---

## Final Commitment

**I, [Your Name], commit to following this constitution.**

**Signature**: _____________________
**Date**: December 4, 2025

**This constitution is the contract I make with my future self to succeed in this hackathon by learning from past mistakes and maintaining discipline.**

**Witness (Claude Code)**: I will enforce these principles and remind you when you deviate.

---

## Appendix: Quick Command Reference

### SpecKit Commands (MANDATORY for specs/plans/tasks)

```bash
# Constitution management
/sp.constitution                    # Create/update constitution

# Specification workflow
/sp.specify "feature description"   # Create feature specification
/sp.plan                            # Create implementation plan
/sp.tasks                           # Generate task list
/sp.clarify                         # Clarify spec ambiguities
/sp.analyze                         # Cross-artifact consistency check

# Traceability
/sp.adr "decision title"            # Record architectural decision
/sp.phr                             # Record prompt history

# Git workflow
/sp.git.commit_pr                   # Commit and create PR
```

### Phase Checks

```bash
scripts/check-phase-1-complete.sh
scripts/check-phase-2-complete.sh
scripts/check-phase-3-complete.sh
scripts/check-phase-4-complete.sh
scripts/check-phase-5-complete.sh
```

### Feature Checks

```bash
scripts/check-feature-necessity.sh
```

### Daily Workflow

```bash
# Start session
cat docs/SESSION_HANDOFF.md
cat docs/DAILY_CHECKLIST.md

# End session
vim docs/SESSION_HANDOFF.md
git commit -m "feat: [what you did]"
```

### Weekly Maintenance

```bash
scripts/weekly-cleanup.sh
vim docs/PROJECT_STATUS.md
```

### Emergency

```bash
# If violating constitution
vim WHY.md
git add WHY.md
git commit -m "docs: constitutional override - [reason]"
```

---

**Constitution Version**: 1.3.0
**Last Updated**: 2025-12-10
**Status**: ACTIVE
**Next Review**: After Phase II completion
**SpecKit Integration**: MANDATORY - All specs/plans/tasks via /sp.* commands
**Governance**: Section 11 - All amendments via /sp.constitution command

**Remember**: Excellence is not an act, but a habit. This constitution is the framework for building that habit.

**Let's build something great. 🚀**
