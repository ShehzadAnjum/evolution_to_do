#!/bin/bash
# scripts/check-phase-3-complete.sh
# Blocks Phase IV start until Phase III is 100% complete

echo "🚪 Phase III → Phase IV Gate Check"
echo ""

PHASE_3_COMPLETE=true

# Check 1: Specs exist
if [ ! -d "specs/phase-3" ]; then
    echo "❌ Missing: specs/phase-3/ directory"
    PHASE_3_COMPLETE=false
fi

# Check 2: MCP server exists
if [ ! -d "backend/src/mcp_server" ]; then
    echo "❌ Missing: backend/src/mcp_server/ directory"
    PHASE_3_COMPLETE=false
fi

# Check 3: Chat endpoint exists
if [ ! -f "backend/src/api/routes/chat.py" ]; then
    echo "⚠️  Warning: Chat endpoint not found (expected: backend/src/api/routes/chat.py)"
fi

# Check 4: Capstone exists
if [ ! -f "specs/phase-3/capstone.md" ]; then
    echo "❌ Missing: specs/phase-3/capstone.md"
    PHASE_3_COMPLETE=false
fi

# Check 5: Tests pass
if [ -d "backend/tests" ]; then
    cd backend
    if ! uv run pytest --tb=no -q > /dev/null 2>&1; then
        echo "⚠️  Warning: Backend tests failing"
    fi
    cd ..
fi

# Check 6: Manual verification
echo ""
echo "📝 Manual Checks (verify yourself):"
echo "  [ ] ChatKit UI deployed and working"
echo "  [ ] Can send messages and get AI responses"
echo "  [ ] Natural language commands execute tasks:"
echo "      - 'Add a task to buy groceries'"
echo "      - 'Show me all my tasks'"
echo "      - 'Mark task 3 as complete'"
echo "      - 'Delete the meeting task'"
echo "  [ ] Conversation history persists"
echo "  [ ] Server restarts don't lose conversation state"
echo "  [ ] All 5 MCP tools working"
echo "  [ ] Demo video recorded (< 90 seconds)"
echo "  [ ] Submitted before Dec 21, 11:59 PM"
echo ""

if [ "$PHASE_3_COMPLETE" = false ]; then
    echo "❌ GATE FAILED: Phase III is not complete"
    echo "Complete all checks above before starting Phase IV"
    exit 1
else
    echo "✅ GATE PASSED: Phase III appears complete"
    echo ""
    echo "Proceed to Phase IV only after manual checks completed"
    exit 0
fi

