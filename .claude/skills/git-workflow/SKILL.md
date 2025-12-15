---
name: git-workflow
description: Git workflow patterns for Evolution Todo project. Use when committing changes, creating branches, or managing version control.
---

# Git Workflow

## Commit Message Format

```
type(scope): description

[optional body]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## Branch Strategy

- `main` - Production-ready code
- `feature/*` - New features
- `fix/*` - Bug fixes

## Common Commands

```bash
# Status check
git status
git log --oneline -5

# Feature branch
git checkout -b feature/chatkit-integration

# Commit with message
git commit -m "feat(chat): implement ChatKit UI"

# Create safety tag
git tag -a v1.0.0-pre-feature -m "Safety checkpoint"

# Revert to tag
git checkout v1.0.0-pre-feature
```

## Pre-Commit Hooks

This project has pre-commit hooks that check:
- SESSION_HANDOFF.md was updated recently
- No secrets in committed files
