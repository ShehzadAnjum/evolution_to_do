# Reusable Intelligence Reference Guide

**Version**: 1.0.0
**Last Updated**: 2025-12-10
**Project**: Evolution of Todo - Hackathon II

---

## Table of Contents

1. [Overview](#1-overview)
2. [Complete Inventory](#2-complete-inventory)
3. [Agents Reference](#3-agents-reference)
4. [Subagents Reference](#4-subagents-reference)
5. [Skills Reference](#5-skills-reference)
6. [SpecKit Commands Reference](#6-speckit-commands-reference)
7. [History Records (ADR/PHR)](#7-history-records-adrphr)
8. [Your Responsibilities Checklist](#8-your-responsibilities-checklist)
9. [Decision Trees](#9-decision-trees)
10. [Quick Reference Card](#10-quick-reference-card)

---

## 1. Overview

### What is Reusable Intelligence?

Reusable Intelligence is a framework of **knowledge documents** that guide Claude's behavior. They are NOT executable code - they are structured knowledge that Claude reads to understand:
- **What** to do (agents define responsibilities)
- **How** to do it (skills provide patterns)
- **When** to apply specific expertise (subagents for narrow tasks)

### The Hierarchy

```
┌─────────────────────────────────────────────────────────────┐
│                     CONSTITUTION                             │
│            (specs/constitution.md)                          │
│         Source of truth for all principles                   │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│    AGENTS     │   │    SKILLS     │   │   COMMANDS    │
│ (9 total)     │   │ (9 total)     │   │ (11 total)    │
│ Domain owners │   │ Knowledge     │   │ /sp.* actions │
│ Long-lived    │   │ Reusable      │   │ User-triggered│
└───────────────┘   └───────────────┘   └───────────────┘
        │
        ▼
┌───────────────┐
│  SUBAGENTS    │
│ (14 total)    │
│ Task-specific │
│ Narrow scope  │
└───────────────┘
```

### How Claude Uses These

| Type | How Claude Uses It | When Read |
|------|-------------------|-----------|
| Agents | Reads for domain guidance | Working in that domain |
| Subagents | Reads for specific task patterns | Doing that specific task |
| Skills | Reads for code patterns & knowledge | Implementing related features |
| Commands | Executes when you type `/sp.*` | You trigger them |

---

## 2. Complete Inventory

### Summary Table

| Category | Count | Location | Status |
|----------|-------|----------|--------|
| Agents | 9 | `.claude/agents/` | ✅ All workable |
| Subagents | 14 | `.claude/subagents/` | ✅ All workable |
| Skills | 9 | `.claude/skills/` | ✅ All workable |
| Commands | 11 | `.claude/commands/` | ✅ All workable |
| Workflows | 0 | `.claude/workflows/` | ⚠️ Not created |
| Task Templates | 0 | `specs/tasks/templates/` | ⚠️ Not created |
| ADRs | 4 | `history/adr/` | ✅ Active |
| PHR Directories | 4 | `history/prompts/` | ✅ Active |

### File Listing

```
.claude/
├── agents/                          # 9 agents
│   ├── ai-mcp.md
│   ├── auth-security.md
│   ├── backend-service.md
│   ├── docs-demo.md
│   ├── frontend-web.md
│   ├── infra-devops.md
│   ├── system-architect.md
│   ├── testing-quality.md
│   └── vercel-deployment.md
│
├── subagents/                       # 14 subagents
│   ├── api-endpoint-implementer.md
│   ├── better-auth-jwt-integrator.md
│   ├── chat-agent-behavior-tuner.md
│   ├── db-schema-migration-specialist.md
│   ├── dockerfile-creator.md
│   ├── git-hygiene-subagent.md
│   ├── helm-k8s-manifests-writer.md
│   ├── k8s-troubleshooter.md
│   ├── mcp-tools-implementer.md
│   ├── spec-constitution-enforcer.md
│   ├── task-planner.md
│   ├── test-generator.md
│   ├── ui-component-implementer.md
│   └── vercel-sanitizer.md
│
├── skills/                          # 9 skills
│   ├── better-auth-jwt.md
│   ├── chatkit-integration.md
│   ├── docker-minikube.md
│   ├── git-workflow.md
│   ├── kafka-dapr-patterns.md
│   ├── mcp-crud-design.md
│   ├── neon-sqlmodel.md
│   ├── spec-kit-monorepo.md
│   └── vercel-deployment.md
│
├── commands/                        # 11 commands
│   ├── sp.adr.md
│   ├── sp.analyze.md
│   ├── sp.checklist.md
│   ├── sp.clarify.md
│   ├── sp.constitution.md
│   ├── sp.git.commit_pr.md
│   ├── sp.implement.md
│   ├── sp.phr.md
│   ├── sp.plan.md
│   ├── sp.specify.md
│   └── sp.tasks.md
│
└── workflows/                       # 0 workflows (not yet created)

history/
├── adr/                             # 4 ADRs
│   ├── 001-authentication-stack-better-auth.md
│   ├── 002-database-stack-neon-postgresql.md
│   ├── 003-orm-stack-sqlmodel.md
│   └── 004-data-model-user-id-as-text.md
│
└── prompts/                         # 4 PHR directories
    ├── 001-phase1-console-todo/
    ├── constitution/
    ├── general/
    └── phase-2/
```

---

## 3. Agents Reference

Agents are **long-lived domain owners** with broad responsibilities.

### Agent Matrix

| Agent | File | Domain | Active Phase | Key Responsibilities |
|-------|------|--------|--------------|---------------------|
| System Architect | `system-architect.md` | Architecture | All | Phase transitions, tech decisions, cross-cutting concerns |
| Backend Service | `backend-service.md` | Backend | II+ | FastAPI, SQLModel, MCP server, API endpoints |
| Frontend Web | `frontend-web.md` | Frontend | II+ | Next.js, React, UI components, ChatKit |
| Auth Security | `auth-security.md` | Security | II+ | Better Auth, JWT, security patterns |
| AI MCP | `ai-mcp.md` | AI | III+ | OpenAI Agents SDK, MCP tools, AI behavior |
| Infra DevOps | `infra-devops.md` | Infrastructure | IV+ | Docker, K8s, Helm, Dapr |
| Testing Quality | `testing-quality.md` | Quality | All | Test strategy, coverage, quality gates |
| Docs Demo | `docs-demo.md` | Documentation | All | README, docs, demo scripts |
| Vercel Deployment | `vercel-deployment.md` | Deployment | II+ | Vercel-specific deployment |

### Agent Details

#### 1. System Architect Agent
**File**: `.claude/agents/system-architect.md`
**When Claude Reads It**: Making architecture decisions, phase transitions

**Responsibilities**:
- Overall system architecture
- Phase boundary enforcement
- Technology selection decisions
- Cross-cutting concerns (logging, monitoring)
- Integration patterns between components

**You Should Reference When**:
- Starting a new phase
- Making technology choices
- Designing system integrations

---

#### 2. Backend Service Agent
**File**: `.claude/agents/backend-service.md`
**When Claude Reads It**: Working on backend code

**Responsibilities**:
- FastAPI route implementations
- SQLModel model definitions
- Database connection management
- JWT middleware and auth
- MCP tool implementations (Phase III+)
- Backend tests

**You Should Reference When**:
- Creating API endpoints
- Modifying database models
- Setting up authentication
- Implementing MCP tools

---

#### 3. Frontend Web Agent
**File**: `.claude/agents/frontend-web.md`
**When Claude Reads It**: Working on frontend code

**Responsibilities**:
- Next.js App Router pages
- React component implementation
- State management
- API client integration
- ChatKit integration (Phase III+)
- Frontend tests

**You Should Reference When**:
- Creating UI components
- Implementing pages
- Setting up state management
- Integrating with backend

---

#### 4. Auth Security Agent
**File**: `.claude/agents/auth-security.md`
**When Claude Reads It**: Working on authentication/authorization

**Responsibilities**:
- Better Auth configuration
- JWT token handling
- Protected routes
- Security best practices
- OAuth integration

**You Should Reference When**:
- Setting up authentication
- Implementing protected routes
- Handling tokens
- Security reviews

---

#### 5. AI MCP Agent
**File**: `.claude/agents/ai-mcp.md`
**When Claude Reads It**: Working on AI features (Phase III+)

**Responsibilities**:
- OpenAI Agents SDK integration
- MCP tool design and implementation
- AI agent behavior tuning
- Natural language processing
- ChatKit UI integration

**You Should Reference When**:
- Starting Phase III
- Implementing AI chatbot
- Creating MCP tools

---

#### 6. Infra DevOps Agent
**File**: `.claude/agents/infra-devops.md`
**When Claude Reads It**: Working on infrastructure (Phase IV+)

**Responsibilities**:
- Docker containerization
- Kubernetes deployment
- Helm charts
- Dapr components
- CI/CD pipelines

**You Should Reference When**:
- Starting Phase IV
- Setting up Docker
- Deploying to Kubernetes

---

#### 7. Testing Quality Agent
**File**: `.claude/agents/testing-quality.md`
**When Claude Reads It**: Writing tests, quality checks

**Responsibilities**:
- Test strategy definition
- Unit test patterns
- Integration test patterns
- Coverage requirements
- Quality gates

**You Should Reference When**:
- Writing tests
- Setting up test infrastructure
- Defining quality requirements

---

#### 8. Docs Demo Agent
**File**: `.claude/agents/docs-demo.md`
**When Claude Reads It**: Documentation tasks

**Responsibilities**:
- README maintenance
- API documentation
- Demo scripts
- Capstone documents
- Session handoff

**You Should Reference When**:
- Updating documentation
- Creating demo videos
- Writing capstones

---

#### 9. Vercel Deployment Agent
**File**: `.claude/agents/vercel-deployment.md`
**When Claude Reads It**: Vercel deployment issues

**Responsibilities**:
- Vercel configuration
- Environment variables
- Build optimization
- Deployment troubleshooting
- Preview deployments

**You Should Reference When**:
- Deploying to Vercel
- Fixing deployment issues
- Optimizing builds

---

## 4. Subagents Reference

Subagents are **narrow task specialists** with focused expertise.

### Subagent Matrix

| Subagent | File | Task Type | Phase |
|----------|------|-----------|-------|
| Spec Constitution Enforcer | `spec-constitution-enforcer.md` | Validation | All |
| Task Planner | `task-planner.md` | Planning | All |
| API Endpoint Implementer | `api-endpoint-implementer.md` | Backend | II+ |
| DB Schema Migration Specialist | `db-schema-migration-specialist.md` | Database | II+ |
| UI Component Implementer | `ui-component-implementer.md` | Frontend | II+ |
| Better Auth JWT Integrator | `better-auth-jwt-integrator.md` | Auth | II+ |
| MCP Tools Implementer | `mcp-tools-implementer.md` | AI | III+ |
| Chat Agent Behavior Tuner | `chat-agent-behavior-tuner.md` | AI | III+ |
| Dockerfile Creator | `dockerfile-creator.md` | Infra | IV+ |
| Helm K8s Manifests Writer | `helm-k8s-manifests-writer.md` | Infra | IV+ |
| K8s Troubleshooter | `k8s-troubleshooter.md` | Infra | IV+ |
| Vercel Sanitizer | `vercel-sanitizer.md` | Deployment | II+ |
| Test Generator | `test-generator.md` | Testing | All |
| Git Hygiene Subagent | `git-hygiene-subagent.md` | Git | All |

### Subagent Details

#### 1. Spec Constitution Enforcer
**File**: `.claude/subagents/spec-constitution-enforcer.md`
**Purpose**: Validates that implementation follows specs and constitution

**Checklist**:
- [ ] Implementation matches spec exactly
- [ ] No scope creep
- [ ] Phase boundaries respected
- [ ] Constitution principles followed

---

#### 2. Task Planner
**File**: `.claude/subagents/task-planner.md`
**Purpose**: Breaks down features into implementable tasks

**Provides**:
- Task breakdown patterns
- Dependency identification
- Estimation guidance
- Priority assignment

---

#### 3. API Endpoint Implementer
**File**: `.claude/subagents/api-endpoint-implementer.md`
**Purpose**: Creates FastAPI endpoints following patterns

**Template Includes**:
- Route definition
- Request/response schemas
- Authentication
- Error handling
- Tests

---

#### 4. DB Schema Migration Specialist
**File**: `.claude/subagents/db-schema-migration-specialist.md`
**Purpose**: Handles database migrations safely

**Provides**:
- SQLModel patterns
- Migration strategies
- Rollback procedures
- Data validation

---

#### 5. UI Component Implementer
**File**: `.claude/subagents/ui-component-implementer.md`
**Purpose**: Creates React components with proper patterns

**Template Includes**:
- Component structure
- Props typing
- State management
- Styling (Tailwind)
- Tests

---

#### 6. Better Auth JWT Integrator
**File**: `.claude/subagents/better-auth-jwt-integrator.md`
**Purpose**: Integrates Better Auth and JWT handling

**Provides**:
- Configuration patterns
- Token extraction
- Protected routes
- Error handling

---

#### 7. MCP Tools Implementer
**File**: `.claude/subagents/mcp-tools-implementer.md`
**Purpose**: Creates MCP tools for AI agent (Phase III+)

**Provides**:
- Tool definition patterns
- Input/output schemas
- Error handling
- Testing patterns

---

#### 8. Chat Agent Behavior Tuner
**File**: `.claude/subagents/chat-agent-behavior-tuner.md`
**Purpose**: Tunes AI agent behavior (Phase III+)

**Provides**:
- Prompt engineering patterns
- Context management
- Response formatting
- Guardrails

---

#### 9. Dockerfile Creator
**File**: `.claude/subagents/dockerfile-creator.md`
**Purpose**: Creates optimized Dockerfiles (Phase IV+)

**Provides**:
- Multi-stage builds
- Optimization patterns
- Security best practices
- Layer caching

---

#### 10. Helm K8s Manifests Writer
**File**: `.claude/subagents/helm-k8s-manifests-writer.md`
**Purpose**: Creates Kubernetes manifests and Helm charts (Phase IV+)

**Provides**:
- Deployment templates
- Service definitions
- ConfigMaps/Secrets
- Helm values

---

#### 11. K8s Troubleshooter
**File**: `.claude/subagents/k8s-troubleshooter.md`
**Purpose**: Debugs Kubernetes issues (Phase IV+)

**Provides**:
- Diagnostic commands
- Common issue fixes
- Log analysis
- Resource debugging

---

#### 12. Vercel Sanitizer
**File**: `.claude/subagents/vercel-sanitizer.md`
**Purpose**: Prepares code for Vercel deployment

**Checklist**:
- [ ] Environment variables configured
- [ ] Build command correct
- [ ] No server-side secrets exposed
- [ ] Middleware configured

---

#### 13. Test Generator
**File**: `.claude/subagents/test-generator.md`
**Purpose**: Generates comprehensive test cases

**Provides**:
- Test templates (backend/frontend)
- Edge case patterns
- Mock strategies
- Coverage guidance

---

#### 14. Git Hygiene Subagent
**File**: `.claude/subagents/git-hygiene-subagent.md`
**Purpose**: Ensures clean git practices

**Checklist**:
- [ ] No secrets in commits
- [ ] Commit message conventions
- [ ] Tests pass
- [ ] Build succeeds
- [ ] SESSION_HANDOFF.md updated

---

## 5. Skills Reference

Skills are **reusable knowledge blocks** with patterns and code snippets.

### Skills Matrix

| Skill | File | Knowledge Domain | Phase |
|-------|------|------------------|-------|
| Spec-Kit Monorepo | `spec-kit-monorepo.md` | SpecKit patterns | All |
| Neon SQLModel | `neon-sqlmodel.md` | Database patterns | II+ |
| Better Auth JWT | `better-auth-jwt.md` | Auth patterns | II+ |
| MCP CRUD Design | `mcp-crud-design.md` | MCP tool patterns | III+ |
| ChatKit Integration | `chatkit-integration.md` | Chat UI patterns | III+ |
| Docker Minikube | `docker-minikube.md` | Container patterns | IV+ |
| Kafka Dapr Patterns | `kafka-dapr-patterns.md` | Event patterns | V+ |
| Vercel Deployment | `vercel-deployment.md` | Deployment patterns | II+ |
| Git Workflow | `git-workflow.md` | Git conventions | All |

### Skill Details

#### 1. Spec-Kit Monorepo
**File**: `.claude/skills/spec-kit-monorepo.md`
**Contains**: SpecKit Plus configuration and usage patterns

**Key Knowledge**:
- Directory structure conventions
- Phase definitions
- Feature specifications
- Command usage

---

#### 2. Neon SQLModel
**File**: `.claude/skills/neon-sqlmodel.md`
**Contains**: Neon PostgreSQL + SQLModel patterns

**Key Knowledge**:
- Connection string handling
- Model definitions
- Session management
- Query patterns
- Migration strategies

---

#### 3. Better Auth JWT
**File**: `.claude/skills/better-auth-jwt.md`
**Contains**: Better Auth integration patterns

**Key Knowledge**:
- Client configuration
- Server configuration
- JWT extraction
- Protected routes
- OAuth setup

---

#### 4. MCP CRUD Design
**File**: `.claude/skills/mcp-crud-design.md`
**Contains**: MCP tool design patterns (Phase III+)

**Key Knowledge**:
- Tool schema design
- CRUD tool patterns
- Error handling
- Testing strategies

---

#### 5. ChatKit Integration
**File**: `.claude/skills/chatkit-integration.md`
**Contains**: ChatKit UI patterns (Phase III+)

**Key Knowledge**:
- Component setup
- Message handling
- Streaming responses
- Custom styling

---

#### 6. Docker Minikube
**File**: `.claude/skills/docker-minikube.md`
**Contains**: Docker and Kubernetes patterns (Phase IV+)

**Key Knowledge**:
- Dockerfile patterns
- Docker Compose
- Minikube setup
- Local development

---

#### 7. Kafka Dapr Patterns
**File**: `.claude/skills/kafka-dapr-patterns.md`
**Contains**: Event-driven patterns (Phase V+)

**Key Knowledge**:
- Pub/sub patterns
- State store usage
- Service invocation
- Event schemas

---

#### 8. Vercel Deployment
**File**: `.claude/skills/vercel-deployment.md`
**Contains**: Vercel deployment patterns

**Key Knowledge**:
- Configuration
- Environment variables
- Build optimization
- Edge functions

---

#### 9. Git Workflow
**File**: `.claude/skills/git-workflow.md`
**Contains**: Git conventions and workflows

**Key Knowledge**:
- Branch naming
- Commit conventions
- PR workflow
- Semantic versioning

---

## 6. SpecKit Commands Reference

Commands are **user-triggered actions** via `/sp.*` syntax.

### Commands Matrix

| Command | Purpose | When to Use | Output |
|---------|---------|-------------|--------|
| `/sp.specify` | Create feature spec | Starting new feature | `specs/features/*.md` |
| `/sp.plan` | Create implementation plan | After spec ready | `specs/*/plan.md` |
| `/sp.tasks` | Generate task list | After plan ready | `specs/tasks/*.md` |
| `/sp.clarify` | Ask clarifying questions | Spec is ambiguous | Updated spec |
| `/sp.adr` | Record architecture decision | Major tech choice | `history/adr/*.md` |
| `/sp.phr` | Record prompt history | Valuable exchange | `history/prompts/*.md` |
| `/sp.constitution` | Update constitution | Principles change | Updated constitution |
| `/sp.checklist` | Generate checklist | Before deployment | Checklist output |
| `/sp.analyze` | Analyze consistency | After task generation | Analysis report |
| `/sp.git.commit_pr` | Git workflow | Ready to commit/PR | Git operations |
| `/sp.implement` | Execute tasks | Ready to implement | Code changes |

### Command Details

#### `/sp.specify`
**Purpose**: Create a feature specification
**Input**: Feature description
**Output**: `specs/features/{feature-name}.md`

**Example**:
```
/sp.specify "User can filter tasks by status (complete/incomplete)"
```

---

#### `/sp.plan`
**Purpose**: Create implementation plan from spec
**Input**: Feature spec (auto-detected or specified)
**Output**: Implementation plan with steps

**Example**:
```
/sp.plan
```

---

#### `/sp.tasks`
**Purpose**: Generate actionable task list
**Input**: Plan (auto-detected)
**Output**: `specs/tasks/{feature-name}-tasks.md`

**Example**:
```
/sp.tasks
```

---

#### `/sp.clarify`
**Purpose**: Ask clarifying questions about spec
**Input**: Spec to clarify
**Output**: Up to 5 clarifying questions, updates spec with answers

**Example**:
```
/sp.clarify
```

---

#### `/sp.adr`
**Purpose**: Record an Architecture Decision Record
**Input**: Decision context
**Output**: `history/adr/{number}-{title}.md`

**Example**:
```
/sp.adr
```

---

#### `/sp.phr`
**Purpose**: Record a Prompt History Record
**Input**: Exchange to record
**Output**: `history/prompts/{category}/{title}.md`

**Example**:
```
/sp.phr
```

---

#### `/sp.constitution`
**Purpose**: Update project constitution
**Input**: Principle changes
**Output**: Updated `specs/constitution.md`

**Example**:
```
/sp.constitution
```

---

#### `/sp.checklist`
**Purpose**: Generate a custom checklist
**Input**: Context (deployment, feature, etc.)
**Output**: Checklist for the context

**Example**:
```
/sp.checklist
```

---

#### `/sp.analyze`
**Purpose**: Analyze consistency across spec/plan/tasks
**Input**: Auto-detects files
**Output**: Consistency report

**Example**:
```
/sp.analyze
```

---

#### `/sp.git.commit_pr`
**Purpose**: Autonomous git workflow
**Input**: Changes to commit
**Output**: Commit and/or PR

**Example**:
```
/sp.git.commit_pr
```

---

#### `/sp.implement`
**Purpose**: Execute tasks from tasks.md
**Input**: Task file
**Output**: Implemented code

**Example**:
```
/sp.implement
```

---

## 7. History Records (ADR/PHR)

### Architecture Decision Records (ADRs)

**Location**: `history/adr/`
**Purpose**: Record significant technical decisions

**Current ADRs**:
1. `001-authentication-stack-better-auth.md` - Why Better Auth
2. `002-database-stack-neon-postgresql.md` - Why Neon
3. `003-orm-stack-sqlmodel.md` - Why SQLModel
4. `004-data-model-user-id-as-text.md` - Why text user IDs

**When to Create**:
- Choosing a technology
- Changing architecture
- Making trade-off decisions
- Deviating from common patterns

---

### Prompt History Records (PHRs)

**Location**: `history/prompts/`
**Purpose**: Record valuable AI exchanges for learning

**Current Categories**:
- `001-phase1-console-todo/` - Phase I learnings
- `constitution/` - Constitution-related exchanges
- `general/` - General useful patterns
- `phase-2/` - Phase II learnings

**When to Create**:
- Solved a tricky problem
- Learned something reusable
- Found a good pattern
- Made a mistake worth documenting

---

## 8. Your Responsibilities Checklist

### Legend
- 🔴 **MUST DO** - Required for compliance
- 🟡 **SHOULD DO** - Strongly recommended
- 🟢 **NICE TO DO** - Optional but beneficial

---

### A. Every Session

| Task | Priority | Trigger | Command/Action |
|------|----------|---------|----------------|
| Update SESSION_HANDOFF.md | 🔴 MUST | End of session | Claude updates, you verify |
| Review changes before commit | 🔴 MUST | Before commit | Review git diff |
| Run tests | 🔴 MUST | Before commit | `uv run pytest` / `npm test` |

---

### B. When Starting New Feature

| Task | Priority | Trigger | Command/Action |
|------|----------|---------|----------------|
| Create feature spec | 🔴 MUST | New feature request | `/sp.specify "description"` |
| Create implementation plan | 🔴 MUST | After spec | `/sp.plan` |
| Generate tasks | 🟡 SHOULD | After plan | `/sp.tasks` |
| Clarify ambiguities | 🟡 SHOULD | Spec unclear | `/sp.clarify` |

---

### C. When Making Decisions

| Task | Priority | Trigger | Command/Action |
|------|----------|---------|----------------|
| Create ADR | 🔴 MUST | Technology choice | `/sp.adr` |
| Create ADR | 🔴 MUST | Architecture change | `/sp.adr` |
| Update constitution | 🟡 SHOULD | Principle change | `/sp.constitution` |

---

### D. When Learning Something

| Task | Priority | Trigger | Command/Action |
|------|----------|---------|----------------|
| Create PHR | 🟡 SHOULD | Solved tricky problem | `/sp.phr` |
| Update skill | 🟡 SHOULD | Found reusable pattern | "Update [skill] with..." |
| Update subagent | 🟢 NICE | Better checklist item | "Add to [subagent]..." |

---

### E. Before Deployment

| Task | Priority | Trigger | Command/Action |
|------|----------|---------|----------------|
| Run checklist | 🔴 MUST | Before deploy | `/sp.checklist` |
| Verify environment vars | 🔴 MUST | Before deploy | Check Vercel/Railway |
| Run all tests | 🔴 MUST | Before deploy | Full test suite |
| Update docs | 🟡 SHOULD | After changes | Update README if needed |

---

### F. When Discovering Truths

| What You Learned | Action | Example Prompt |
|------------------|--------|----------------|
| Code pattern works well | Update skill | "Update neon-sqlmodel skill with this SQLite test pattern" |
| New responsibility for agent | Update agent | "Add MCP error handling to backend-service agent" |
| Better checklist item | Update subagent | "Add 'check FK constraints' to test-generator subagent" |
| Architecture insight | Create ADR | `/sp.adr` |
| Valuable exchange | Create PHR | `/sp.phr` |
| Principle needs update | Update constitution | `/sp.constitution` |
| Reusable task pattern | Create template | "Create task template for API endpoint implementation" |

---

### G. Phase Transitions

| Task | Priority | Trigger | Command/Action |
|------|----------|---------|----------------|
| Run phase gate check | 🔴 MUST | Before next phase | `bash scripts/check-phase-N-complete.sh` |
| Create capstone | 🔴 MUST | Phase complete | Document in `specs/phase-N/capstone.md` |
| Update VERSION | 🔴 MUST | Phase complete | Update VERSION file |
| Update CHANGELOG | 🟡 SHOULD | Phase complete | Add to CHANGELOG.md |

---

## 9. Decision Trees

### When to Use Which Command

```
New feature requested?
├── YES → /sp.specify
│         └── Spec created?
│             ├── YES → /sp.plan
│             │         └── Plan created?
│             │             ├── YES → /sp.tasks (optional)
│             │             └── NO → Continue planning
│             └── NO → Need clarification? → /sp.clarify
└── NO → Continue with existing work

Making architecture decision?
├── YES → /sp.adr
└── NO → Continue

Found valuable pattern/exchange?
├── YES → /sp.phr
└── NO → Continue

Ready to commit?
├── YES → Follow git-hygiene-subagent checklist
│         └── Or use /sp.git.commit_pr
└── NO → Continue working

Session ending?
├── YES → Update SESSION_HANDOFF.md
│         └── Commit changes
└── NO → Continue
```

### When to Update What

```
Learned a new code pattern?
├── Reusable across features? → Update relevant skill
├── Specific to task type? → Update relevant subagent
└── One-time thing? → Don't update anything

Found a bug in process?
├── Constitution principle? → /sp.constitution
├── Agent responsibility? → Update agent
├── Subagent checklist? → Update subagent
└── Skill knowledge? → Update skill

Made a technology choice?
├── Will affect multiple features? → /sp.adr (REQUIRED)
├── Local to one feature? → Document in spec
└── Trivial choice? → No documentation needed
```

---

## 10. Quick Reference Card

### Most Common Actions

| I want to... | Do this |
|--------------|---------|
| Start a new feature | `/sp.specify "description"` |
| Plan implementation | `/sp.plan` |
| Record a decision | `/sp.adr` |
| Save useful exchange | `/sp.phr` |
| Commit changes | `/sp.git.commit_pr` or manual |
| Check before deploy | `/sp.checklist` |
| Update a skill | "Update [skill] with [pattern]" |
| Update an agent | "Add [responsibility] to [agent]" |

### File Locations Quick Reference

```
Constitution:     specs/constitution.md
Phase Specs:      specs/phases/phase-N.md
Feature Specs:    specs/features/*.md
Task Specs:       specs/tasks/*.md
Agents:           .claude/agents/*.md
Subagents:        .claude/subagents/*.md
Skills:           .claude/skills/*.md
Commands:         .claude/commands/*.md
ADRs:             history/adr/*.md
PHRs:             history/prompts/*/*.md
Session Handoff:  docs/SESSION_HANDOFF.md
```

### Phase Gate Scripts

```bash
# Phase I → II
bash scripts/check-phase-1-complete.sh

# Phase II → III
bash scripts/check-phase-2-complete.sh

# Phase III → IV
bash scripts/check-phase-3-complete.sh

# Phase IV → V
bash scripts/check-phase-4-complete.sh

# Phase V final
bash scripts/check-phase-5-complete.sh
```

---

## Appendix: Gaps to Fill

### Not Yet Created

| Item | Priority | Create When |
|------|----------|-------------|
| Workflows | Low | When orchestration needed |
| Task Templates | Medium | When patterns emerge |
| Phase III+ agent details | Low | When Phase III starts |

### How to Create Missing Items

**Task Template**:
```
"Create a task template for [pattern] in specs/tasks/templates/"
```

**Workflow**:
```
"Create a workflow for [process] in .claude/workflows/"
```

---

**Document Version**: 1.0.0
**Last Updated**: 2025-12-10
**Maintainer**: User (with Claude's assistance)
