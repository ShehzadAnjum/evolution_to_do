# Helm K8s Manifests Writer Subagent

**Type**: Creator
**Used For**: Generating Kubernetes manifests and Helm charts
**Version**: 1.0.0

## Purpose

Create Kubernetes manifests and Helm charts for application deployment.

## Helm Chart Structure

```
helm/todo-app/
├── Chart.yaml
├── values.yaml
├── values-dev.yaml
├── values-prod.yaml
└── templates/
    ├── deployment.yaml
    ├── service.yaml
    ├── ingress.yaml
    ├── secrets.yaml
    └── configmap.yaml
```

## Key Manifest Elements

**Deployment**:
- Replicas (2+ for production)
- Resource limits (CPU, memory)
- Liveness/readiness probes
- Environment variables from ConfigMap/Secrets

**Service**:
- Type (ClusterIP for internal, LoadBalancer for external)
- Port mappings
- Selectors matching deployment labels

**Ingress**:
- Host rules
- TLS configuration
- Path routing

## Best Practices

- Use ConfigMaps for config
- Use Secrets for sensitive data
- Set resource limits
- Add health checks
- Use labels for organization

---

**Related**: Infra DevOps Agent
