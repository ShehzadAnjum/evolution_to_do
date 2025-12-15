# Skill: GitHub Actions CI/CD

## Overview
Patterns and best practices for GitHub Actions CI/CD pipelines.

## Workflow Triggers

### Push/PR Triggers
```yaml
on:
  push:
    branches: [main, develop]
    paths:
      - 'src/**'
      - 'package.json'
  pull_request:
    branches: [main]
```

### Workflow Chaining (CD after CI)
```yaml
on:
  workflow_run:
    workflows: ["CI - Build"]
    types: [completed]
    branches: [main]

jobs:
  deploy:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
```

### Manual Trigger
```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: 'Deploy environment'
        required: true
        default: 'staging'
        type: choice
        options:
          - staging
          - production
```

## Docker Build & Push

### To GHCR (GitHub Container Registry)
```yaml
env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ghcr.io/${{ github.repository }}/app

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

      - uses: docker/metadata-action@v5
        id: meta
        with:
          images: ${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=raw,value=latest,enable={{is_default_branch}}

      - uses: docker/build-push-action@v5
        with:
          context: .
          file: ./Dockerfile
          push: ${{ github.event_name != 'pull_request' }}
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

## Secrets Handling

### CRITICAL: Special Characters in Secrets
**Problem**: `--set` flags don't handle URLs with special characters
**Solution**: Use environment variables + heredoc

```yaml
- name: Deploy
  env:
    DATABASE_URL: ${{ secrets.DATABASE_URL }}
    API_KEY: ${{ secrets.API_KEY }}
  run: |
    cat > /tmp/config.yaml << EOF
    database:
      url: "${DATABASE_URL}"
    api:
      key: "${API_KEY}"
    EOF

    # Use the file
    helm upgrade --install app ./chart -f /tmp/config.yaml

    # Always cleanup
    rm -f /tmp/config.yaml
```

### Available Secrets
| Secret | Source | Scope |
|--------|--------|-------|
| `GITHUB_TOKEN` | Auto-provided | Repo (packages, issues, PRs) |
| `secrets.*` | Repo/Org settings | Custom secrets |

### Setting Secrets via CLI
```bash
# Set secret
echo "value" | gh secret set SECRET_NAME

# Set from file
gh secret set SECRET_NAME < file.txt

# List secrets
gh secret list
```

## Caching Strategies

### Node.js Dependencies
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'
```

### Python Dependencies
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.13'
    cache: 'pip'
```

### Docker Layer Cache
```yaml
- uses: docker/build-push-action@v5
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## Concurrency Control

### Prevent Overlapping Deployments
```yaml
concurrency:
  group: deploy-${{ github.ref }}
  cancel-in-progress: true
```

### Queue Deployments (don't cancel)
```yaml
concurrency:
  group: deploy-production
  cancel-in-progress: false
```

## Matrix Builds

### Multiple Versions
```yaml
jobs:
  test:
    strategy:
      matrix:
        node: [18, 20, 22]
        os: [ubuntu-latest, macos-latest]
      fail-fast: true
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node }}
```

## Reusable Workflows

### Define Reusable Workflow
```yaml
# .github/workflows/deploy-template.yml
name: Reusable Deploy

on:
  workflow_call:
    inputs:
      environment:
        required: true
        type: string
    secrets:
      DEPLOY_KEY:
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Deploying to ${{ inputs.environment }}"
```

### Use Reusable Workflow
```yaml
jobs:
  deploy-staging:
    uses: ./.github/workflows/deploy-template.yml
    with:
      environment: staging
    secrets:
      DEPLOY_KEY: ${{ secrets.STAGING_DEPLOY_KEY }}
```

## Common Patterns

### Job Summary
```yaml
- name: Summary
  run: |
    echo "## Deployment Summary" >> $GITHUB_STEP_SUMMARY
    echo "| Service | Status |" >> $GITHUB_STEP_SUMMARY
    echo "|---------|--------|" >> $GITHUB_STEP_SUMMARY
    echo "| Backend | ✅ |" >> $GITHUB_STEP_SUMMARY
```

### Conditional Steps
```yaml
- name: Deploy to Production
  if: github.ref == 'refs/heads/main'
  run: ./deploy.sh production

- name: Deploy to Staging
  if: github.ref == 'refs/heads/develop'
  run: ./deploy.sh staging
```

### Always Run (Cleanup)
```yaml
- name: Cleanup
  if: always()
  run: rm -rf /tmp/secrets
```

## Debugging

### Enable Debug Logging
Set repository secret: `ACTIONS_STEP_DEBUG=true`

### Check Workflow Locally
```bash
# Install act
brew install act  # macOS

# Run workflow locally
act push
```

### View Logs
```bash
# List runs
gh run list

# View specific run
gh run view <run-id> --log
```

## K8s Deployment Patterns

### Force Pod Restart for `latest` Tag

**Problem**: When using `latest` tag, `helm upgrade` won't restart pods if spec unchanged.

**Solution**: Add explicit rollout restart after helm upgrade:

```yaml
- name: Deploy with Helm
  run: |
    helm upgrade --install myapp ./chart --wait

- name: Force pod restart
  run: |
    # Required because 'latest' tag + unchanged spec = no restart
    kubectl rollout restart deployment/frontend
    kubectl rollout restart deployment/backend

- name: Verify deployment
  run: |
    kubectl rollout status deployment/frontend --timeout=120s
    kubectl rollout status deployment/backend --timeout=120s
```

## Anti-Patterns to Avoid

1. **Don't echo secrets**: Never `echo $SECRET`
2. **Don't hardcode secrets**: Use `${{ secrets.* }}`
3. **Don't skip cleanup**: Always remove temp secret files
4. **Don't use `latest` in production**: Pin action versions
5. **Don't ignore failures**: Use `fail-fast: true`
6. **Don't forget rollout restart**: When using `latest` tag with K8s

## References
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- ADR-010: Azure AKS Cloud Deployment
- PHR-006: Helm Secrets with Special Characters
- PHR-007: AKS Auth/CORS Debugging
- Subagent: cicd-pipeline-subagent.md
