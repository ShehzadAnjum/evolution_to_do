#!/bin/bash
# scripts/check-phase-2-complete.sh
# Blocks Phase III start until Phase II is 100% complete

echo "🚪 Phase II → Phase III Gate Check"
echo ""

PHASE_2_COMPLETE=true

# Check 1: Specs exist
if [ ! -d "specs/phase-2" ]; then
    echo "❌ Missing: specs/phase-2/ directory"
    PHASE_2_COMPLETE=false
fi

# Check 2: Backend API exists
if [ ! -d "backend/src/api" ]; then
    echo "❌ Missing: backend/src/api/ directory"
    PHASE_2_COMPLETE=false
fi

# Check 3: Frontend exists
if [ ! -d "frontend" ]; then
    echo "❌ Missing: frontend/ directory"
    PHASE_2_COMPLETE=false
fi

# Check 4: Capstone exists
if [ ! -f "specs/phase-2/capstone.md" ]; then
    echo "❌ Missing: specs/phase-2/capstone.md"
    PHASE_2_COMPLETE=false
fi

# Check 5: Backend tests pass (if tests exist)
if [ -d "backend/tests" ]; then
    cd backend
    if ! uv run pytest --tb=no -q > /dev/null 2>&1; then
        echo "⚠️  Warning: Backend tests failing (run 'uv run pytest' to see errors)"
    fi
    cd ..
fi

# Check 6: Frontend builds (if package.json exists)
if [ -f "frontend/package.json" ]; then
    cd frontend
    if ! npm run build > /dev/null 2>&1; then
        echo "⚠️  Warning: Frontend build failing (run 'npm run build' to see errors)"
    fi
    cd ..
fi

# Check 7: Deployment verification
echo ""
echo "📝 Manual Checks (verify yourself):"
echo "  [ ] Web UI deployed and accessible"
echo "  [ ] Backend API deployed and accessible"
echo "  [ ] User can signup, signin, logout"
echo "  [ ] JWT tokens working (auth header)"
echo "  [ ] User A cannot see User B's tasks"
echo "  [ ] All 5 Basic operations work in UI"
echo "  [ ] Demo video recorded (< 90 seconds)"
echo "  [ ] Submitted before Dec 14, 11:59 PM"
echo ""

if [ "$PHASE_2_COMPLETE" = false ]; then
    echo "❌ GATE FAILED: Phase II is not complete"
    echo "Complete all checks above before starting Phase III"
    exit 1
else
    echo "✅ GATE PASSED: Phase II appears complete"
    echo ""
    echo "Proceed to Phase III only after manual checks completed"
    exit 0
fi

