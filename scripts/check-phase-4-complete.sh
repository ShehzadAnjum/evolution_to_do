#!/bin/bash
# scripts/check-phase-4-complete.sh
# Blocks Phase V start until Phase IV is 100% complete

echo "🚪 Phase IV → Phase V Gate Check"
echo ""

PHASE_4_COMPLETE=true

# Check 1: Specs exist
if [ ! -d "specs/phase-4" ]; then
    echo "❌ Missing: specs/phase-4/ directory"
    PHASE_4_COMPLETE=false
fi

# Check 2: Dockerfiles exist
if [ ! -f "docker/Dockerfile.backend" ] && [ ! -f "backend/Dockerfile" ]; then
    echo "⚠️  Warning: Backend Dockerfile not found"
fi
if [ ! -f "docker/Dockerfile.frontend" ] && [ ! -f "frontend/Dockerfile" ]; then
    echo "⚠️  Warning: Frontend Dockerfile not found"
fi

# Check 3: Helm charts exist
if [ ! -d "helm/todo-app" ]; then
    echo "❌ Missing: helm/todo-app/ directory"
    PHASE_4_COMPLETE=false
fi

# Check 4: Capstone exists
if [ ! -f "specs/phase-4/capstone.md" ]; then
    echo "❌ Missing: specs/phase-4/capstone.md"
    PHASE_4_COMPLETE=false
fi

# Check 5: Manual verification
echo ""
echo "📝 Manual Checks (verify yourself):"
echo "  [ ] Docker images built for frontend and backend"
echo "  [ ] Helm charts created"
echo "  [ ] Minikube started and accessible"
echo "  [ ] Helm install successful"
echo "  [ ] Pods running (kubectl get pods shows Running)"
echo "  [ ] Application accessible on localhost"
echo "  [ ] All Phase III features working same as before"
echo "  [ ] kubectl-ai or kagent usage documented"
echo "  [ ] Demo video recorded (< 90 seconds)"
echo "  [ ] Submitted before Jan 4, 11:59 PM"
echo ""

if [ "$PHASE_4_COMPLETE" = false ]; then
    echo "❌ GATE FAILED: Phase IV is not complete"
    echo "Complete all checks above before starting Phase V"
    exit 1
else
    echo "✅ GATE PASSED: Phase IV appears complete"
    echo ""
    echo "Proceed to Phase V only after manual checks completed"
    exit 0
fi

