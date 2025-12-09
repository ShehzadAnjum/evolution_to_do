I assumes the Hackathon II Todo spec is already in /specs and that you are using SpecKit and 
---

1. Purpose and scope of this document

---

This document tells Claude Code:

* What this project is
* How the repository is structured
* Which agents, subagents, skills, tasks, and workflows exist
* How to work phase by phase from Constitution to deployment
* How to avoid the problems already seen (Git issues, Vercel deployment issues, local-works-remote-breaks)

Goal

* 100 percent coverage of the Hackathon II requirements and phases
* Clean Spec-Driven Development from constitution → plan → tasks → implementation → tests → deployment
* Reusable intelligence that can be copied to future projects

Claude, always respect this document and keep implementation aligned with it.

---

2. Monorepo structure

---

Root layout

* specs/

  * constitution.md           (this document)
  * hackathon-brief.md        (original hackathon specification)
  * phases/

    * phase-1.md
    * phase-2.md
    * phase-3.md
    * phase-4.md
    * phase-5.md
  * api/

    * rest-endpoints.md
    * mcp-tools.md
  * database/

    * schema.md
    * migrations-notes.md
  * features/

    * tasks-core.md
    * auth-and-users.md
    * chat-agent.md
    * recurring-tasks-and-reminders.md
    * events-and-kafka-dapr.md
  * tasks/

    * phase-1-tasks.md
    * phase-2-tasks.md
    * phase-3-tasks.md
    * phase-4-tasks.md
    * phase-5-tasks.md
    * templates/

      * template-crud-feature.md
      * template-secure-api-with-jwt.md
      * template-add-mcp-tool.md
      * template-deploy-service-to-minikube.md
      * template-add-recurring-feature.md

* backend/

  * app/                      (FastAPI, SQLModel, MCP server, Agents SDK)
  * tests/
  * CLAUDE.md                 (backend-focused instructions)
  * pyproject.toml / requirements.txt

* frontend/

  * app/                      (Next.js app router)
  * components/
  * lib/
  * CLAUDE.md                 (frontend-focused instructions)
  * package.json
  * next.config.js

* infra/

  * docker/

    * backend.Dockerfile
    * frontend.Dockerfile
    * docker-compose.local.yml
  * k8s/

    * base-manifests/
    * helm/
  * dapr/

    * components/
  * kafka/                    (Redpanda / Kafka configs)
  * CLAUDE.md

* .claude/

  * agents/                   (long-lived top-level agents)
  * subagents/                (narrow specialists)
  * skills/                   (reusable knowledge)
  * workflows/                (optional, orchestration YAML if used)

* .spec-kit/

  * config.yaml               (SpecKit configuration for this repo)

* CLAUDE.md                   (root project guidance file for Claude Code)

* README.md

Claude, when editing code in any folder, first read the nearest CLAUDE.md in that folder and follow its rules.

---

3. Project phases (from the hackathon document)

---

The hackathon defines multiple phases for the same Todo domain. High-level mapping:

* Phase 1

  * Local, simple implementation
  * Focus on basic CRUD, no web UI, no AI, minimal infra

* Phase 2

  * Proper backend (FastAPI + SQLModel + Neon)
  * Web frontend (Next.js + Better Auth)
  * Clean DB and auth design

* Phase 3

  * AI agent and MCP tools
  * Chat entry point for the Todo domain

* Phase 4

  * Dockerizing, basic K8s deployment, local cluster

* Phase 5

  * Kafka / Redpanda and Dapr integration
  * Cloud-native, event-driven Todo

This Constitution governs all phases. Each phase gets its own spec file in specs/phases and its own task list in specs/tasks.

---

4. Main constitution for the whole project

---

Vision

* Deliver a Todo system that evolves from local to fully cloud-native and AI-augmented
* Use Spec-Driven Development:

  * Write and refine specs first
  * Plan tasks from specs
  * Implement tasks
  * Test and deploy
  * Keep specs and code aligned

Non-functional constraints and high-level gates

* Gate 0: Constitution ready

  * specs/constitution.md written and reviewed
  * Root CLAUDE.md created
  * .spec-kit/config.yaml present

* Gate 1: Phase 1 completion

  * Phase 1 spec in specs/phases/phase-1.md is accurate
  * All Phase 1 tasks in specs/tasks/phase-1-tasks.md are complete
  * Application works locally as described
  * No hardcoded architecture dead-ends that block Phase 2

* Gate 2: Phase 2 completion

  * Clean API layer and SQLModel schema
  * Neon connection stable
  * Better Auth integrated and issuing JWTs
  * Frontend uses API and auth correctly
  * Basic test coverage for core API endpoints and components

* Gate 3: Phase 3 completion

  * MCP tools implemented and tested
  * AI chat endpoint stable
  * ChatKit integrated on frontend
  * Agent can perform CRUD via tools

* Gate 4: Phase 4 completion

  * Backend and frontend Dockerfiles verified
  * Local Docker Compose or Minikube runs successfully
  * Basic K8s manifests or Helm chart deploys and app is reachable

* Gate 5: Phase 5 completion

  * Kafka / Redpanda installed in cluster
  * Dapr components configured
  * Events for tasks and reminders flowing end-to-end
  * Observability and simple health checks in place

Claude, always keep these gates in mind when making changes.

---

5. Root CLAUDE.md (summary of what Claude should do)

---

Core instructions to Claude Code at repo root (summary; you can copy this into the root CLAUDE.md file):

* Always read:

  * specs/constitution.md
  * specs/hackathon-brief.md
  * specs/phases/<current-phase>.md
* Never implement features that are not backed by a spec file
* When asked for changes, do:

  * Update spec if needed
  * Ask to confirm spec changes if they are large
  * Then implement code changes
  * Then update tests and docs
* Prefer small, focused pull-request sized changes
* Keep frontend and backend aligned with:

  * specs/api/rest-endpoints.md
  * specs/database/schema.md
* Use the agents, subagents, and skills defined in .claude/ instead of rewriting prompts each time

---

6. Agents (reusable intelligence, long-lived)

---

Create these as markdown files under .claude/agents.

6.1 System Architect Agent

File: .claude/agents/system-architect.md

Mission

* Own the architecture across all phases
* Keep specs, tasks, and code aligned with the Constitution and hackathon brief

Scope

* Edit specs/constitution.md and specs/phases/*
* Define and adjust folder structure
* Define API, DB, and AI interactions at a high level

Out of scope

* Writing detailed component code
* Writing CSS and small UI details

Inputs

* Any spec files
* Git history if needed

Outputs

* Updated spec documents
* ADR-style notes when big decisions change

6.2 Backend Service Agent

File: .claude/agents/backend-service.md

Mission

* Own the FastAPI app, SQLModel models, DB migrations, and MCP server

Scope

* Implement and maintain REST endpoints
* Implement MCP tools for tasks
* Integrate Neon and handle migrations
* Keep specs/api/rest-endpoints.md and specs/database/schema.md in sync with code

6.3 Frontend Web Agent

File: .claude/agents/frontend-web.md

Mission

* Own the Next.js app, including UI, ChatKit integration, and communication with backend

Scope

* Implement pages, components, and hooks
* Configure ChatKit and domain settings
* Handle Better Auth client-side flow and token passing

6.4 Auth and Security Agent

File: .claude/agents/auth-security.md

Mission

* Own Better Auth configuration, JWT issuance and verification, and API security

Scope

* Configure Better Auth with Neon
* Implement JWT plugin
* Add FastAPI guards and middleware
* Define routes and guards based on roles

6.5 AI and MCP Agent

File: .claude/agents/ai-mcp.md

Mission

* Own AI agent design and MCP tools

Scope

* Define tools in specs/api/mcp-tools.md
* Implement MCP server functions
* Design system and user prompts for the Todo agent
* Ensure tools cover all required operations and error handling

6.6 Infra and DevOps Agent

File: .claude/agents/infra-devops.md

Mission

* Own Docker, Docker Compose, K8s, Helm, Dapr, and Kafka/Redpanda setup

Scope

* Create and maintain Dockerfiles, compose files, manifests, Helm charts
* Configure Dapr components and Kafka topics
* Provide scripts and instructions for local and cloud deployment

6.7 Testing and Quality Agent

File: .claude/agents/testing-quality.md

Mission

* Own test strategy and quality gates

Scope

* Define test structure for backend and frontend
* Write or update tests when features change
* Define phase gates in specs/constitution.md
* Run and interpret test results

6.8 Docs and Demo Agent

File: .claude/agents/docs-demo.md

Mission

* Own README, developer setup guide, architecture overview, and demo scripts

Scope

* Keep README.md up to date
* Maintain simple diagrams in plain text or Mermaid in specs/
* Prepare short demo scripts and notes per phase

6.9 Vercel Deployment Agent

File: .claude/agents/vercel-deployment.md

Mission

* Own everything related to Vercel deployments for the frontend

Scope

* Ensure that:

  * Vercel is wired to the correct branch
  * Environment variables are defined in Vercel
  * next.config.js is compatible with serverless runtime
  * No unsupported Node-only APIs are used in Server Components

Inputs

* frontend code
* Vercel project details (documented in specs or README)

Outputs

* Deployment checklist
* Fixes for Vercel-specific errors

---

7. Subagents (narrow specialists)

---

Create these as markdown files under .claude/subagents.

7.1 Spec and Constitution Enforcer

Job

* Given a spec file and code paths, detect drift and inconsistencies

Used for

* Pre-commit checks
* Before phase submission
* Before major refactors

7.2 Task Planner

Job

* Take a spec (phase or feature) and generate a list of tasks:

  * Short titles
  * Description
  * Acceptance criteria
  * Suggested agent

Used for

* Start of each phase
* Start of large features such as recurring tasks or chat

7.3 API Endpoint Implementer

Job

* Implement one backend REST endpoint with:

  * FastAPI route
  * SQLModel changes
  * Pydantic schemas
  * Backend tests

7.4 DB Schema and Migration Specialist

Job

* Adjust SQLModel models
* Generate or describe migrations
* Keep specs/database/schema.md in sync

7.5 UI Component Implementer

Job

* Implement a single UI component or page in Next.js
* Wire it to API and handle errors cleanly

7.6 Better Auth and JWT Integrator

Job

* Configure Better Auth to use Neon
* Enable JWT issuance
* Implement client token handling and backend verification

7.7 MCP Tools Implementer

Job

* Implement add_task, list_tasks, update_task, delete_task, complete_task and similar tools
* Write tests for each tool

7.8 Chat Agent Behavior Tuner

Job

* Focus on system prompt and behavior of the Todo agent
* Map natural language intents to tools
* Avoid hallucinations and unsupported operations

7.9 Dockerfile Creator

Job

* Write and adjust backend and frontend Dockerfiles
* Ensure they work in local Docker and K8s

7.10 Helm and K8s Manifests Writer

Job

* Generate Helm charts and base manifests
* Ensure required env vars and secrets are defined

7.11 K8s Troubleshooter

Job

* Read kubectl outputs, pod logs, and suggest fixes

7.12 Vercel Sanitizer

Job

* Scan frontend code for patterns that break Vercel:

  * Node-only APIs in server components
  * Misplaced env variables
  * Incorrect dynamic imports

7.13 Test Generator

Job

* Generate or improve tests for a given endpoint, MCP tool, or component

7.14 Git Hygiene Subagent

Job

* Ensure:

  * No secrets committed
  * Reasonable commit messages
  * Main branch always stable
  * Feature branches merged in with review

---

8. Skills (reusable knowledge blocks)

---

Create these as markdown files under .claude/skills.

Each skill should:

* Explain the domain
* List common pitfalls
* Provide best-practice patterns

Required skills for this project:

* skill-spec-kit-monorepo.md

  * How specs, .spec-kit, frontend, backend, infra, and .claude relate

* skill-neon-sqlmodel.md

  * Connection patterns
  * Session management
  * Basic indexing and performance

* skill-better-auth-jwt.md

  * Setup steps
  * How to wire backend and frontend
  * Common errors

* skill-mcp-crud-design.md

  * How to design CRUD tools for Todo items
  * Error handling patterns

* skill-chatkit-integration.md

  * Domain configuration
  * Key usage
  * Basic chat UI wiring

* skill-docker-minikube.md

  * How to build and run images locally
  * Common issues

* skill-kafka-dapr-patterns.md

  * Event model for Todo changes and reminders
  * Topic naming and Dapr pub/sub mapping

* skill-vercel-deployment.md

  * Branch selection
  * Env vars
  * Common Next.js pitfalls on Vercel

* skill-git-workflow.md

  * Branch strategy
  * Merge rules
  * How to keep main deployable

---

9. Development methodology (how Claude should work)

---

For every phase and feature:

1. Start from specs

* Read:

  * specs/constitution.md
  * specs/hackathon-brief.md
  * specs/phases/<phase>.md
* If the request is not clearly covered by specs, clarify or update the spec first

2. Plan tasks

* Use the Task Planner subagent on the relevant spec files
* Store tasks in specs/tasks/phase-x-tasks.md
* Ensure each task:

  * Has a clear title
  * Has acceptance criteria
  * Has a suggested agent

3. Implement in small steps

* Pick one task
* Use the appropriate agent and subagents
* Make focused changes in backend, frontend, or infra
* Update tests and docs in the same step

4. Quality and alignment

* Use:

  * Testing and Quality Agent
  * Spec and Constitution Enforcer subagent
* Confirm:

  * Specs match code
  * Tests pass
  * No obvious regressions

5. Git and Vercel safety

* Use Git Hygiene subagent for:

  * Checking for secrets
  * Commit message review
* Before pushing to main or deploy branch:

  * Run the tests locally
  * For frontend, run the Vercel Sanitizer subagent
* Only then push

---

10. Git workflow and avoiding past issues

---

Branching

* main

  * Always stable
  * Only code that passes tests and deploys cleanly

* dev

  * Integration branch for new features

* feature/...

  * Short-lived branches for specific tasks

Rules

* Never push experimental code directly to main
* Always run tests and basic local checks before pushing
* When a Vercel build fails, capture the error and let the Vercel Deployment Agent and Vercel Sanitizer subagent suggest fixes

Common pitfalls to avoid

* Missing environment variables in Vercel
* Using process.env directly in client components without NEXT_PUBLIC prefix
* Server-only modules imported into client components
* Node-only APIs used in edge runtimes

---

11. Backend and frontend CLAUDE.md content (summary)

---

backend/CLAUDE.md

* Always respect:

  * specs/api/rest-endpoints.md
  * specs/database/schema.md
* When adding or changing an endpoint:

  * Update spec first if needed
  * Use Backend Service Agent and API Endpoint Implementer subagent
  * Add or update tests
* For DB changes:

  * Use DB Schema and Migration Specialist subagent
  * Update specs/database/schema.md

frontend/CLAUDE.md

* Always respect:

  * specs/features/tasks-core.md
  * specs/features/auth-and-users.md
  * specs/features/chat-agent.md
* Use Frontend Web Agent and UI Component Implementer subagent
* For auth:

  * Use Better Auth and JWT Integrator subagent
* For chat:

  * Use ChatKit Integration skill and Chat Agent Behavior Tuner subagent

infra/CLAUDE.md

* Use Infra and DevOps Agent
* For Docker:

  * Use Dockerfile Creator subagent
* For K8s and Helm:

  * Use Helm and K8s Manifests Writer, K8s Troubleshooter
* For Kafka and Dapr:

  * Use Kafka / Dapr skill and related patterns

---

12. How to harvest reusable intelligence during and after the project

---

During the project

* Whenever you repeat a long explanation or pattern:

  * Turn it into a Skill or a subagent
* Whenever you repeat a sequence of changes:

  * Turn it into a task template

After each phase

* Have Docs and Demo Agent write:

  * What went well
  * What failed (for example, specific Git or Vercel issues)
  * Which prompts and patterns worked best

At the end of the project

* Review:

  * .claude/agents
  * .claude/subagents
  * .claude/skills
  * specs/tasks/templates
* Clean them
* Copy them into a separate “SDD-RI Library” repo so you can reuse them in future projects

---

13. Project versioning scheme

---

Version format

* All releases follow semantic versioning: MAJOR.MINOR.PATCH (mm.nnn.ooo)

Version increment rules

* MAJOR (mm)

  * Incremented for breaking changes, major architectural shifts, or phase transitions
  * Examples: Phase 1→2, major API redesigns, authentication system overhaul
  * Reset MINOR and PATCH to 0

* MINOR (nnn)

  * Incremented when new features are added or existing features significantly change
  * Examples: New task filtering, recurring tasks, chat agent, OAuth providers
  * Reset PATCH to 0
  * Keep MAJOR unchanged

* PATCH (ooo)

  * Incremented for bug fixes, minor improvements, or iterations on the same feature
  * Examples: UI tweaks, performance optimizations, dependency updates, documentation fixes
  * Keep MAJOR and MINOR unchanged

Version tracking

* Current version stored in VERSION file at project root
* Version displayed prominently in application UI:

  * Bottom right of login page
  * Footer of dashboard pages
  * /api/version endpoint (backend)

* Version updated in VERSION file before each commit that changes code
* Git tags created for each MAJOR and MINOR release

Version governance

* Version changes require:

  * Update VERSION file with new version number
  * Update CHANGELOG.md with changes since last version
  * Commit message format: "chore: bump version to X.Y.Z"

* MAJOR version changes require:

  * ADR documenting breaking changes and migration path
  * Update to constitution if governance rules change
  * Sign-off from project owner

* Version history maintained in CHANGELOG.md with format:

  * Version number and date
  * Summary of changes (Added, Changed, Fixed, Removed)
  * Links to relevant commits and pull requests

Initial version

* Current version: 02.001.000

  * MAJOR 02: Phase II (web app with authentication)
  * MINOR 001: First feature-complete version of Phase II
  * PATCH 000: Initial release

---

14. What Claude should do now with this document

---

1. Verify the current repo against this structure
2. Propose and apply changes to:

   * Folder structure
   * specs layout
   * .claude agents, subagents, and skills
   * Root and subfolder CLAUDE.md files
3. Bring the project back into alignment phase by phase, starting at Phase 1
4. Add missing tests, docs, and deployment checks, with special attention to:

   * Git hygiene
   * Vercel deployment stability
   * Backend and frontend alignment
