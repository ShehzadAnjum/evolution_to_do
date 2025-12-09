# Skill: SpecKit Plus Monorepo

## Overview

This skill captures knowledge about how specs, .spec-kit configuration, and monorepo structure relate in Spec-Driven Development.

## Core Concepts

### SpecKit Plus Configuration

**File**: `.spec-kit/config.yaml`

Defines:
- Monorepo structure (frontend, backend, infra)
- Phase definitions and boundaries
- Feature specifications
- Agent/subagent/skill registry

### Directory Structure

```
project/
├── .spec-kit/
│   └── config.yaml         # Master configuration
├── specs/
│   ├── constitution.md     # Project governance
│   ├── phases/             # Phase specifications
│   ├── features/           # Feature specifications
│   ├── api/                # API contracts
│   ├── database/           # Schema specifications
│   ├── tasks/              # Task breakdowns
│   └── ui/                 # UI specifications
├── backend/                # FastAPI app
├── frontend/               # Next.js app
└── infra/                  # Docker, K8s, Helm
```

### SpecKit Commands

| Command | Purpose |
|---------|---------|
| `/sp.constitution` | Update constitution |
| `/sp.specify` | Create feature spec |
| `/sp.plan` | Create implementation plan |
| `/sp.tasks` | Generate task list |
| `/sp.clarify` | Clarify ambiguities |
| `/sp.adr` | Record architectural decision |
| `/sp.phr` | Record prompt history |
| `/sp.analyze` | Analyze spec consistency |
| `/sp.git.commit_pr` | Git workflow |

## Key Patterns

### Spec-First Development

```markdown
1. User: /sp.specify "Feature: Task filtering"
   → Creates specs/features/task-filtering.md

2. User: /sp.plan
   → Creates implementation plan

3. User: /sp.tasks
   → Creates tasks/feature-task-filtering.md

4. Claude: Implements from spec
   → Code matches specification exactly
```

### Phase Boundaries

```yaml
# .spec-kit/config.yaml
phases:
  phase-1:
    name: Console App
    technologies: [python, in-memory]
    constraints: no-persistence, cli-only
    
  phase-2:
    name: Web App
    technologies: [nextjs, fastapi, neon, better-auth]
    constraints: jwt-auth, user-isolation
```

### Feature Registry

```yaml
features:
  tasks-core:
    spec: specs/features/tasks-core.md
    phases: [1, 2, 3, 4, 5]
    
  auth-and-users:
    spec: specs/features/auth-and-users.md
    phases: [2, 3, 4, 5]
```

## Anti-Patterns

### ❌ Manual Spec Creation

```bash
# DON'T: Create specs manually
touch specs/features/new-feature.md
vim specs/features/new-feature.md
```

### ✅ Use SpecKit Commands

```bash
# DO: Use SpecKit commands
/sp.specify "Feature: New feature description"
```

### ❌ Ignoring Phase Boundaries

```python
# DON'T: Implement Phase III in Phase II
from openai import OpenAI  # This is Phase III!
```

### ✅ Respect Phase Constraints

```python
# DO: Check current phase first
# specs/phases/phase-2.md says: No AI features
# Therefore: Don't import OpenAI in Phase II
```

## Validation Checklist

- [ ] `.spec-kit/config.yaml` exists and is valid YAML
- [ ] All features in config have corresponding spec files
- [ ] Spec files follow standard template
- [ ] Phase boundaries are enforced
- [ ] Tasks reference their parent specs
- [ ] Constitution is the source of truth

## Related Skills

- `neon-sqlmodel.md` - Database patterns
- `better-auth-jwt.md` - Auth configuration
- `git-workflow.md` - Version control

---

**Part of**: Evolution of Todo Reusable Intelligence
**Phase**: All phases
**Last Updated**: 2025-12-10
