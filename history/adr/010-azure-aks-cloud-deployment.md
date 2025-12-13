# ADR-010: Azure AKS Cloud Deployment Architecture

## Status
**Accepted** - 2025-12-14

## Context
Phase V Part C requires cloud deployment of the Evolution Todo application. The reference architecture specified:
- Vendor-agnostic container images (GHCR)
- Kubernetes deployment with Helm
- GitHub Actions CI/CD pipeline
- One-command deploy capability

Options considered:
1. **DigitalOcean Kubernetes (DOKS)** - Original plan, $200 free credits
2. **Azure AKS** - User's existing Azure subscription
3. **Hetzner** - Budget-friendly option
4. **GKE** - Quota issues encountered previously (ADR-005)

## Decision
**Azure AKS** with GitHub Actions CI/CD pipeline:

### Architecture
```
GitHub Push → CI (Build Docker) → GHCR → CD (Helm Deploy) → AKS
```

### Components
| Component | Choice | Rationale |
|-----------|--------|-----------|
| Container Registry | GHCR (public) | Free, integrated with GitHub Actions |
| Kubernetes | Azure AKS (Free tier) | User has Azure subscription |
| VM Size | Standard_B2s_v2 | Cheapest available in subscription |
| Region | westus2 | B-series v2 availability |
| CI/CD | GitHub Actions | Zero cost, native integration |
| Package Manager | Helm | Industry standard, templating |

### Cost Optimization
- Free tier AKS management
- Single node (Standard_B2s_v2: ~$30-40/month)
- Can stop cluster when not in use: `az aks stop`

## Consequences

### Positive
- Vendor-agnostic images work on any K8s (AKS, DOKS, Hetzner)
- Zero manual deployment steps after setup
- Helm chart reusable across environments
- Cost-effective with stop/start capability

### Negative
- Azure subscription required
- B-series v2 not available in all regions (eastus failed)
- Service principal management for CD pipeline

### Lessons Learned
1. **VM Quota Restrictions**: Azure subscriptions may restrict VM types by region
2. **Helm Secrets**: Special characters in URLs need values file, not `--set`
3. **GHCR Visibility**: Default private, must change to public for K8s pull

## References
- ADR-005: Cloud Deployment Deferred (GKE quota)
- PHR-006: Helm Secrets with Special Characters
- `.github/workflows/ci.yml` - CI pipeline
- `.github/workflows/cd.yml` - CD pipeline
- `infra/helm/evolution-todo/` - Helm chart
