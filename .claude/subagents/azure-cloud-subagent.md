# Azure Cloud Subagent

**Type**: Cloud Specialist
**Used For**: Azure-specific operations (AKS, Service Principals, Resource Groups)
**Version**: 1.0.0
**Created**: 2025-12-14
**Parent Agent**: infra-devops.md

## Purpose

Handle Azure-specific cloud operations including AKS cluster management, service principals, resource groups, and Azure CLI operations.

## Responsibilities

- Create and manage Azure resource groups
- Create and manage AKS clusters
- Create service principals for CI/CD
- Configure Azure RBAC and permissions
- Troubleshoot Azure-specific issues
- Optimize Azure costs

## Quick Reference Commands

### Authentication
```bash
# Login interactively
az login

# Login with service principal
az login --service-principal -u <app-id> -p <password> --tenant <tenant-id>

# Check current subscription
az account show

# List subscriptions
az account list -o table

# Set subscription
az account set --subscription "<name-or-id>"
```

### Resource Groups
```bash
# Create resource group
az group create --name myapp-rg --location westus2

# List resource groups
az group list -o table

# Delete resource group
az group delete --name myapp-rg --yes --no-wait
```

### AKS Cluster Management
```bash
# Register provider (first time)
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

# Scale cluster
az aks scale --resource-group myapp-rg --name myapp-aks --node-count 3
```

### Service Principals (for CI/CD)
```bash
# Create SP with contributor role on resource group
az ad sp create-for-rbac \
  --name "myapp-github-actions" \
  --role contributor \
  --scopes /subscriptions/$(az account show --query id -o tsv)/resourceGroups/myapp-rg \
  --sdk-auth

# Output JSON → AZURE_CREDENTIALS GitHub secret
```

## Common Issues & Fixes

### Issue: VM size not allowed
**Error**: `The VM size of Standard_B2s is not allowed in your subscription`
**Cause**: Subscription quota restrictions by region
**Fix**: Try different VM size (v2 series) or different region
```bash
# Check available VM sizes
az vm list-skus --location westus2 --resource-type virtualMachines \
  --query "[?contains(name, 'Standard_B')].name" -o tsv
```

### Issue: SubscriptionNotRegistered
**Error**: `The subscription is not registered to use namespace 'Microsoft.ContainerService'`
**Fix**: Register the provider
```bash
az provider register --namespace Microsoft.ContainerService --wait
```

### Issue: Subscription not found after re-login
**Cause**: Login switched to different tenant
**Fix**: Check and set correct subscription
```bash
az account list -o table
az account set --subscription "<correct-subscription>"
```

### Issue: Service Principal expired
**Cause**: SP credentials expire after 1 year by default
**Fix**: Reset credentials
```bash
az ad sp credential reset --id <app-id>
```

## Cost Optimization

| Action | Savings |
|--------|---------|
| Use Free tier AKS management | ~$73/month |
| Use B-series VMs | ~50% vs D-series |
| Stop cluster when not in use | 100% compute savings |
| Use spot instances (dev/test) | ~60-90% savings |
| Single node for dev | Minimal cost |

### Stop/Start Schedule (example)
```bash
# Stop at end of day
az aks stop --resource-group myapp-rg --name myapp-aks

# Start in morning
az aks start --resource-group myapp-rg --name myapp-aks

# Automate with Azure Automation or cron
```

## Current Deployment

| Resource | Value |
|----------|-------|
| Resource Group | `evo-todo-rg` |
| Location | `westus2` |
| AKS Cluster | `evo-todo-aks` |
| VM Size | `Standard_B2s_v2` |
| Node Count | 1 |
| K8s Version | 1.33 |
| Service Principal | `evolution-todo-github-actions` |

## Debug Checklist

1. Check login status: `az account show`
2. Check subscription: `az account list -o table`
3. Check resource group: `az group show --name myapp-rg`
4. Check AKS status: `az aks show --resource-group myapp-rg --name myapp-aks`
5. Check VM quotas: `az vm list-usage --location westus2 -o table`

---

**Related**:
- Agent: infra-devops.md
- Subagent: cicd-pipeline-subagent.md
- Skill: azure-aks-deployment.md
- ADR-010: Azure AKS Cloud Deployment
