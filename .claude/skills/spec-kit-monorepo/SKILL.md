---
name: spec-kit-monorepo
description: SpecKit Plus configuration for monorepo projects. Use when managing specifications, phases, and task planning in spec-driven development.
---

# SpecKit Monorepo

## Configuration

```yaml
# .spec-kit/config.yaml
project:
  name: evolution-todo
  type: monorepo
  version: "05.10.005"

phases:
  - name: phase-1
    status: complete
  - name: phase-2
    status: complete
  - name: phase-3
    status: complete
  - name: phase-4
    status: complete
  - name: phase-5
    status: complete

features:
  - tasks-core
  - auth-and-users
  - chat-agent
  - recurring-tasks
```

## Slash Commands

- `/sp.specify` - Create feature specification
- `/sp.plan` - Create implementation plan
- `/sp.tasks` - Generate task list
- `/sp.clarify` - Clarify spec ambiguities
- `/sp.adr` - Create Architecture Decision Record
- `/sp.analyze` - Analyze consistency
- `/sp.git.commit_pr` - Autonomous git workflow

## Directory Structure

```
specs/
├── constitution.md     # Project principles
├── phases/             # Phase specifications
├── features/           # Feature specifications
├── api/                # API specifications
├── database/           # Schema specifications
└── tasks/              # Task lists
```

## Usage Pattern

1. Create spec: `/sp.specify "Feature: X"`
2. Plan implementation: `/sp.plan`
3. Generate tasks: `/sp.tasks`
4. Implement from spec
5. Validate against spec
