#!/bin/bash
# Test script for Kafka + Dapr integration

set -e
export PATH="$HOME/bin:$PATH"

echo "=== Phase V: Kafka + Dapr Test ==="
echo ""

echo "1. Checking Kafka pods..."
kubectl get pods -n kafka
echo ""

echo "2. Checking Dapr status..."
dapr status -k
echo ""

echo "3. Checking app pods (backend should be 2/2)..."
kubectl get pods -n evolution-todo
echo ""

echo "4. Checking Dapr pubsub component..."
kubectl get components -n evolution-todo
echo ""

echo "5. Checking Dapr subscriptions..."
kubectl get subscriptions -n evolution-todo
echo ""

echo "6. Checking backend Dapr sidecar logs (last 10 lines)..."
kubectl logs -n evolution-todo -l app.kubernetes.io/component=backend -c daprd --tail=10
echo ""

echo "=== All checks complete ==="
echo ""
echo "To test event publishing:"
echo "  1. kubectl port-forward svc/evolution-todo-backend 8000:8000 -n evolution-todo"
echo "  2. curl -X POST http://localhost:8000/api/tasks -H 'Content-Type: application/json' -d '{\"title\":\"Test\"}'"
echo "  3. Watch logs: kubectl logs -n evolution-todo -l app.kubernetes.io/component=backend -c backend -f"
