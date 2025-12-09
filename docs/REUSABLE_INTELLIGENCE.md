# Reusable Intelligence Opportunities

This document identifies opportunities to create sub-agents and reusable tasks, aligning with the "Reusable Intelligence" bonus points for Hackathon II. By formalizing these, we enhance the project's adherence to Spec-Driven Development, streamline workflows, and centralize constitutional enforcement.

---

## 1. Spec-Driven Workflow Automation Sub-Agent

**Purpose**: To guide and automate the creation and management of specifications, plans, tasks, ADRs, and PHRs, ensuring strict adherence to Spec-Driven Development principles and templates.

**Core Idea**: Encapsulate the invocation and best practices of SpecKit-like commands into callable, reusable tasks.

**Example Reusable Tasks**:

*   **`create_spec(feature_name: str, phase: int, template: str = "default")`**:
    *   **Description**: Automates the creation of a new feature specification (`spec.md`) within the correct phase directory, utilizing a specified template.
    *   **Benefit**: Ensures consistent spec formatting and location, reduces manual setup.

*   **`generate_plan(spec_path: str)`**:
    *   **Description**: Automates the generation of an implementation plan (`plan.md`) based on a given feature specification.
    *   **Benefit**: Streamlines the technical design phase, ensuring all plans are linked to approved specs.

*   **`generate_tasks(plan_path: str)`**:
    *   **Description**: Automates the creation of a detailed task list (`tasks.md`) from an implementation plan.
    *   **Benefit**: Provides granular, actionable steps for AI agents and human developers, linked directly to the plan.

*   **`record_adr(title: str, decision_context: str, options_considered: list, decision: str, consequences: str)`**:
    *   **Description**: Formalizes the process of recording an Architectural Decision Record, prompting for all necessary details.
    *   **Benefit**: Centralizes architectural knowledge, captures rationale, and improves traceability of significant decisions.

*   **`record_phr(prompt_text: str, agent_response: str, stage: str, feature_name: str = "general")`**:
    *   **Description**: Automates the creation of Prompt History Records, ensuring all interactions are logged for traceability and learning.
    *   **Benefit**: Essential for AI-driven development, providing a clear audit trail of agent interactions and decisions.

---

## 2. Constitutional Guardian Sub-Agent

**Purpose**: To actively monitor and enforce the project's constitutional principles, providing alerts and guidance to prevent deviations and ensure adherence to established rules.

**Core Idea**: Convert the "Constitutional Enforcement Duties" (currently embedded in the main agent's logic) into explicit, callable functions that can be reused and potentially integrated into pre-commit hooks or automated checks.

**Example Reusable Tasks**:

*   **`check_phase_gate(current_phase_num: int, target_phase_num: int, feature_context: str)`**:
    *   **Description**: Verifies that a requested feature or action aligns with the current hackathon phase, invoking the relevant phase gate script (`scripts/check-phase-N-complete.sh`).
    *   **Benefit**: Strictly enforces `Principle I: Phase Boundaries Are HARD GATES`, preventing scope creep.

*   **`enforce_documentation_first(tool_name: str, docs_url: str)`**:
    *   **Description**: Reminds the user to read documentation for new tools and prompts them to complete the `docs/BEFORE_NEW_TOOL.md` checklist.
    *   **Benefit**: Upholds `Principle III: Read Documentation First`, saving significant debugging time.

*   **`remind_session_handoff()`**:
    *   **Description**: Prompts the user to update `docs/SESSION_HANDOFF.md` at the end of a work session.
    *   **Benefit**: Ensures `Principle IV: Context Preservation Protocol` is followed, improving session continuity.

*   **`run_feature_necessity_test(feature_name: str)`**:
    *   **Description**: Executes the interactive feature necessity test script (`scripts/check-feature-necessity.sh`) before a new feature is started.
    *   **Benefit**: Enforces `Principle VII: Value-Driven Feature Development`, ensuring only truly necessary features are implemented at the right time.

*   **`enforce_wip_limit(current_tasks_in_progress: list)`**:
    *   **Description**: Checks that only one major task is in progress at any given time, reminding the user of `Principle II: Finish One Thing Before Starting Next`.
    *   **Benefit**: Prevents context switching and ensures tasks are completed 100% before moving on.

---

## 3. Code Generation and Refinement Sub-Agent (Phase-Specific)

**Purpose**: To generate high-quality, idiomatic code snippets and complete modules based on specific instructions and project conventions, tailored to the current phase's technology stack.

**Core Idea**: Encapsulate project-specific coding patterns and best practices (from `backend/CLAUDE.md`, `frontend/CLAUDE.md`, etc.) into focused code generation capabilities.

**Example Reusable Tasks**:

*   **`generate_fastapi_crud_endpoints(model_name: str, operations: list, auth_required: bool = True)`**:
    *   **Description**: Generates a complete set of FastAPI CRUD endpoints for a given SQLModel, including authentication dependencies.
    *   **Benefit**: Ensures consistent API structure, Pydantic model usage, and adherence to security patterns.

*   **`generate_nextjs_component(component_name: str, type: "client" | "server", props: dict, logic: str)`**:
    *   **Description**: Creates a Next.js component (server or client) with specified props and basic business logic, following styling conventions.
    *   **Benefit**: Accelerates frontend development, maintains UI consistency, and applies correct Next.js rendering patterns.

*   **`create_sqlmodel_schema(table_name: str, fields: dict, relationships: list = None)`**:
    *   **Description**: Generates a SQLModel class definition with appropriate fields, types, and relationships.
    *   **Benefit**: Ensures data model consistency and type safety across the backend.

---

## 4. Testing and Verification Sub-Agent

**Purpose**: To automate the execution and analysis of tests, provide clear feedback on test outcomes, and assist in identifying and resolving test failures.

**Core Idea**: Centralize the testing process, making it easily invokable and interpretable, reducing the manual effort of running and debugging tests.

**Example Reusable Tasks**:

*   **`run_all_backend_tests()`**:
    *   **Description**: Executes all backend (pytest) unit and integration tests.
    *   **Benefit**: Provides a quick, comprehensive check of backend functionality.

*   **`run_specific_backend_tests(test_path: str)`**:
    *   **Description**: Runs tests for a specified file or directory in the backend.
    *   **Benefit**: Allows for targeted testing during iterative development.

*   **`run_all_frontend_tests()`**:
    *   **Description**: Executes all frontend (Jest) tests.
    *   **Benefit**: Ensures frontend component and logic integrity.

*   **`analyze_test_output(raw_output: str)`**:
    *   **Description**: Parses raw test output to highlight failures, errors, and coverage reports.
    *   **Benefit**: Simplifies test result interpretation, quickly pinpointing problem areas.

*   **`suggest_fix_from_test_failure(error_message: str, file_context: str)`**:
    *   **Description**: Based on a test failure message and relevant code context, suggests potential solutions or areas to investigate.
    *   **Benefit**: Accelerates debugging and reduces the time spent resolving test issues.

---
