---
name: cloud-native-blueprint
description: Cloud-native deployment patterns for Kubernetes, CI/CD, and Dapr. Use when deploying to AKS/DOKS, setting up GitHub Actions pipelines, configuring Helm charts, or implementing event-driven architecture with Dapr.
---

# Cloud-Native Blueprint

## CI/CD Pipeline (GitHub Actions)

### CI Workflow
```yaml
name: CI
on:
  push:
    branches: [main]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build and push images
        run: |
          echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin
          docker build -t ghcr.io/${{ github.repository }}/backend:latest -f infra/docker/backend.Dockerfile .
          docker push ghcr.io/${{ github.repository }}/backend:latest
```

### CD Workflow
```yaml
name: CD
on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]
jobs:
  deploy:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    steps:
      - uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      - run: |
          az aks get-credentials --resource-group $RG --name $CLUSTER
          helm upgrade --install app ./infra/helm/chart
          kubectl rollout restart deployment/backend deployment/frontend
```

## Helm Chart Structure

```
helm/app/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── configmap.yaml
    ├── secrets.yaml
    └── ingress.yaml
```

## Dapr Components

### Pub/Sub (Kafka/Redpanda)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
spec:
  type: pubsub.kafka
  metadata:
    - name: brokers
      value: "broker:9092"
    - name: authType
      value: "password"
```

### State Store
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
spec:
  type: state.postgresql
  metadata:
    - name: connectionString
      secretKeyRef:
        name: db-secret
        key: url
```

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Pods not pulling new images | Add `kubectl rollout restart` after helm upgrade |
| CORS errors | Add frontend URL to backend allowed origins |
| Auth cookies not working | Check `useSecureCookies` matches protocol (http/https) |
| Dapr sidecar not injecting | Add annotations: `dapr.io/enabled: "true"` |

## Quick Commands

```bash
# AKS login
az aks get-credentials --resource-group RG --name CLUSTER

# Deploy with Helm
helm upgrade --install app ./chart -f values.yaml

# Restart pods
kubectl rollout restart deployment/backend

# Check Dapr
dapr status -k
```

See `references/` for detailed AKS setup and troubleshooting guides.
