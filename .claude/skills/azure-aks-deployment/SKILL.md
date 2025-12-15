---
name: azure-aks-deployment
description: Azure AKS deployment patterns. Use when deploying to Azure Kubernetes Service, setting up service principals, or configuring Helm releases on AKS.
---

# Azure AKS Deployment

## Create AKS Cluster

```bash
az group create --name evo-todo-rg --location westus2
az aks create \
  --resource-group evo-todo-rg \
  --name evo-todo-aks \
  --node-count 1 \
  --node-vm-size Standard_B2s_v2 \
  --generate-ssh-keys
```

## Service Principal for GitHub Actions

```bash
az ad sp create-for-rbac \
  --name "evolution-todo-github-actions" \
  --role contributor \
  --scopes /subscriptions/{sub-id}/resourceGroups/evo-todo-rg \
  --json-auth
```

Store output as `AZURE_CREDENTIALS` secret in GitHub.

## Deploy with Helm

```bash
az aks get-credentials --resource-group evo-todo-rg --name evo-todo-aks
helm upgrade --install evolution-todo ./infra/helm/evolution-todo \
  --set backend.image.tag=latest \
  --set frontend.image.tag=latest
```

## Install Dapr on AKS

```bash
helm repo add dapr https://dapr.github.io/helm-charts/
helm install dapr dapr/dapr --namespace dapr-system --create-namespace
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Image pull errors | Check GHCR permissions, use `imagePullSecrets` |
| Service not accessible | Use LoadBalancer type or Ingress |
| Pods CrashLoopBackOff | Check logs: `kubectl logs pod-name` |
