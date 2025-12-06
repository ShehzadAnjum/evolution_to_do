# Implementation Plan: Phase I Console Todo Application

**Branch**: `001-phase1-console-todo` | **Date**: 2025-12-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-phase1-console-todo/spec.md`

## Summary

Build a command-line todo application with 5 core operations (Add, View, Mark Complete, Update, Delete) using Python 3.13+ and UV package manager. The application uses in-memory storage (session-only persistence) and a menu-driven interface for maximum discoverability.

**Primary Requirements**:
- Menu-driven CLI interface with all operations accessible
- Task entity with id, title, description, and completion status
- In-memory storage using Python data structures
- Clear error handling and user feedback

**Technical Approach**:
- Pure Python with standard library only (no external runtime dependencies)
- Dataclass for Task model with validation
- Dictionary-based TaskStore for O(1) lookups
- Modular architecture for future reusability

## Technical Context

**Language/Version**: Python 3.13+ (specified in user input)
**Package Manager**: UV (for virtual environment and dependency management)
**Primary Dependencies**: Standard library only (no external runtime dependencies)
**Dev Dependencies**: pytest, pytest-cov (testing only)
**Storage**: In-memory (Dict[int, Task]) - session-only, no persistence
**Testing**: pytest with coverage reporting
**Target Platform**: Cross-platform console (Linux, macOS, Windows)
**Project Type**: Single project (console application)
**Performance Goals**: Instant response (<100ms for all operations)
**Constraints**: Standard library only, no database, no external services
**Scale/Scope**: Single user, 100+ tasks without degradation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Phase Boundaries | ✅ PASS | Phase I only - no persistence, no web, no AI |
| II. Complete Before Proceeding | ✅ PASS | Single feature focus |
| III. Documentation-First | ✅ PASS | Spec complete before planning |
| IV. Context Preservation | ✅ PASS | PHR records maintained |
| V. Repository Hygiene | ✅ PASS | Clean structure, .gitignore configured |
| VI. Spec-Driven Development | ✅ PASS | Following /sp.specify → /sp.plan flow |
| VII. Value-Driven Features | ✅ PASS | All features deliver immediate value |
| VIII. Quality Over Speed | ✅ PASS | Tests planned, clean architecture |
| IX. Reusable Intelligence | ✅ PASS | Reusability review planned (see below) |

### Reusability Opportunities (Principle IX)

| Component | Reuse Potential | Extraction Target |
|-----------|-----------------|-------------------|
| Task dataclass | High - usable in all phases | `lib/models/task.py` |
| TaskStore pattern | High - generic CRUD store | `lib/stores/base_store.py` |
| Menu system | Medium - CLI pattern | `lib/cli/menu.py` |
| Input validation | High - reusable validators | `lib/validators/` |
| Output formatters | Medium - display patterns | `lib/formatters/` |

## Project Structure

### Documentation (this feature)

```text
specs/001-phase1-console-todo/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 research output
├── data-model.md        # Entity definitions
├── quickstart.md        # Setup and run instructions
├── contracts/           # Interface contracts
│   └── cli-interface.md # CLI input/output contract
├── checklists/          # Quality checklists
│   └── requirements.md  # Spec quality validation
└── tasks.md             # Task list (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point with main loop
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task dataclass
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_store.py    # In-memory task storage
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── menu.py          # Menu display and navigation
│   │   ├── handlers.py      # Operation handlers
│   │   └── formatters.py    # Output formatting utilities
│   └── lib/                 # Reusable components (Principle IX)
│       ├── __init__.py
│       └── validators.py    # Input validation utilities
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_task.py
│   │   └── test_task_store.py
│   └── integration/
│       ├── __init__.py
│       └── test_cli.py
├── pyproject.toml           # UV project configuration
└── README.md                # Backend-specific documentation
```

**Structure Decision**: Single project layout under `backend/` to prepare for Phase II expansion (when `frontend/` will be added). This matches the "web application" structure pattern while keeping Phase I focused.

## Complexity Tracking

> No violations detected - simplest viable structure selected.

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| Storage | In-memory Dict | Simplest for Phase I, no persistence needed |
| UI | Text menu | Most discoverable, no dependencies |
| Architecture | 3-layer (CLI/Service/Model) | Clean separation without over-engineering |
| Testing | pytest only | Standard, simple, sufficient |

## Implementation Phases

### Phase 0: Research ✅
- Python 3.13+ features (dataclasses, type hints)
- UV package manager best practices
- Menu-driven CLI patterns

### Phase 1: Design ✅
- Data model (Task entity)
- CLI interface contract
- Quickstart guide

### Phase 2: Tasks (via /sp.tasks)
- Task breakdown by user story
- Dependency ordering
- Parallel opportunities identified

## Success Verification

After implementation, verify against spec success criteria:

| Criterion | Verification Method |
|-----------|---------------------|
| SC-001: 60s workflow | Manual timing test |
| SC-002: 95% first-attempt | User testing |
| SC-003: Self-correcting errors | Error message review |
| SC-004: Instant response | Subjective testing |
| SC-005: 100+ tasks | Load test script |
| SC-006: 10s discoverability | New user test |
| SC-007: 90s demo | Record and time |
