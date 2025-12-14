# CI/CD Pipeline Subagent

**Type**: Implementer
**Used For**: Creating and maintaining CI/CD pipelines (GitHub Actions)
**Version**: 1.0.0
**Created**: 2025-12-14
**Parent Agent**: infra-devops.md

## Purpose

Create, debug, and maintain GitHub Actions CI/CD workflows for automated building, testing, and deployment.

## Responsibilities

- Create GitHub Actions workflow files
- Configure CI pipelines (build, test, lint)
- Configure CD pipelines (deploy to K8s, cloud)
- Manage workflow secrets and environment variables
- Debug failing pipelines
- Optimize workflow performance (caching, parallelization)

## Workflow Templates

### CI Pipeline (Build & Push Docker)
```yaml
name: CI - Build and Push

on:
  push:
    branches: [main]
  pull_request:
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
        if: github.event_name != 'pull_request'
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - uses: docker/metadata-action@v5
        id: meta
        with:
          images: ${{ env.IMAGE_NAME }}/app
          tags: |
            type=sha,prefix=
            type=raw,value=latest,enable={{is_default_branch}}

      - uses: docker/build-push-action@v5
        with:
          context: .
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

### CD Pipeline (Deploy to K8s)
```yaml
name: CD - Deploy

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

      - uses: azure/login@v2  # or cloud-specific action
        with:
          creds: ${{ secrets.CLOUD_CREDENTIALS }}

      - uses: azure/setup-helm@v4

      - name: Deploy with Helm
        env:
          # Use env vars for secrets to avoid shell escaping issues
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          cat > /tmp/values.yaml << EOF
          backend:
            env:
              DATABASE_URL: "${DATABASE_URL}"
          EOF

          helm upgrade --install app ./chart -f /tmp/values.yaml --wait
          rm -f /tmp/values.yaml
```

## Common Issues & Fixes

### Issue: Secrets with special characters fail
**Cause**: `--set` flag doesn't escape URLs properly
**Fix**: Use values file with environment variables (see PHR-006)

### Issue: Image tag mismatch (CI vs CD)
**Cause**: CI uses short SHA, CD uses full SHA
**Fix**: Use `latest` tag or ensure SHA format matches

### Issue: Concurrent deployments conflict
**Cause**: Multiple CD runs at same time
**Fix**: Add concurrency group:
```yaml
concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: true
```

### Issue: Workflow not triggering
**Cause**: YAML syntax error or wrong event
**Fix**: Validate with `act` locally or check Actions tab

## Debug Checklist

1. Check workflow syntax: `.github/workflows/*.yml`
2. Check Actions tab for run logs
3. Verify secrets are set: `gh secret list`
4. Test locally with `act` (optional)
5. Check permissions (packages:write for GHCR)

## Required Secrets

| Secret | Purpose | Example |
|--------|---------|---------|
| `GITHUB_TOKEN` | Auto-provided | Push to GHCR |
| `AZURE_CREDENTIALS` | Azure SP JSON | Deploy to AKS |
| `DATABASE_URL` | DB connection | App config |

## Best Practices

1. **Cache dependencies**: Use `cache-from: type=gha`
2. **Parallel jobs**: Split independent tasks
3. **Fail fast**: Use `fail-fast: true` for matrix builds
4. **Protect secrets**: Never echo secrets, use env vars
5. **Concurrency control**: Prevent overlapping deployments

---

**Related**:
- Agent: infra-devops.md
- Skill: github-actions-cicd.md
- ADR-010: Azure AKS Cloud Deployment
- PHR-006: Helm Secrets with Special Characters
