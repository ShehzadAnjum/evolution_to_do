# Skill: Cloud-Native Blueprint

## Overview

This skill provides a complete blueprint for deploying cloud-native applications to Kubernetes with CI/CD, service mesh, and event-driven architecture. It consolidates lessons learned from deploying Evolution of Todo to Azure AKS.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           GitHub Actions CI/CD                               │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐  │
│  │   Checkout  │───▶│ Build/Push  │───▶│  AKS Auth   │───▶│   Deploy    │  │
│  │   Code      │    │   to GHCR   │    │   kubectl   │    │   Helm      │  │
│  └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                         │
                                         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Azure AKS Cluster                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐│
│  │                         evolution-todo namespace                         ││
│  │  ┌───────────────────┐           ┌───────────────────┐                 ││
│  │  │   Frontend Pod    │           │   Backend Pod     │                 ││
│  │  │  ┌─────────────┐  │           │  ┌─────────────┐  │                 ││
│  │  │  │   Next.js   │  │           │  │   FastAPI   │  │                 ││
│  │  │  │    App      │  │   REST    │  │    App      │  │                 ││
│  │  │  │   :3000     │──┼───────────┼──│   :8000     │  │                 ││
│  │  │  └─────────────┘  │           │  └──────┬──────┘  │                 ││
│  │  │                   │           │         │         │                 ││
│  │  │                   │           │  ┌──────▼──────┐  │                 ││
│  │  │                   │           │  │Dapr Sidecar │  │                 ││
│  │  │                   │           │  │   :3500     │  │                 ││
│  │  └───────────────────┘           │  └──────┬──────┘  │                 ││
│  │                                  └─────────┼─────────┘                 ││
│  │                                            │                            ││
│  │  ┌─────────────────────────────────────────▼─────────────────────────┐ ││
│  │  │                    Dapr Components                                 │ ││
│  │  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐            │ ││
│  │  │  │  Pub/Sub     │  │  State Store │  │  Bindings    │            │ ││
│  │  │  │ (Redpanda)   │  │ (PostgreSQL) │  │  (Cron)      │            │ ││
│  │  │  └──────────────┘  └──────────────┘  └──────────────┘            │ ││
│  │  └────────────────────────────────────────────────────────────────────┘ ││
│  └─────────────────────────────────────────────────────────────────────────┘│
│                                                                              │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐      │
│  │  LoadBalancer    │    │  LoadBalancer    │    │    Secrets       │      │
│  │  :3000 (public)  │    │  :8000 (public)  │    │  (encrypted)     │      │
│  └──────────────────┘    └──────────────────┘    └──────────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
                    │                    │
                    ▼                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        External Services                                     │
│  ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐      │
│  │  Neon PostgreSQL │    │  Redpanda Cloud  │    │   Google OAuth   │      │
│  │   (Database)     │    │    (Kafka)       │    │   (Auth)         │      │
│  └──────────────────┘    └──────────────────┘    └──────────────────┘      │
└─────────────────────────────────────────────────────────────────────────────┘
```

## CI/CD Pipeline Structure

### Workflow Architecture

```yaml
# Two-stage pipeline: CI builds, CD deploys
ci.yml:
  triggers: [push, pull_request]
  jobs:
    - build-backend → GHCR
    - build-frontend → GHCR

cd.yml:
  triggers: [workflow_run: ci.yml success]
  jobs:
    - deploy → AKS
```

### CI Workflow (Build & Push)

```yaml
name: CI - Build and Push

on:
  push:
    branches: [main]
    paths:
      - 'backend/**'
      - 'frontend/**'
      - '.github/workflows/ci.yml'
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_PREFIX: ${{ github.repository_owner }}/evolution_to_do

jobs:
  build-backend:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push backend
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          file: ./infra/docker/backend.Dockerfile
          push: ${{ github.event_name != 'pull_request' }}
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/backend:latest
            ${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/backend:${{ github.sha }}

  build-frontend:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - name: Log in to GHCR
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push frontend
        uses: docker/build-push-action@v5
        with:
          context: ./frontend
          file: ./infra/docker/frontend.Dockerfile
          push: ${{ github.event_name != 'pull_request' }}
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/frontend:latest
            ${{ env.REGISTRY }}/${{ env.IMAGE_PREFIX }}/frontend:${{ github.sha }}
          build-args: |
            NEXT_PUBLIC_API_URL=${{ secrets.NEXT_PUBLIC_API_URL }}
```

### CD Workflow (Deploy to AKS)

```yaml
name: CD - Deploy to AKS

on:
  workflow_run:
    workflows: ["CI - Build and Push"]
    types: [completed]
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    steps:
      - uses: actions/checkout@v4

      - name: Azure Login
        uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Set AKS context
        uses: azure/aks-set-context@v4
        with:
          resource-group: ${{ secrets.AKS_RESOURCE_GROUP }}
          cluster-name: ${{ secrets.AKS_CLUSTER_NAME }}

      - name: Install Dapr on AKS
        run: |
          if ! kubectl get namespace dapr-system > /dev/null 2>&1; then
            helm repo add dapr https://dapr.github.io/helm-charts/
            helm repo update
            helm upgrade --install dapr dapr/dapr \
              --namespace dapr-system \
              --create-namespace \
              --wait --timeout 5m
          fi

      - name: Create namespace and secrets
        run: |
          kubectl create namespace evolution-todo --dry-run=client -o yaml | kubectl apply -f -
          kubectl create secret generic evolution-todo-secrets \
            --namespace evolution-todo \
            --from-literal=database-url="${{ secrets.DATABASE_URL }}" \
            --from-literal=better-auth-secret="${{ secrets.BETTER_AUTH_SECRET }}" \
            --from-literal=openai-api-key="${{ secrets.OPENAI_API_KEY }}" \
            --dry-run=client -o yaml | kubectl apply -f -

      - name: Deploy Dapr Components
        env:
          REDPANDA_BROKERS: ${{ secrets.REDPANDA_BROKERS }}
        run: |
          if [ -n "$REDPANDA_BROKERS" ]; then
            kubectl apply -f infra/dapr/cloud/pubsub-redpanda.yaml
          else
            kubectl apply -f infra/dapr/cloud/pubsub-memory.yaml
          fi
          kubectl apply -f infra/dapr/cloud/statestore.yaml

      - name: Deploy with Helm
        run: |
          helm upgrade --install evolution-todo ./infra/helm/evolution-todo \
            --namespace evolution-todo \
            --set backend.image.tag=latest \
            --set frontend.image.tag=latest \
            --wait --timeout 10m

      # CRITICAL: Force pod restart for latest tag
      - name: Force pod restart to pull latest images
        run: |
          kubectl rollout restart deployment/frontend -n evolution-todo
          kubectl rollout restart deployment/backend -n evolution-todo
          kubectl rollout status deployment/frontend -n evolution-todo --timeout=5m
          kubectl rollout status deployment/backend -n evolution-todo --timeout=5m
```

## Helm Chart Structure

```
infra/helm/evolution-todo/
├── Chart.yaml
├── values.yaml
└── templates/
    ├── _helpers.tpl
    ├── backend-deployment.yaml
    ├── backend-service.yaml
    ├── frontend-deployment.yaml
    ├── frontend-service.yaml
    └── secrets.yaml
```

### values.yaml

```yaml
global:
  imageRegistry: ghcr.io/username/evolution_to_do

backend:
  name: backend
  replicaCount: 1
  image:
    repository: ghcr.io/username/evolution_to_do/backend
    tag: latest
    pullPolicy: Always
  service:
    type: LoadBalancer
    port: 8000
  resources:
    limits:
      cpu: 500m
      memory: 512Mi
    requests:
      cpu: 100m
      memory: 256Mi

frontend:
  name: frontend
  replicaCount: 1
  image:
    repository: ghcr.io/username/evolution_to_do/frontend
    tag: latest
    pullPolicy: Always
  service:
    type: LoadBalancer
    port: 3000
    loadBalancerIP: "x.x.x.x"  # Static Azure IP
  resources:
    limits:
      cpu: 300m
      memory: 256Mi
    requests:
      cpu: 50m
      memory: 128Mi

dapr:
  enabled: true

healthCheck:
  enabled: true
  initialDelaySeconds: 10
  periodSeconds: 30
  timeoutSeconds: 5
```

### Deployment with Dapr Sidecar

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .Values.backend.name }}
spec:
  replicas: {{ .Values.backend.replicaCount }}
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
      {{- if .Values.dapr.enabled }}
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "backend"
        dapr.io/app-port: "{{ .Values.backend.service.port }}"
        dapr.io/enable-api-logging: "true"
      {{- end }}
    spec:
      containers:
        - name: {{ .Values.backend.name }}
          image: "{{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag }}"
          imagePullPolicy: {{ .Values.backend.image.pullPolicy }}
          ports:
            - containerPort: {{ .Values.backend.service.port }}
          env:
            - name: DATABASE_URL
              valueFrom:
                secretKeyRef:
                  name: evolution-todo-secrets
                  key: database-url
            {{- if .Values.dapr.enabled }}
            - name: DAPR_ENABLED
              value: "true"
            - name: DAPR_HTTP_PORT
              value: "3500"
            {{- end }}
```

## Dapr Components

### Pub/Sub (In-Memory - Demo)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: taskevents
  namespace: evolution-todo
spec:
  type: pubsub.in-memory
  version: v1
  metadata: []
```

### Pub/Sub (Redpanda Cloud - Production)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: taskevents
  namespace: evolution-todo
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      secretKeyRef:
        name: redpanda-credentials
        key: brokers
    - name: authType
      value: "password"
    - name: saslUsername
      secretKeyRef:
        name: redpanda-credentials
        key: username
    - name: saslPassword
      secretKeyRef:
        name: redpanda-credentials
        key: password
    - name: saslMechanism
      value: "SCRAM-SHA-256"
    - name: disableTls
      value: "false"
```

### State Store (PostgreSQL)

```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: evolution-todo
spec:
  type: state.postgresql
  version: v1
  metadata:
    - name: connectionString
      secretKeyRef:
        name: evolution-todo-secrets
        key: database-url
    - name: tableName
      value: "dapr_state"
```

## Critical Lessons Learned

### 1. Secure Cookies with HTTP LoadBalancer

**Problem**: AKS LoadBalancer uses HTTP, but `useSecureCookies: NODE_ENV === "production"` blocks cookies.

**Solution**: Base secure cookies on URL scheme, not environment:

```typescript
// ❌ WRONG - breaks on HTTP production
advanced: {
  useSecureCookies: process.env.NODE_ENV === "production",
}

// ✅ CORRECT - works for HTTP or HTTPS
advanced: {
  useSecureCookies: (env.BETTER_AUTH_URL ?? "http://localhost:3000").startsWith("https://"),
}
```

### 2. Pod Restart with Latest Tag

**Problem**: Pods don't pull new images when using `latest` tag because spec doesn't change.

**Solution**: Add explicit rollout restart to CD workflow:

```yaml
- name: Force pod restart to pull latest images
  run: |
    kubectl rollout restart deployment/frontend -n evolution-todo
    kubectl rollout restart deployment/backend -n evolution-todo
```

### 3. CORS Configuration

**Problem**: Backend rejects requests from Kubernetes LoadBalancer IP.

**Solution**: Add all valid origins to CORS:

```python
origins = [
    "http://localhost:3000",
    f"http://{aks_public_ip}:3000",
    f"http://{aks_public_ip}.nip.io:3000",  # nip.io for DNS
]
```

### 4. Azure Service Principal

**Create credentials for GitHub Actions**:

```bash
az ad sp create-for-rbac \
  --name "github-actions-aks" \
  --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/{resource-group} \
  --sdk-auth
```

Store entire JSON output as `AZURE_CREDENTIALS` secret.

### 5. Static IP for Frontend

**Reserve Azure public IP**:

```bash
# Create IP in the MC_ node resource group
az network public-ip create \
  --resource-group MC_evolution-todo_evolution-todo-aks_eastus \
  --name evolution-todo-frontend-ip \
  --sku Standard \
  --allocation-method static
```

Reference in Helm values:
```yaml
frontend:
  service:
    loadBalancerIP: "x.x.x.x"
```

### 6. nip.io for Dynamic DNS

Use `{ip}.nip.io` for OAuth redirect URIs without custom domain:

```
BETTER_AUTH_URL=http://172.171.119.133.nip.io:3000
Google OAuth redirect: http://172.171.119.133.nip.io:3000/api/auth/callback/google
```

### 7. Dapr Sidecar Verification

Check injection is working:

```bash
# Should show 2/2 READY (app + sidecar)
kubectl get pods -n evolution-todo
# NAME                       READY   STATUS
# backend-xxx                2/2     Running

# Check component loaded
kubectl logs -n evolution-todo -l app=backend -c daprd | grep "Component loaded"
```

## Checklist for Cloud-Native Deployment

### Pre-deployment
- [ ] Docker images build locally
- [ ] Helm chart templates validated (`helm template`)
- [ ] Azure service principal created
- [ ] GitHub secrets configured (AZURE_CREDENTIALS, DATABASE_URL, etc.)
- [ ] Static IP reserved for frontend

### CI Pipeline
- [ ] Build jobs complete successfully
- [ ] Images pushed to GHCR
- [ ] Image tags include SHA for traceability

### CD Pipeline
- [ ] Azure login succeeds
- [ ] AKS context set correctly
- [ ] Dapr installed in dapr-system namespace
- [ ] Secrets created in target namespace
- [ ] Dapr components applied
- [ ] Helm deployment succeeds
- [ ] Pod rollout restart triggered

### Post-deployment
- [ ] Pods running (2/2 with Dapr sidecar)
- [ ] Services have external IPs
- [ ] Health endpoints responding
- [ ] OAuth redirects working
- [ ] API calls succeeding (check CORS)
- [ ] Dapr components loaded (check sidecar logs)

## Quick Debugging Commands

```bash
# Check pod status
kubectl get pods -n evolution-todo

# Check services and external IPs
kubectl get svc -n evolution-todo

# View pod logs
kubectl logs -n evolution-todo deployment/backend -c backend
kubectl logs -n evolution-todo deployment/backend -c daprd

# Check Dapr components
kubectl get components.dapr.io -n evolution-todo

# Debug auth issues
kubectl exec -n evolution-todo deployment/frontend -- env | grep -i auth

# Test internal service connectivity
kubectl run -it --rm debug --image=curlimages/curl --restart=Never -- \
  curl http://backend:8000/health
```

---

**Part of**: Evolution of Todo Reusable Intelligence
**Category**: Cloud-Native Deployment
**Points Value**: +200 (Cloud-Native Blueprint skill)
**Last Updated**: 2025-12-14
