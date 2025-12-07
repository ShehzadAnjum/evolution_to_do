#!/bin/bash
# scripts/weekly-cleanup.sh
# Weekly repository maintenance

echo "🧹 Weekly Repository Cleanup"
echo ""

# 1. Delete merged branches
echo "1. Checking for merged branches..."
git fetch --prune
MERGED=$(git branch --merged main | grep -v "main" | grep -v "\*")
if [ -n "$MERGED" ]; then
    echo "Found merged branches:"
    echo "$MERGED"
    read -p "Delete these? (yes/no): " DELETE
    if [ "$DELETE" = "yes" ]; then
        echo "$MERGED" | xargs git branch -d
        echo "✅ Deleted merged branches"
    fi
else
    echo "✅ No merged branches to delete"
fi
echo ""

# 2. Check for uncommitted changes
echo "2. Checking for uncommitted changes..."
if [ -n "$(git status --short)" ]; then
    echo "⚠️  Warning: Uncommitted changes found"
    git status --short
    echo "Commit or stash before weekend"
else
    echo "✅ No uncommitted changes"
fi
echo ""

# 3. Check repository size
echo "3. Checking repository size..."
REPO_SIZE=$(du -sh .git 2>/dev/null | cut -f1)
echo "Repository size: $REPO_SIZE"
if [ -n "$REPO_SIZE" ]; then
    REPO_SIZE_KB=$(du -s .git 2>/dev/null | cut -f1)
    if [ -n "$REPO_SIZE_KB" ] && [ "$REPO_SIZE_KB" -gt 100000 ]; then
        echo "⚠️  Warning: Repository larger than 100MB"
        echo "Consider cleaning large files"
    fi
fi
echo ""

# 4. Check for docs at root
echo "4. Checking for documentation sprawl..."
ROOT_DOCS=$(ls *.md 2>/dev/null | grep -v "README.md" | grep -v "CLAUDE.md" | grep -v "GEMINI.md" | grep -v "QUICK_REFERENCE.md" || true)
if [ -n "$ROOT_DOCS" ]; then
    echo "⚠️  Warning: Extra markdown files at root:"
    echo "$ROOT_DOCS"
    echo "Move to docs/ directory"
else
    echo "✅ Root directory clean"
fi
echo ""

# 5. Update PROJECT_STATUS
echo "5. Update PROJECT_STATUS.md"
if [ -f "docs/PROJECT_STATUS.md" ]; then
    echo "Last updated: $(grep "Updated:" docs/PROJECT_STATUS.md | head -1 || echo "Unknown")"
    read -p "Update now? (yes/no): " UPDATE
    if [ "$UPDATE" = "yes" ]; then
        ${EDITOR:-vim} docs/PROJECT_STATUS.md
    fi
else
    echo "⚠️  Warning: docs/PROJECT_STATUS.md not found"
fi
echo ""

echo "✅ Weekly cleanup complete"

