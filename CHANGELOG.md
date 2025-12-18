# Changelog

All notable changes to the Evolution of Todo project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Version format: MAJOR.MINOR.PATCH (mm.nnn.ooo)

- **MAJOR**: Phase transitions, breaking changes, major architectural shifts
- **MINOR**: New features, significant feature changes
- **PATCH**: Bug fixes, minor improvements, iterations on same feature

---

## [05.11.000] - 2025-12-17

### Added
- **FreeRTOS MQTT Task**: Dedicated background task for reliable MQTT connection
  - Runs `mqtt.loop()` every 50ms on Core 1 (separate from WiFi)
  - Mutex-protected MQTT client access
  - Automatic reconnection with exponential backoff
  - 5-minute status logging for monitoring
- **Task Auto-Complete**: Tasks marked complete when ESP32 executes scheduled device actions
  - Backend callback from MQTT EXECUTED message
  - `mark_task_complete_by_command_id()` function in main.py
- **Device Schedule Category**: Auto-assign "Device Schedules" category for IoT tasks
  - Category field disabled for device_schedule tasks
  - Default to "device_schedules" category

### Changed
- **Sidebar Layout**: Moved "Device Schedules" from Views to Categories section
  - Better semantic organization
  - Filters by `task_type === "device_schedule"`
- **MQTT KeepAlive**: Set to 30 seconds (was default 15)
- **WiFi Power Saving**: Explicitly disabled at both Arduino and ESP-IDF level
  - `WiFi.setSleep(false)`
  - `esp_wifi_set_ps(WIFI_PS_NONE)`
- **DNS Resolution Fix**: Detect 0.0.0.0 as DNS failure, use fallback IP

### Fixed
- **MQTT Disconnection Issue**: Root cause was `client.loop()` not called frequently enough
  - FreeRTOS task ensures 20 calls/second
  - Research: https://esp32.com/viewtopic.php?t=16109
- **DNS 0.0.0.0 Bug**: Refresh DNS config before every MQTT reconnect attempt

### Technical Details
- ESP32 code: `evolution_iot.ino` - 2200+ lines with FreeRTOS task
- Stack size: 8KB for MQTT task (TLS needs ~6KB)
- Priority: 5 (higher than main loop)

### Phase
- Phase V: IoT Device Scheduling (v4.0.0 feature)

---

## [05.10.007] - 2025-12-16

### Fixed
- ESP32 LCD single scroll cycle (scroll once then return to time)
- ESP32 schedule display on LCD when receiving SCHEDULE command
- MQTT update on task edit (not just create)

---

## [05.10.006] - 2025-12-15

### Added
- Backend MQTT schedule sync on task update
- ESP32 TIME_DISPLAY_MS increased to 30 seconds

---

## [05.001.000] - 2025-12-11

### Added
- **Phase V Local Complete**: Kafka + Dapr event-driven architecture on Minikube
- **Event Models**: TaskEvent, ReminderEvent, RecurringTriggerEvent in `backend/src/models/event.py`
- **Event Service**: Dapr pub/sub client via HTTP API in `backend/src/services/event_service.py`
- **Event Handlers**: 6 subscription endpoints in `backend/src/api/routes/events.py`
- **Dapr Components**: pubsub.yaml and subscriptions/tasks.yaml
- **Test Script**: `scripts/test-kafka-dapr.sh` for verification
- **ADR-005**: Cloud deployment deferred due to GKE quota

### Changed
- **Tasks Routes**: Added background event publishing to all CRUD operations
- **Helm Chart**: Added Dapr sidecar annotations and values
- **Kafka-Dapr Skill**: Added 8 lessons learned from Phase V

### Infrastructure
- **Strimzi Kafka**: Deployed on Minikube (Bitnami/Redpanda failed)
- **Dapr**: Deployed to K8s with pubsub component
- **GCP Setup**: Project `evolution-todo-v2` created, images pushed to Artifact Registry
- **GKE**: Cluster DELETED due to CPUS_ALL_REGIONS quota (4/10, need 24)

### Event Types Implemented
- task.created, task.updated, task.completed, task.deleted
- reminder.due, recurring.trigger

### Phase
- Phase V: Cloud Deployment + Event-Driven Architecture (Local Complete)

### Notes
- Cloud deployment deferred pending GCP quota increase
- Local Minikube demo fully functional
- Resume commands documented in SESSION_HANDOFF.md
- **1st Iteration Complete** - ready for v1.0.0 tag

---

## [04.001.000] - 2025-12-10

### Added
- **Phase IV Complete**: Docker + Kubernetes + Helm deployment working
- **Backend Dockerfile**: Multi-stage Python 3.13 build
- **Frontend Dockerfile**: Multi-stage Node 20 standalone
- **Docker Compose**: Local development compose file
- **K8s Base Manifests**: Namespace, deployments, services, ingress
- **Helm Chart**: Full chart with configurable values
- **Docker-Minikube Skill**: Added Phase IV lessons learned

### Phase
- Phase IV: Kubernetes Packaging (NO NEW FEATURES)

### Notes
- Both pods running (1/1 READY) on Minikube
- Health endpoint at `/health` not `/api/health`
- Use `imagePullPolicy: Never` for local minikube images

---

## [03.001.000] - 2025-12-10

### Added
- **Phase III MVP**: AI chatbot creates tasks via natural language
- **MCP Module Structure**: `backend/src/mcp/` with tool definitions
- **ToolExecutor**: Bridges MCP tool calls to task database operations
- **Chat API**: POST /api/chat endpoint with JWT authentication
- **OpenAI Client**: Wrapper for gpt-4o-mini with function calling
- **ChatService**: Handles conversation flow and tool execution
- **Chat UI**: MessageInput, MessageList, ChatInterface components
- **Chat Page**: /chat route with AI task assistant
- **PHR-001**: Documented pydantic-settings env vars lesson
- **PHR-002**: Captured unified UI vision for second iteration

### MCP Tools Implemented
- add_task: Create new task via natural language
- list_tasks: Query user's tasks with filters
- get_task: Get single task by ID
- update_task: Modify existing task
- delete_task: Remove task
- complete_task: Mark task as complete
- search_tasks: Search by keyword

### Phase
- Phase III: AI Chatbot with MCP Tools

### Notes
- User verified: "chat is working ok"
- All 7 MCP tools functional
- 108 backend tests passing
- Frontend builds successfully

---

## [03.000.000] - 2025-12-10

### Changed
- **Phase Transition**: Phase II → Phase III (AI Chatbot Integration)
- **Version Bump**: MAJOR version bump for phase transition

### Phase II Sign-Off Summary
- 137 tests passing (108 backend + 29 frontend)
- All task CRUD operations implemented
- Email/password authentication working
- JWT token flow verified
- Known deferral: Google OAuth (to be fixed later)

### Phase
- Phase III: AI Chatbot with MCP Tools

---

## [02.004.000] - 2025-12-10

### Added
- **14 Subagents**: Complete narrow specialist subagent framework
  - spec-constitution-enforcer: Validates code against specs
  - task-planner: Breaks specs into actionable tasks
  - api-endpoint-implementer: Implements REST endpoints
  - db-schema-migration-specialist: Handles database changes
  - ui-component-implementer: Creates React components
  - better-auth-jwt-integrator: Sets up authentication
  - mcp-tools-implementer: Creates MCP tools
  - chat-agent-behavior-tuner: Refines AI system prompts
  - dockerfile-creator: Writes optimized Dockerfiles
  - helm-k8s-manifests-writer: Generates K8s manifests
  - k8s-troubleshooter: Debugs Kubernetes issues
  - vercel-sanitizer: Scans for Vercel incompatibilities
  - test-generator: Generates test cases
  - git-hygiene-subagent: Pre-commit validation
- **9 Skills**: Complete reusable knowledge block framework
  - spec-kit-monorepo: SpecKit and monorepo patterns
  - neon-sqlmodel: Neon PostgreSQL with SQLModel
  - better-auth-jwt: Authentication integration
  - mcp-crud-design: MCP tool patterns
  - chatkit-integration: ChatKit UI setup
  - docker-minikube: Docker and local K8s
  - kafka-dapr-patterns: Event-driven architecture
  - vercel-deployment: Vercel deployment guide
  - git-workflow: Git conventions and workflow

### Changed
- **Reusable Intelligence**: Complete agent/subagent/skill framework operational
- **Compliance**: ~95% constitutional compliance achieved

### Phase
- Phase II: Full-stack web application with authentication

### Notes
- All 14 subagents from constitutional requirements implemented
- All 9 skills covering all phases implemented
- Ready for Priority 4 (infra/ directory structure)

---

## [02.003.000] - 2025-12-09

### Added
- **Complete Agent Framework**: All 9 agents now implemented
- **Auth Security Agent**: Authentication and security ownership
- **AI MCP Agent**: AI agent and MCP tools design (Phase III ready)
- **Infra DevOps Agent**: Docker, K8s, Helm, Dapr, Kafka expertise
- **Testing Quality Agent**: Test strategy and quality gates
- **Docs Demo Agent**: Documentation and demo preparation
- **Vercel Deployment Agent**: Vercel-specific deployment specialist

### Changed
- **Reusable Intelligence**: Complete 9-agent framework operational
- **Development Patterns**: Agent-based development fully established

### Phase
- Phase II: Full-stack web application with authentication

### Notes
- All 9 agents from Project Constitution+Playbook Section 6 now implemented
- Each agent provides comprehensive guidance for their domain
- Ready for agent-based development across all phases
- Compliance: ~90% (up from ~85%)

---

## [02.002.000] - 2025-12-09

### Added
- **Constitutional compliance structure**: Implemented Tier 1 critical structure
- **.spec-kit/config.yaml**: Comprehensive SpecKit Plus configuration at root level
- **.claude/ directory structure**: Created agents/, subagents/, skills/, workflows/ directories
- **Root CLAUDE.md**: Comprehensive project-wide guidance for Claude Code
- **System Architect Agent**: Architecture ownership and governance
- **Backend Service Agent**: FastAPI and SQLModel implementation guidance
- **Frontend Web Agent**: Next.js and UI implementation guidance
- **Constitutional reconciliation plan**: Detailed roadmap for full compliance

### Changed
- **Project structure**: Aligned with Project Constitution+Playbook requirements
- **Reusable Intelligence**: Established agent-based development framework

### Phase
- Phase II: Full-stack web application with authentication

### Notes
- This is a MINOR version bump (new feature: constitutional compliance structure)
- Tier 1 critical structure complete per reconciliation plan
- Tier 2 (specs/ reorganization) and Tier 3 (cleanup) pending

---

## [02.001.000] - 2025-12-09

### Added
- **Versioning system**: Implemented semantic versioning scheme (MAJOR.MINOR.PATCH)
- **Version display**: Added version number to bottom right of login page
- **Version tracking**: Created VERSION file for version tracking
- **Version governance**: Added versioning rules to project constitution
- **CHANGELOG**: Created this changelog to track version history

### Changed
- **Constitution**: Updated Project Constitution+Playbook with versioning scheme (Section 13)

### Phase
- Phase II: Full-stack web application with authentication

### Notes
- Initial version number: 02.001.000
- MAJOR 02 represents Phase II (web app with authentication)
- MINOR 001 represents first feature-complete version of Phase II
- PATCH 000 represents initial release

---

## Previous Work (Pre-versioning)

### Phase II Implementation
- Next.js 14 frontend with App Router
- Better Auth integration with email/password and Google OAuth
- Neon PostgreSQL database
- Protected routes with middleware
- Login/signup pages with futuristic design
- FastAPI backend (in progress)
- Task management UI (in progress)

### Phase I Implementation
- Console-based Python todo application
- In-memory task storage
- Basic CRUD operations

---

## Version History

| Version      | Date       | Phase     | Description                          |
|--------------|------------|-----------|--------------------------------------|
| 05.11.000    | 2025-12-17 | Phase V   | FreeRTOS MQTT task, stability fix    |
| 05.10.007    | 2025-12-16 | Phase V   | ESP32 LCD scroll, MQTT task edit     |
| 05.10.006    | 2025-12-15 | Phase V   | MQTT sync on task update             |
| 05.001.000   | 2025-12-11 | Phase V   | Kafka + Dapr event-driven local      |
| 04.001.000   | 2025-12-10 | Phase IV  | Docker + K8s + Helm deployment       |
| 03.001.000   | 2025-12-10 | Phase III | AI chatbot MCP tools MVP             |
| 02.004.000   | 2025-12-10 | Phase II  | 14 subagents, 9 skills complete      |
| 02.001.000   | 2025-12-09 | Phase II  | Versioning system implementation     |

