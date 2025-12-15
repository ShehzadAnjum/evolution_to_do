---
name: docker-minikube
description: Docker containerization and Minikube local Kubernetes. Use when building Dockerfiles, running containers locally, or deploying to local K8s cluster.
---

# Docker & Minikube

## Multi-Stage Dockerfile (Python)

```dockerfile
FROM python:3.13-slim AS builder
WORKDIR /app
RUN pip install --no-cache-dir fastapi uvicorn sqlmodel

FROM python:3.13-slim AS production
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY src ./src
RUN useradd --create-home appuser && chown -R appuser /app
USER appuser
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Multi-Stage Dockerfile (Node)

```dockerfile
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
RUN adduser --system --uid 1001 nextjs
COPY --from=builder --chown=nextjs /app/.next/standalone ./
USER nextjs
EXPOSE 3000
CMD ["node", "server.js"]
```

## Minikube Commands

```bash
minikube start --driver=docker
minikube dashboard
eval $(minikube docker-env)  # Use minikube's Docker
kubectl apply -f k8s/
minikube service frontend --url
```

## Docker Compose (Local Dev)

```yaml
services:
  backend:
    build: { context: ., dockerfile: infra/docker/backend.Dockerfile }
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=${DATABASE_URL}
  frontend:
    build: { context: ., dockerfile: infra/docker/frontend.Dockerfile }
    ports: ["3000:3000"]
```
