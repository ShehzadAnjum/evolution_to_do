#!/bin/bash
# scripts/check-phase-1-complete.sh
# Blocks Phase II start until Phase I is 100% complete

echo "🚪 Phase I → Phase II Gate Check"
echo ""

PHASE_1_COMPLETE=true

# Check 1: Specs exist
if [ ! -d "specs/001-phase1-console-todo" ] && [ ! -d "specs/phase-1" ]; then
    echo "❌ Missing: specs/001-phase1-console-todo/ or specs/phase-1/ directory"
    PHASE_1_COMPLETE=false
fi

# Check 2: Python source exists
if [ ! -d "backend/src" ]; then
    echo "❌ Missing: backend/src/ directory"
    PHASE_1_COMPLETE=false
fi

# Check 3: Capstone exists
if [ ! -f "specs/001-phase1-console-todo/capstone.md" ]; then
    echo "❌ Missing: specs/001-phase1-console-todo/capstone.md"
    PHASE_1_COMPLETE=false
fi

# Check 4: Tests pass
if [ -d "backend" ]; then
    cd backend
    if ! uv run pytest --tb=no -q > /dev/null 2>&1; then
        echo "❌ Tests failing: Run 'uv run pytest' in backend/ to see errors"
        PHASE_1_COMPLETE=false
    fi
    cd ..
fi

# Check 5: CLAUDE.md exists
if [ ! -f "CLAUDE.md" ]; then
    echo "❌ Missing: CLAUDE.md"
    PHASE_1_COMPLETE=false
fi

# Check 6: GitHub repo is public
if [ -d ".git" ]; then
    REMOTE=$(git remote get-url origin 2>/dev/null)
    if [ -z "$REMOTE" ]; then
        echo "⚠️  Warning: No git remote configured"
    fi
else
    echo "❌ Missing: .git directory (not a git repo)"
    PHASE_1_COMPLETE=false
fi

# Check 7: Submission form completed
echo ""
echo "📝 Manual Checks (verify yourself):"
echo "  [ ] All 5 Basic operations work (Add, Delete, Update, View, Mark Complete)"
echo "  [ ] Demo video recorded (< 90 seconds)"
echo "  [ ] Form submitted at https://forms.gle/CQsSEGM3GeCrL43c8"
echo ""

if [ "$PHASE_1_COMPLETE" = false ]; then
    echo "❌ GATE FAILED: Phase I is not complete"
    echo "Complete all checks above before starting Phase II"
    exit 1
else
    echo "✅ GATE PASSED: Phase I appears complete"
    echo ""
    echo "Proceed to Phase II only after manual checks completed"
    exit 0
fi

