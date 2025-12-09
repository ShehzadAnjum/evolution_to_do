# Skill: Docker + Minikube Local K8s

## Overview

This skill captures patterns for containerizing the application with Docker and deploying to local Kubernetes via Minikube (Phase IV).

## Core Concepts

### Container Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      Minikube Cluster                        │
├─────────────────┬───────────────────┬───────────────────────┤
│   Frontend Pod  │   Backend Pod     │   Database            │
│   (Next.js)     │   (FastAPI)       │   (External: Neon)    │
│                 │                   │                       │
│   Port: 3000    │   Port: 8000      │   External connection │
└─────────────────┴───────────────────┴───────────────────────┘
```

## Docker Setup

### Backend Dockerfile

**File**: `backend/Dockerfile`
```dockerfile
# Build stage
FROM python:3.13-slim AS builder

WORKDIR /app

# Install uv for fast dependency management
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Production stage
FROM python:3.13-slim AS production

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY src/ ./src/
COPY main.py ./

# Set environment
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile

**File**: `frontend/Dockerfile`
```dockerfile
# Build stage
FROM node:22-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm ci

# Copy source
COPY . .

# Build
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# Production stage
FROM node:22-alpine AS production

WORKDIR /app

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

# Copy built assets
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 3000

CMD ["node", "server.js"]
```

### Docker Compose (Development)

**File**: `docker-compose.yml`
```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - BETTER_AUTH_SECRET=${BETTER_AUTH_SECRET}
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
      - BETTER_AUTH_URL=http://localhost:3000
    depends_on:
      backend:
        condition: service_healthy
```

## Minikube Setup

### Installation & Start

```bash
# Install minikube
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

# Start cluster
minikube start --driver=docker --memory=4096 --cpus=2

# Enable addons
minikube addons enable ingress
minikube addons enable metrics-server

# Verify
kubectl get nodes
```

### Build Images in Minikube

```bash
# Use Minikube's Docker daemon
eval $(minikube docker-env)

# Build images (they'll be available in Minikube)
docker build -t evolution-todo-backend:latest ./backend
docker build -t evolution-todo-frontend:latest ./frontend

# Verify
docker images | grep evolution-todo
```

## Kubernetes Manifests

### Backend Deployment

**File**: `infra/k8s/backend-deployment.yaml`
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  labels:
    app: evolution-todo
    component: backend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: evolution-todo
      component: backend
  template:
    metadata:
      labels:
        app: evolution-todo
        component: backend
    spec:
      containers:
        - name: backend
          image: evolution-todo-backend:latest
          imagePullPolicy: Never  # Use local image
          ports:
            - containerPort: 8000
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: evolution-todo-secrets
                  key: database-url
            - name: BETTER_AUTH_SECRET
              valueFrom:
                secretKeyRef:
                  name: evolution-todo-secrets
                  key: better-auth-secret
          readinessProbe:
            httpGet:
              path: /health
              port: 8000
            initialDelaySeconds: 5
            periodSeconds: 10
          resources:
            limits:
              memory: "512Mi"
              cpu: "500m"
            requests:
              memory: "256Mi"
              cpu: "250m"
```

### Service

**File**: `infra/k8s/backend-service.yaml`
```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
spec:
  selector:
    app: evolution-todo
    component: backend
  ports:
    - port: 8000
      targetPort: 8000
  type: ClusterIP
```

### Secrets

```bash
# Create secrets
kubectl create secret generic evolution-todo-secrets \
  --from-literal=database-url='postgresql://...' \
  --from-literal=better-auth-secret='...'
```

### Ingress

**File**: `infra/k8s/ingress.yaml`
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: evolution-todo-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
    - host: evolution-todo.local
      http:
        paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: backend
                port:
                  number: 8000
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend
                port:
                  number: 3000
```

## Common Commands

```bash
# Apply all manifests
kubectl apply -f infra/k8s/

# Check pods
kubectl get pods -l app=evolution-todo

# View logs
kubectl logs -l component=backend -f

# Port forward for testing
kubectl port-forward svc/backend 8000:8000

# Access via Minikube
minikube service frontend --url

# Dashboard
minikube dashboard
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| ImagePullBackOff | Set imagePullPolicy: Never for local images |
| CrashLoopBackOff | Check logs: kubectl logs pod-name |
| Connection refused | Verify service selector matches pod labels |
| Ingress not working | Check: minikube addons enable ingress |

## Anti-Patterns

### ❌ Hardcoded Secrets

```yaml
env:
  - name: DATABASE_URL
    value: "postgresql://user:pass@host/db"
```

### ✅ Use Kubernetes Secrets

```yaml
env:
  - name: DATABASE_URL
    valueFrom:
      secretKeyRef:
        name: app-secrets
        key: database-url
```

---

**Part of**: Evolution of Todo Reusable Intelligence
**Phase**: IV, V
**Last Updated**: 2025-12-10
