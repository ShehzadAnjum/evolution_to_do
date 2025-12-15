---
name: github-actions-cicd
description: GitHub Actions CI/CD patterns for Docker builds and Kubernetes deployments. Use when creating workflows for automated testing, building container images, or deploying to cloud platforms.
---

# GitHub Actions CI/CD

## Basic CI Workflow

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.13"
      - run: pip install -e ".[test]"
      - run: pytest

  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Login to GHCR
        run: echo "${{ secrets.GITHUB_TOKEN }}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin
      - name: Build and push
        run: |
          docker build -t ghcr.io/${{ github.repository }}/app:latest .
          docker push ghcr.io/${{ github.repository }}/app:latest
```

## CD with Azure AKS

```yaml
name: CD
on:
  workflow_run:
    workflows: ["CI"]
    types: [completed]
    branches: [main]

jobs:
  deploy:
    if: ${{ github.event.workflow_run.conclusion == 'success' }}
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}
      - name: Get AKS credentials
        run: az aks get-credentials --resource-group ${{ vars.RESOURCE_GROUP }} --name ${{ vars.CLUSTER_NAME }}
      - name: Deploy
        run: |
          helm upgrade --install app ./infra/helm/chart
          kubectl rollout restart deployment/app
```

## Secrets Setup

Required secrets in GitHub repo settings:
- `AZURE_CREDENTIALS` - Service principal JSON
- `DATABASE_URL` - Database connection string
- `OPENAI_API_KEY` - API keys

## Best Practices

- Use `workflow_run` to chain CI→CD
- Always `rollout restart` when using `latest` tag
- Store secrets in GitHub Secrets, not in code
- Use `vars` for non-sensitive configuration
