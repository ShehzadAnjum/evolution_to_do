# Skill: Azure AKS Deployment

## Overview
Patterns and commands for deploying applications to Azure Kubernetes Service (AKS) with GitHub Actions CI/CD.

## Quick Reference

### AKS Cluster Management
```bash
# Create resource group
az group create --name myapp-rg --location westus2

# Register container service provider (first time only)
az provider register --namespace Microsoft.ContainerService --wait

# Create AKS cluster (cost-optimized)
az aks create \
  --resource-group myapp-rg \
  --name myapp-aks \
  --node-count 1 \
  --node-vm-size Standard_B2s_v2 \
  --enable-managed-identity \
  --generate-ssh-keys \
  --tier free

# Get credentials
az aks get-credentials --resource-group myapp-rg --name myapp-aks

# Stop cluster (save money)
az aks stop --resource-group myapp-rg --name myapp-aks

# Start cluster
az aks start --resource-group myapp-rg --name myapp-aks

# Delete cluster
az aks delete --resource-group myapp-rg --name myapp-aks --yes
```

### Service Principal for CI/CD
```bash
# Create SP with contributor role on resource group
az ad sp create-for-rbac \
  --name "myapp-github-actions" \
  --role contributor \
  --scopes /subscriptions/$(az account show --query id -o tsv)/resourceGroups/myapp-rg \
  --sdk-auth

# Output JSON goes in AZURE_CREDENTIALS GitHub secret
```

### Helm Deployment
```bash
# Lint chart
helm lint ./infra/helm/myapp

# Dry run
helm upgrade --install myapp ./infra/helm/myapp --dry-run

# Deploy with values file (recommended for secrets)
helm upgrade --install myapp ./infra/helm/myapp \
  -f /tmp/secrets-values.yaml \
  --wait \
  --timeout 5m

# Check status
helm status myapp
helm history myapp

# Rollback
helm rollback myapp 1
```

### Expose Service
```bash
# Patch to LoadBalancer
kubectl patch svc frontend -p '{"spec": {"type": "LoadBalancer"}}'

# Get external IP
kubectl get svc frontend -o jsonpath='{.status.loadBalancer.ingress[0].ip}'
```

## GitHub Actions CI Workflow

```yaml
name: CI - Build and Push Docker Images

on:
  push:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ghcr.io/${{ github.repository }}

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - uses: docker/setup-buildx-action@v3

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/build-push-action@v5
        with:
          context: .
          file: infra/docker/backend.Dockerfile
          push: true
          tags: |
            ${{ env.IMAGE_NAME }}/backend:latest
            ${{ env.IMAGE_NAME }}/backend:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## GitHub Actions CD Workflow

```yaml
name: CD - Deploy to AKS

on:
  workflow_run:
    workflows: ["CI - Build and Push Docker Images"]
    types: [completed]
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}

    steps:
      - uses: actions/checkout@v4

      - uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - uses: azure/aks-set-context@v4
        with:
          resource-group: myapp-rg
          cluster-name: myapp-aks

      - uses: azure/setup-helm@v4

      - name: Deploy with Helm
        run: |
          helm upgrade --install myapp ./infra/helm/myapp \
            --set backend.image.tag=${{ github.sha }} \
            --set backend.env.DATABASE_URL="${{ secrets.DATABASE_URL }}" \
            --wait --timeout 5m
```

## Helm Chart Structure

```
infra/helm/myapp/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── _helpers.tpl
    ├── backend-deployment.yaml
    ├── backend-service.yaml
    ├── frontend-deployment.yaml
    ├── frontend-service.yaml
    ├── secrets.yaml
    └── ingress.yaml
```

## Common Issues

| Issue | Solution |
|-------|----------|
| VM size not allowed | Try different region or VM series (v2) |
| SubscriptionNotRegistered | `az provider register --namespace Microsoft.ContainerService` |
| Image pull fails | Make GHCR packages public or add imagePullSecret |
| Secrets empty | Use values file instead of `--set` for URLs |
| Pod CrashLoopBackOff | Check logs: `kubectl logs <pod> --previous` |

## Cost Optimization

| Action | Savings |
|--------|---------|
| Use Free tier AKS | ~$73/month |
| Use B-series VMs | ~50% vs D-series |
| Stop when not in use | Pay only when running |
| Single node for dev | Minimal cost |

## Verification Commands

```bash
# Cluster health
kubectl get nodes
kubectl top nodes

# Pod status
kubectl get pods -o wide
kubectl describe pod <pod-name>
kubectl logs <pod-name>

# Service status
kubectl get svc
kubectl get endpoints

# Test connectivity
kubectl run curl --image=curlimages/curl --rm -it --restart=Never -- curl http://backend:8000/health
```

## Related
- ADR-010: Azure AKS Cloud Deployment
- PHR-006: Helm Secrets with Special Characters
- Skill: docker-minikube.md (local K8s)
