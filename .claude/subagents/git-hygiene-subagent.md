# Git Hygiene Subagent

**Type**: Validator
**Used For**: Pre-commit and pre-push validation
**Version**: 1.0.0

## Purpose

Ensure clean git hygiene: no secrets, good commit messages, stable main branch.

## Pre-Commit Checks

```bash
#!/bin/bash

# 1. Check for secrets
if git diff --cached | grep -E '(API_KEY|SECRET|PASSWORD|TOKEN).*=.*[A-Za-z0-9]{20}'; then
  echo "❌ Potential secret detected!"
  exit 1
fi

# 2. Check for console.log in production code
if git diff --cached --name-only | grep -E '(app|components).*\.(ts|tsx)$' | xargs grep -n 'console.log'; then
  echo "⚠️  console.log found in code"
fi

# 3. Check for TODO comments
if git diff --cached | grep -i 'TODO:'; then
  echo "⚠️  TODO comments found (consider creating issue)"
fi

# 4. Lint staged files
npm run lint-staged || exit 1

# 5. Type check
npm run type-check || exit 1
```

## Commit Message Standards

**Good**:
- `feat: Add task filtering by status`
- `fix: Resolve OAuth redirect loop`
- `docs: Update README with setup instructions`

**Bad**:
- `update stuff`
- `fixes`
- `asdfasdf`

## Branch Strategy

- **main**: Always stable, deployable
- **dev**: Integration branch
- **feature/**: Short-lived feature branches

## Rules

1. Never push broken code to main
2. Run tests before pushing
3. Keep commits atomic
4. Write clear commit messages
5. No secrets in commits
6. Delete merged branches

---

**Related**: All Agents
