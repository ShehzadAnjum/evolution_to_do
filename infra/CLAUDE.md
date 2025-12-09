# Infrastructure Context: Evolution of Todo (Phase IV+)

**Stack**: Docker | Kubernetes | Helm | Dapr | Kafka
**Last Updated**: 2025-12-10
**Status**: Placeholder structure for Phase IV

---

## Quick Reference

```bash
cd infra

# Phase IV: Local Kubernetes
minikube start --driver=docker
kubectl apply -f k8s/
helm install evolution-todo helm/evolution-todo/

# Phase V: Cloud (DOKS)
kubectl config use-context do-nyc1-evolution-todo
kubectl apply -f k8s/
```

---

## Directory Structure

```
infra/
├── CLAUDE.md            # This file
├── docker/              # Dockerfiles
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
├── k8s/                 # Kubernetes manifests
│   ├── backend-deployment.yaml
│   ├── backend-service.yaml
│   ├── frontend-deployment.yaml
│   ├── frontend-service.yaml
│   ├── ingress.yaml
│   └── secrets.yaml
├── helm/                # Helm charts (Phase V)
│   └── evolution-todo/
│       ├── Chart.yaml
│       ├── values.yaml
│       └── templates/
└── dapr/                # Dapr components (Phase V)
    └── components/
        ├── pubsub.yaml
        └── statestore.yaml
```

---

## Phase Boundaries

### Phase IV: Local Kubernetes
- Docker containerization
- Minikube deployment
- Basic K8s manifests
- NO NEW FEATURES (just packaging Phase III)

### Phase V: Cloud + Advanced
- DigitalOcean Kubernetes (DOKS)
- Helm charts
- Kafka/Redpanda
- Dapr components
- Recurring tasks and reminders

---

## Current Status

This directory contains placeholder structure for Phase IV.
Actual implementation happens when Phase III is complete.

**Do not implement Phase IV features until:**
1. Phase II complete (task CRUD, tests, capstone)
2. Phase III complete (AI chatbot, MCP tools)
3. Phase gate check passes

---

## Related Agents

- **Infra DevOps Agent**: `.claude/agents/infra-devops.md`
- **Dockerfile Creator**: `.claude/subagents/dockerfile-creator.md`
- **Helm K8s Writer**: `.claude/subagents/helm-k8s-manifests-writer.md`
- **K8s Troubleshooter**: `.claude/subagents/k8s-troubleshooter.md`

## Related Skills

- **Docker Minikube**: `.claude/skills/docker-minikube.md`
- **Kafka Dapr Patterns**: `.claude/skills/kafka-dapr-patterns.md`

---

**Parent Context**: See `/CLAUDE.md` for project-wide instructions.
