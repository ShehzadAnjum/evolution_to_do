# Speckit Workflow: DOs and DON'Ts Guide

**Purpose**: This guide defines what should and should NOT be included in each step of the speckit workflow, and where excluded items belong instead.

---

## 1. Constitution

### ✅ DOs - What SHALL be defined here:

- **Core principles and values** that govern all development
  - Development methodologies (e.g., TDD, small steps)
  - Quality standards (e.g., type safety, production-ready code)
  - Architectural patterns (e.g., package-style, separation of concerns)
  - Documentation standards
  - Security principles

- **Project-wide constraints** that apply to all features
  - Technology stack decisions (language, frameworks, databases)
  - Deployment targets
  - Performance requirements at project level
  - Design system basics (colors, themes, UI philosophy)

- **Governance rules** for the project
  - How to amend the constitution
  - Version control for constitution
  - Ratification and amendment dates

- **Workflow principles** (high-level)
  - The speckit flow itself (Constitution → Spec → Clarify (optional) → Plan → Tasks → Implementation → Capstone)
  - Testing strategy (what types of tests, when to use them)

### ❌ DON'Ts - What SHALL NOT be defined here (and where they belong):

- ❌ **Feature-specific requirements** → Defined in **Spec** (`spec.md`)
- ❌ **Feature-specific user stories** → Defined in **Spec** (`spec.md`)
- ❌ **Feature-specific acceptance criteria** → Defined in **Spec** (`spec.md`)
- ❌ **Feature-specific technical design** → Defined in **Plan** (`plan.md`)
- ❌ **Feature-specific data models** → Defined in **Plan** → `data-model.md`
- ❌ **Feature-specific API contracts** → Defined in **Plan** → `contracts/`
- ❌ **Feature-specific implementation tasks** → Defined in **Tasks** (`tasks.md`)
- ❌ **Feature-specific code structure** → Defined in **Plan** → Project Structure section
- ❌ **Feature-specific success metrics** → Defined in **Spec** → Success Criteria section
- ❌ **Feature-specific edge cases** → Defined in **Spec** → Edge Cases section
- ❌ **Implementation details** (file paths, function names) → Defined in **Tasks** (`tasks.md`)
- ❌ **Research findings** → Defined in **Plan** → `research.md`

---

## 2. Spec (Specification)

### ✅ DOs - What SHALL be defined here:

- **User stories** (prioritized P1, P2, P3...)
  - Plain language descriptions of user journeys
  - Why each story has its priority
  - Independent test descriptions for each story

- **Acceptance scenarios** (Given-When-Then format)
  - For each user story
  - Testable outcomes

- **Functional requirements** (FR-XXX)
  - What the system MUST do
  - Written in business/domain language
  - Technology-agnostic

- **Edge cases** (user-facing scenarios)
  - Boundary conditions
  - Error scenarios users might encounter

- **Key entities** (high-level, concept-only)
  - What entities exist (User, Account, Session)
  - What they represent conceptually
  - Relationships at domain level
  - **NOT** database schema or implementation details

- **Success criteria** (measurable, technology-agnostic outcomes)
  - User-focused metrics (e.g., "complete task in under 2 minutes")
  - Business metrics (e.g., "reduce support tickets by 50%")
  - Performance metrics from user perspective (e.g., "supports 10k concurrent users")

- **Assumptions** (if any)
  - Business assumptions
  - Domain assumptions
  - User behavior assumptions

### ❌ DON'Ts - What SHALL NOT be defined here (and where they belong):

- ❌ **Technology choices** (frameworks, libraries, databases) → Already defined in **Constitution** (if project-wide) or defined in **Plan** → Technical Context (if feature-specific)
- ❌ **Implementation approach** (how to build it) → Defined in **Plan** (`plan.md`)
- ❌ **Data model details** (tables, columns, indexes, relationships) → Defined in **Plan** → `data-model.md`
- ❌ **API contracts** (endpoints, request/response formats) → Defined in **Plan** → `contracts/`
- ❌ **File structure** (where code goes) → Defined in **Plan** → Project Structure section
- ❌ **Code organization** (modules, packages, folders) → Defined in **Plan** → Project Structure section
- ❌ **Implementation tasks** (step-by-step tasks) → Defined in **Tasks** (`tasks.md`)
- ❌ **Database schema** (SQL, migrations, types) → Defined in **Plan** → `data-model.md`
- ❌ **Technical constraints** (languages, frameworks) → Defined in **Constitution** (project-wide) or **Plan** (feature-specific)
- ❌ **Research findings** → Defined in **Plan** → `research.md`
- ❌ **Architecture decisions** → Defined in **Plan** → Technical Context and Project Structure
- ❌ **Test implementation details** (what tests to write, file paths) → Defined in **Tasks** (`tasks.md`)
- ❌ **Algorithm details** → Defined in **Plan** → Technical Context or `research.md`
- ❌ **UI/UX mockups or wireframes** → Defined in **Plan** (if technical) or separate design documents
- ❌ **Specific file paths** → Defined in **Tasks** (`tasks.md`)
- ❌ **Dependencies between tasks** → Defined in **Tasks** (`tasks.md`)

### 📝 Key Principles for Spec:

- **Written for business stakeholders**, not developers
- **Focus on WHAT and WHY**, not HOW
- **Technology-agnostic** language (avoid framework/library names unless absolutely necessary)
- **Testable requirements** (every requirement must be verifiable)

---

## 2.5. Clarify (Clarification Phase) - OPTIONAL but RECOMMENDED

**Timing**: After **Spec**, before **Plan**

### ✅ DOs - What SHALL be defined here:

- **Ambiguity detection** and resolution
  - Identify underspecified areas in the specification
  - Detect missing decision points
  - Find vague requirements that need clarification

- **Clarification questions** (maximum 5 per session)
  - Highly targeted questions that materially impact implementation
  - Questions that reduce downstream rework risk
  - Questions answerable with short answers (≤5 words) or multiple-choice options

- **Clarifications section** in `spec.md`
  - Create `## Clarifications` section if missing
  - Add session subheading: `### Session YYYY-MM-DD`
  - Record Q&A pairs: `- Q: <question> → A: <final answer>`

- **Spec updates** based on clarifications (with user consent and approval)
  - Apply clarifications to relevant spec sections immediately **after user approves each answer**
  - Update Functional Requirements if functional ambiguity resolved
  - Update User Stories if interaction/actor distinction clarified
  - Update Key Entities if data shape clarified
  - Add to Edge Cases if negative flow clarified
  - Normalize terminology across spec
  - **Note**: This is an intentional workflow step, not a "backward" modification - Clarify phase is designed to refine and update the spec based on user-approved clarifications

### ❌ DON'Ts - What SHALL NOT be defined here (and where they belong):

- ❌ **New requirements** → Should update **Spec** separately, not during clarification
- ❌ **Technical implementation decisions** → Deferred to **Plan** phase
- ❌ **Research questions** → Deferred to **Plan** → `research.md`
- ❌ **More than 5 questions per session** → Defer remaining to next session or Plan phase
- ❌ **Low-impact clarifications** → Only ask questions that materially affect architecture, data modeling, or validation
- ❌ **Speculative tech stack questions** → Unless blocking functional clarity
- ❌ **Trivial stylistic preferences** → Skip unless blocking correctness
- ❌ **Plan-level execution details** → Deferred to **Plan** phase

### 📝 Key Principles for Clarify:

- **Run BEFORE Plan** - reduces ambiguity before technical design begins
- **Maximum 5 questions** - focus on highest impact ambiguities
- **Incremental updates** - update spec after each answer, not all at once
- **Category coverage balance** - cover high-impact unresolved categories first
- **Validation after each update** - ensure no contradictory statements remain
- **Can skip** if spec is already clear or for exploratory spikes (with warning)

### 🔍 Clarification Taxonomy:

Questions should address these categories (prioritize by impact):

1. **Functional Scope & Behavior**: Core user goals, explicit out-of-scope, user roles
2. **Domain & Data Model**: Entities, attributes, relationships, identity rules, lifecycle
3. **Interaction & UX Flow**: Critical user journeys, error states, accessibility
4. **Non-Functional Quality Attributes**: Performance, scalability, reliability, security, compliance
5. **Integration & External Dependencies**: External services, data formats, protocols
6. **Edge Cases & Failure Handling**: Negative scenarios, rate limiting, conflict resolution
7. **Constraints & Tradeoffs**: Technical constraints, explicit tradeoffs
8. **Terminology & Consistency**: Canonical terms, avoided synonyms
9. **Completion Signals**: Acceptance criteria testability, Definition of Done

---

## 3. Plan (Implementation Plan)

### ✅ DOs - What SHALL be defined here:

- **Technical Context** (from constitution or feature-specific)
  - Language/version
  - Primary dependencies
  - Storage/database
  - Testing frameworks
  - Target platform
  - Project type
  - Performance goals
  - Constraints
  - Scale/scope

- **Constitution Check** (gates)
  - Validation that plan complies with constitution
  - Justifications for any violations

- **Project Structure** (source code layout)
  - Directory structure
  - File organization
  - Module boundaries
  - Entry points
  - Package structure (if applicable)

- **Complexity Tracking** (if constitution violations exist)
  - Why violations are needed
  - Why simpler alternatives were rejected

### ✅ DOs - Documents created by Plan (`/sp.plan` command):

- **`research.md`** (Phase 0 output)
  - Research findings for unknown technical details
  - Best practices for chosen technologies
  - Integration patterns
  - Resolution of all "NEEDS CLARIFICATION" from spec

- **`data-model.md`** (Phase 1 output)
  - Database schema
  - Entity relationships (at database level)
  - Indexes, constraints
  - Data types
  - Migration strategy
  - TypeScript types/interfaces

- **`contracts/`** (Phase 1 output)
  - API endpoint definitions
  - Request/response schemas
  - Error response formats
  - Authentication/authorization requirements
  - OpenAPI/Swagger specs (if applicable)

- **`quickstart.md`** (Phase 1 output)
  - How to use the feature
  - Setup instructions
  - Usage examples
  - Integration guide

- **Agent context updates** (Phase 1 - automated via scripts)
  - Update AI agent context files (Claude.md, GEMINI.md, etc.)
  - Add technology stack information from plan
  - Preserve manual additions between markers
  - Maintain reusable intelligence for future AI interactions

### ❌ DON'Ts - What SHALL NOT be defined here (and where they belong):

- ❌ **User stories** → Already defined in **Spec** (`spec.md`)
- ❌ **Functional requirements** → Already defined in **Spec** (`spec.md`)
- ❌ **Acceptance criteria** → Already defined in **Spec** (`spec.md`)
- ❌ **Success criteria** → Already defined in **Spec** (`spec.md`)
- ❌ **Implementation tasks** (step-by-step breakdown) → Defined in **Tasks** (`tasks.md`)
- ❌ **Task dependencies** → Defined in **Tasks** (`tasks.md`)
- ❌ **Task priorities** → Defined in **Tasks** (`tasks.md`)
- ❌ **Phase organization** (Setup, Foundational, User Stories) → Defined in **Tasks** (`tasks.md`)
- ❌ **Test file paths** → Defined in **Tasks** (`tasks.md`)
- ❌ **Specific function implementations** → Defined in **Implementation** (code)
- ❌ **Actual code** → Defined in **Implementation** (code files)
- ❌ **Project-wide principles** → Already defined in **Constitution**
- ❌ **Edge cases** (detailed scenarios) → Already defined in **Spec** (user-facing) or handled in **Implementation** (technical)

### 📝 Key Principles for Plan:

- **Bridges the gap** between business requirements (Spec) and implementation (Tasks)
- **Technical design** without writing code
- **Research-driven** - resolve unknowns before implementation
- **Structure-focused** - where things go, not how to build them step-by-step

---

## 4. Tasks

### ✅ DOs - What SHALL be defined here:

- **Task breakdown** (T001, T002, T003...)
  - Specific, actionable tasks
  - Exact file paths where work happens
  - Task dependencies
  - Parallel opportunities ([P] markers)
  - Story assignments ([US1], [US2]...)

- **Phase organization**
  - Phase 1: Setup (shared infrastructure)
  - Phase 2: Foundational (blocking prerequisites)
  - Phase 3+: User Stories (in priority order P1, P2, P3...)
  - Final Phase: Polish & Cross-Cutting Concerns

- **Checkpoints** between phases
  - When foundational work is complete
  - When each user story is independently testable

- **Execution order**
  - Which tasks can run in parallel
  - Which tasks depend on others
  - Which phases block other phases

- **Test tasks** (if tests were requested in spec)
  - Contract tests
  - Integration tests
  - Unit tests
  - Manual test procedures

- **Task descriptions** (what to build)
  - File paths
  - Function/component names
  - What to implement
  - What validation to add

- **Strict task format** (REQUIRED)
  - Format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
  - Checkbox: Always start with `- [ ]` (markdown checkbox)
  - Task ID: Sequential number (T001, T002, T003...) in execution order
  - [P] marker: Include ONLY if task is parallelizable (different files, no dependencies)
  - [Story] label: REQUIRED for user story phase tasks only ([US1], [US2], [US3]...)
    - Setup phase: NO story label
    - Foundational phase: NO story label
    - User Story phases: MUST have story label
    - Polish phase: NO story label
  - Description: Clear action with exact file path

- **Task organization by user story**
  - PRIMARY ORGANIZATION: Tasks grouped by user story (P1, P2, P3...)
  - Each story phase is independently testable
  - Map components (models, services, endpoints) to their story
  - Story dependencies identified (most should be independent)

### ❌ DON'Ts - What SHALL NOT be defined here (and where they belong):

- ❌ **User stories** → Already defined in **Spec** (`spec.md`) - reference only
- ❌ **Functional requirements** → Already defined in **Spec** (`spec.md`) - reference only
- ❌ **Technical architecture** → Already defined in **Plan** (`plan.md`) - reference only
- ❌ **Database schema** → Already defined in **Plan** → `data-model.md` - reference only
- ❌ **API contracts** → Already defined in **Plan** → `contracts/` - reference only
- ❌ **Research findings** → Already defined in **Plan** → `research.md` - reference only
- ❌ **Project structure decisions** → Already defined in **Plan** (`plan.md`) - follow it
- ❌ **Technology choices** → Already defined in **Constitution** or **Plan** - follow them
- ❌ **How to implement algorithms** → Defined in **Implementation** (code) or **Plan** → `research.md`
- ❌ **Actual code implementation** → Defined in **Implementation** (source files)
- ❌ **Success criteria** → Already defined in **Spec** (`spec.md`) - use for validation
- ❌ **Acceptance criteria details** → Already defined in **Spec** (`spec.md`) - reference for testing

### 📝 Key Principles for Tasks:

- **Actionable and specific** - each task should be completable independently
- **Traceable** - linked to user stories and functional requirements
- **Prioritized** - organized by story priority (P1, P2, P3...)
- **Testable** - each task produces verifiable output
- **Small steps** - each task should be completable in a reasonable time

---

## 5. Implementation (Red-Green-Refactor)

### ✅ DOs - What SHALL be defined here:

- **RED Phase** (Test-First)
  - Write tests that define desired behavior
  - Tests should FAIL initially (red)
  - Tests should be specific and testable
  - Reference acceptance criteria from Spec
  - Reference task requirements from Tasks

- **GREEN Phase** (Make Tests Pass)
  - Implement minimal code to make tests pass
  - Follow structure from Plan
  - Use contracts from Plan → `contracts/`
  - Follow data model from Plan → `data-model.md`
  - Implement in file paths specified in Tasks
  - Follow principles from Constitution

- **REFACTOR Phase** (Improve Code)
  - Improve code quality without changing behavior
  - Ensure tests still pass
  - Follow type safety requirements (Constitution)
  - Follow security requirements (Constitution)
  - Optimize performance (if needed)
  - Clean up technical debt

- **Actual source code**
  - Functions, classes, components
  - TypeScript/JavaScript files
  - Configuration files
  - Tests (unit, integration, contract)

- **Code documentation** (JSDoc, comments)
  - Public API documentation
  - Complex algorithm explanations
  - Usage examples in code

### ❌ DON'Ts - What SHALL NOT be defined here (and where they belong):

- ❌ **User stories** → Already defined in **Spec** (`spec.md`) - test against them
- ❌ **Functional requirements** → Already defined in **Spec** (`spec.md`) - implement them
- ❌ **Technical architecture** → Already defined in **Plan** (`plan.md`) - follow it
- ❌ **Database schema** → Already defined in **Plan** → `data-model.md` - implement it
- ❌ **API contracts** → Already defined in **Plan** → `contracts/` - follow them
- ❌ **Project structure** → Already defined in **Plan** (`plan.md`) - create files there
- ❌ **Technology choices** → Already defined in **Constitution** or **Plan** - use them
- ❌ **Task breakdown** → Already defined in **Tasks** (`tasks.md`) - work through them
- ❌ **Success criteria** (metrics) → Already defined in **Spec** (`spec.md`) - validate against them
- ❌ **Implementation plan changes** → Should update **Plan** if architecture changes
- ❌ **New requirements** → Should update **Spec** if requirements change
- ❌ **Constitution principles** → Already defined in **Constitution** - follow them

### 📝 Key Principles for Implementation:

- **Test-First** (TDD) - write failing tests before implementation
- **Follow the plan** - structure and contracts from Plan
- **Small increments** - complete tasks from Tasks one at a time
- **Validate continuously** - ensure code meets Spec acceptance criteria
- **Refactor safely** - maintain test coverage during refactoring

---

## 6. Reusable Intelligence (Designing Reusable Intelligence)

**Context**: This is a cross-cutting concern that runs throughout the workflow, especially during Plan phase.

### ✅ DOs - What SHALL be defined here:

- **Agent context files** (Claude.md, GEMINI.md, etc.)
  - Technology stack information extracted from plan.md
  - Project structure and conventions
  - Build and test commands
  - Recent changes and patterns
  - Language-specific guidelines

- **Agent context updates** (automated during Plan phase)
  - Run `.specify/scripts/bash/update-agent-context.sh` after plan.md completion
  - Extract new technology from current plan
  - Add only new information (preserve existing manual additions)
  - Maintain markers for manual vs. automated sections

- **Knowledge preservation** for AI agents
  - Document architectural patterns and decisions
  - Capture domain-specific conventions
  - Maintain consistency across AI interactions
  - Enable future features to benefit from past learnings

### ❌ DON'Ts - What SHALL NOT be defined here (and where they belong):

- ❌ **Feature-specific requirements** → Defined in **Spec** (`spec.md`)
- ❌ **Implementation details** → Defined in **Implementation** (source code)
- ❌ **Task breakdown** → Defined in **Tasks** (`tasks.md`)
- ❌ **Manual edits to auto-generated sections** → Will be overwritten; use designated manual sections

### 📝 Key Principles for Reusable Intelligence:

- **Automated updates** - agent context updated automatically during Plan phase
- **Preserve manual additions** - manual edits preserved between markers
- **Technology-focused** - focuses on stack, tools, patterns, not feature logic
- **Future-proofing** - enables better AI assistance in future features

---

## 7. Brownfield Adoption

**Context**: Adopting speckit workflow in existing projects (not greenfield).

### ✅ DOs - What SHALL be defined here:

- **Incremental adoption strategy**
  - Start with one feature using full speckit workflow
  - Gradually expand to more features
  - Don't require full codebase rewrite

- **Constitution creation for existing projects**
  - Extract existing principles from codebase
  - Document current technology stack choices
  - Capture implicit conventions and patterns
  - Align constitution with existing architecture

- **Feature isolation**
  - Treat each new feature as standalone speckit flow
  - Reference existing codebase in Plan phase (Technical Context)
  - Integrate with existing structure (document in Plan → Project Structure)

- **Legacy code considerations**
  - Document how new features interact with legacy code
  - Plan integration points carefully
  - May need compatibility layer or adapter patterns

### ❌ DON'Ts - What SHALL NOT be defined here (and where they belong):

- ❌ **Full codebase rewrite** → Adopt incrementally, feature by feature
- ❌ **Ignoring existing architecture** → Reference and integrate with existing structure (Plan phase)
- ❌ **Changing existing features** → Only new features follow full speckit workflow initially
- ❌ **Breaking existing functionality** → Ensure compatibility during integration (Plan → Integration section)

### 📝 Key Principles for Brownfield Adoption:

- **Incremental** - adopt one feature at a time, don't boil the ocean
- **Compatibility** - new features must work with existing codebase
- **Documentation** - document how new features integrate with legacy
- **Flexibility** - constitution may need adjustment for existing constraints

---

## 8. Capstone (Completion & Validation)

**Context**: Final validation and completion steps after Implementation phase.

### ✅ DOs - What SHALL be defined here:

- **Validation against Spec**
  - Verify all functional requirements met
  - Confirm acceptance criteria satisfied
  - Validate success criteria achieved
  - Test independent user story completion

- **Validation against Plan**
  - Verify structure matches plan.md → Project Structure
  - Confirm data model matches plan.md → `data-model.md`
  - Validate contracts match plan.md → `contracts/`
  - Check quickstart.md still accurate

- **Validation against Constitution**
  - Verify code follows all principles
  - Check type safety requirements met
  - Confirm security requirements followed
  - Validate testing strategy implemented

- **Completion checklist**
  - All tasks in tasks.md completed
  - All tests passing (if tests requested)
  - Code reviewed and approved
  - Documentation updated (quickstart.md, README, etc.)
  - Integration tests successful (if applicable)

- **Retrospective and learning**
  - Document what went well
  - Capture lessons learned
  - Update reusable intelligence (agent context) with patterns
  - Note deviations from plan and why

### ❌ DON'Ts - What SHALL NOT be defined here (and where they belong):

- ❌ **New feature development** → Start new speckit cycle (Constitution → Spec → ...)
- ❌ **Implementation of missing features** → Should have been caught in earlier phases
- ❌ **Major architecture changes** → Should have been caught in Plan phase
- ❌ **Requirement changes** → Should update Spec and re-plan if needed

### 📝 Key Principles for Capstone:

- **Validation-focused** - ensure everything meets specifications
- **Complete testing** - verify all acceptance criteria
- **Documentation** - ensure all docs are up to date
- **Learning capture** - document patterns for future features
- **Ready for production** - code must be production-ready per constitution

---

## Summary: Step Boundaries

| Concern | Constitution | Spec | Clarify | Plan | Tasks | Implementation |
|---------|-------------|------|---------|------|-------|----------------|
| **Principles & Values** | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| **Technology Stack** | ✅ (project-wide) | ❌ | ❌ | ✅ (feature-specific) | ❌ | ❌ |
| **User Stories** | ❌ | ✅ | ✅ (refine with user approval) | ❌ | ❌ | ❌ |
| **Acceptance Criteria** | ❌ | ✅ | ✅ (refine with user approval) | ❌ | ❌ | ❌ |
| **Functional Requirements** | ❌ | ✅ | ✅ (refine with user approval) | ❌ | ❌ | ❌ |
| **Success Criteria** | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| **Clarifications** | ❌ | ❌ | ✅ (updates spec) | ❌ | ❌ | ❌ |
| **Ambiguity Resolution** | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| **Technical Research** | ❌ | ❌ | ❌ | ✅ (`research.md`) | ❌ | ❌ |
| **Data Model** | ❌ | ❌ | ❌ | ✅ (`data-model.md`) | ❌ | ❌ |
| **API Contracts** | ❌ | ❌ | ❌ | ✅ (`contracts/`) | ❌ | ❌ |
| **Project Structure** | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| **Agent Context** | ❌ | ❌ | ❌ | ✅ (auto-update) | ❌ | ❌ |
| **Task Breakdown** | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Task Dependencies** | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **Source Code** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Tests** | ❌ | ❌ | ❌ | ❌ | ✅ (tasks) | ✅ (code) |
| **Validation** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ (Capstone) |

---

## Flow Dependencies

```
Constitution
    ↓ (provides principles & constraints)
Spec
    ↓ (provides requirements & user stories)
Clarify (OPTIONAL but RECOMMENDED)
    ↓ (resolves ambiguities, updates spec)
Plan
    ↓ (provides technical design & structure, updates agent context)
Tasks
    ↓ (provides step-by-step breakdown)
Implementation
    ↓ (Red-Green-Refactor cycle)
Capstone
    ↓ (validation & completion)
```

**Key Rule**: Each step can only reference or build upon previous steps. Never go backward to modify earlier steps during a later step (unless explicitly correcting an error).

**Exception - Clarify Phase**: The **Clarify phase** is an intentional workflow step designed to refine the Spec based on user-approved clarifications. Unlike error corrections, Clarify enables intentional refinement and ambiguity resolution for User Stories, Acceptance Criteria, Functional Requirements, Key Entities, and Edge Cases. Spec updates during Clarify are expected and required, not a violation of this rule. **All spec updates during Clarify must be done with user consent and approval after each clarification question is answered.**

**Distinction**: 
- **Error correction** (general exception): Fixing mistakes, typos, or factual errors discovered later
- **Clarify phase refinement** (workflow exception): Intentional refinement and ambiguity resolution with explicit user consent and approval

---

## Common Mistakes to Avoid

1. **Putting implementation details in Spec** → Move to Plan or Tasks
2. **Putting user stories in Plan** → Already in Spec, reference them
3. **Putting code structure in Spec** → Move to Plan
4. **Putting requirements in Tasks** → Already in Spec, reference them
5. **Putting research in Spec** → Move to Plan → `research.md`
6. **Putting task breakdown in Plan** → Move to Tasks
7. **Putting architecture in Constitution** → Move to Plan (unless project-wide)
8. **Putting test code in Tasks** → Tasks define test tasks, Implementation writes test code
9. **Skipping phases** → Each phase builds on the previous (especially Clarify before Plan)
10. **Mixing concerns** → Keep each step focused on its purpose
11. **Asking too many clarification questions** → Maximum 5 per session, prioritize high-impact
12. **Not updating spec during Clarify** → Update spec incrementally after each user-approved answer (with user consent)
13. **Putting new requirements in Clarify** → Clarify resolves ambiguities, doesn't add requirements
14. **Ignoring task format requirements** → Tasks must follow strict format: `- [ ] [TaskID] [P?] [Story?] Description`
15. **Skipping agent context updates** → Plan phase should update agent context files automatically
16. **Not validating in Capstone** → Must validate against Spec, Plan, and Constitution
17. **Brownfield: trying to convert everything at once** → Adopt incrementally, feature by feature

