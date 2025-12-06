#!/bin/bash
# scripts/check-phase-5-complete.sh
# Verifies Phase V is 100% complete

echo "🚪 Phase V Final Completion Check"
echo ""

PHASE_5_COMPLETE=true

# Check 1: Specs exist
if [ ! -d "specs/phase-5" ]; then
    echo "❌ Missing: specs/phase-5/ directory"
    PHASE_5_COMPLETE=false
fi

# Check 2: Dapr components exist
if [ ! -d "dapr-components" ]; then
    echo "⚠️  Warning: dapr-components/ directory not found"
fi

# Check 3: Capstone exists
if [ ! -f "specs/phase-5/capstone.md" ]; then
    echo "❌ Missing: specs/phase-5/capstone.md"
    PHASE_5_COMPLETE=false
fi

# Check 4: Manual verification
echo ""
echo "📝 Manual Checks (verify yourself):"
echo "  [ ] All Intermediate features working (priorities, tags, search, sort)"
echo "  [ ] All Advanced features working (recurring tasks, due dates, reminders)"
echo "  [ ] Kafka topics created and events flowing"
echo "  [ ] Dapr pub/sub working (events published/consumed)"
echo "  [ ] Dapr state store working (conversation state)"
echo "  [ ] Dapr cron binding working (reminder checks)"
echo "  [ ] DOKS cluster deployed and accessible"
echo "  [ ] CI/CD pipeline working (push to main → deploy)"
echo "  [ ] Demo video recorded (< 90 seconds)"
echo "  [ ] Submitted before Jan 18, 11:59 PM"
echo ""
echo "📝 Bonus Features (optional):"
echo "  [ ] Urdu language support (+100 points)"
echo "  [ ] Voice commands (+200 points)"
echo "  [ ] Reusable intelligence (subagents/skills) (+200 points)"
echo "  [ ] Cloud-Native blueprints (+200 points)"
echo ""

if [ "$PHASE_5_COMPLETE" = false ]; then
    echo "❌ GATE FAILED: Phase V is not complete"
    echo "Complete all checks above"
    exit 1
else
    echo "✅ GATE PASSED: Phase V appears complete"
    echo ""
    echo "🎉 Congratulations! All phases complete!"
    exit 0
fi

