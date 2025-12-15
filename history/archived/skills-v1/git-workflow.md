# Skill: Git Workflow

## Overview

This skill captures Git workflow patterns for the Evolution of Todo project, including branching strategy, commit conventions, and PR workflows.

## Core Concepts

### Branch Strategy

```
main                 (production - protected)
  │
  ├── develop        (integration - optional)
  │     │
  │     ├── feature/task-crud
  │     ├── feature/auth-oauth
  │     └── fix/login-redirect
  │
  └── hotfix/critical-bug  (direct to main)
```

### Branch Naming

| Type | Pattern | Example |
|------|---------|---------|
| Feature | `feature/<short-description>` | `feature/task-crud` |
| Bug fix | `fix/<issue-or-description>` | `fix/oauth-redirect` |
| Hotfix | `hotfix/<critical-issue>` | `hotfix/auth-bypass` |
| Release | `release/<version>` | `release/02.003.000` |
| Docs | `docs/<topic>` | `docs/api-reference` |

## Commit Conventions

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

| Type | Description |
|------|-------------|
| `feat` | New feature |
| `fix` | Bug fix |
| `docs` | Documentation |
| `style` | Formatting (no code change) |
| `refactor` | Code restructure (no feature/fix) |
| `test` | Adding/fixing tests |
| `chore` | Build, dependencies, config |

### Scopes

| Scope | Description |
|-------|-------------|
| `auth` | Authentication |
| `api` | Backend API |
| `ui` | Frontend UI |
| `db` | Database |
| `infra` | Infrastructure |
| `deps` | Dependencies |

### Examples

```bash
# Feature
feat(api): add task CRUD endpoints

Implements REST endpoints for task management:
- GET /api/tasks - list user tasks
- POST /api/tasks - create task
- PATCH /api/tasks/{id} - update task
- DELETE /api/tasks/{id} - delete task

Closes #42

# Bug fix
fix(auth): resolve OAuth redirect loop

The redirect URI was not including the full path,
causing infinite redirects after Google login.

Updated trustedOrigins to include *.vercel.app

# Docs
docs: update API reference with examples

# Chore
chore(deps): update better-auth to 1.2.3
```

## Workflow Commands

### Starting Work

```bash
# Ensure main is up to date
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/task-crud

# Start working...
```

### During Development

```bash
# Stage changes
git add -A

# Commit with message
git commit -m "feat(api): add task list endpoint"

# Push to remote
git push -u origin feature/task-crud
```

### Creating PR

```bash
# Ensure up to date with main
git fetch origin
git rebase origin/main

# Push (may need force after rebase)
git push -f origin feature/task-crud

# Create PR via GitHub CLI
gh pr create --title "feat(api): add task CRUD endpoints" --body "..."
```

### Merging

```bash
# After PR approval
gh pr merge --squash

# Or via GitHub UI
# Use "Squash and merge" for clean history
```

## Pre-Commit Checks

### Git Hygiene Subagent Checklist

```markdown
- [ ] No secrets in staged files
- [ ] Commit message follows convention
- [ ] Tests pass
- [ ] Build succeeds
- [ ] SESSION_HANDOFF.md updated (if applicable)
- [ ] No console.log/print statements (unless intentional)
```

### Automated Checks

```bash
# .git/hooks/pre-commit
#!/bin/bash

# Check for secrets
if git diff --cached --name-only | xargs grep -l "password\|secret\|api_key" 2>/dev/null; then
  echo "⚠️ Potential secrets detected!"
  exit 1
fi

# Run tests
npm test

# Lint
npm run lint
```

## Semantic Versioning

### Version Format

```
MM.NNN.PPP

MM  = Major version (Phase)
NNN = Minor version (Feature)
PPP = Patch version (Fix)
```

### Version Bumping

```bash
# Read current version
cat VERSION

# Update version
echo "02.004.000" > VERSION

# Update changelog
cat >> CHANGELOG.md << 'EOF'

## [02.004.000] - 2025-12-10

### Added
- Task CRUD API endpoints
