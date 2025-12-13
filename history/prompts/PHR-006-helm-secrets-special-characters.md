# PHR-006: Helm Secrets with Special Characters

## Date
2025-12-14

## Category
Infrastructure / Kubernetes / Helm

## Problem Statement
When deploying to AKS with Helm, the DATABASE_URL containing special characters (`:`, `/`, `@`, `?`, `=`) was not being passed correctly via `--set` flag, resulting in empty secrets and application crash.

## Initial Approach (Failed)
```bash
helm upgrade --install myapp ./chart \
  --set backend.env.DATABASE_URL="postgresql://user:pass@host/db?sslmode=require"
```

**Result**: Secret contained empty string. SQLAlchemy threw:
```
sqlalchemy.exc.ArgumentError: Could not parse SQLAlchemy URL from given URL string
```

## Root Cause
Helm's `--set` flag interprets special characters. URLs with `://`, `@`, `?`, `=` get parsed incorrectly or truncated.

## Solution
Use a values file instead of `--set` for complex strings:

```bash
# Create values file with environment variables
export $(grep -v '^#' .env | xargs)
cat > /tmp/secrets-values.yaml << EOF
backend:
  env:
    DATABASE_URL: "${DATABASE_URL}"
    BETTER_AUTH_SECRET: "${BETTER_AUTH_SECRET}"
    OPENAI_API_KEY: "${OPENAI_API_KEY}"
EOF

# Deploy with values file
helm upgrade --install myapp ./chart -f /tmp/secrets-values.yaml

# Clean up
rm /tmp/secrets-values.yaml
```

## Alternative Solutions

### 1. Base64 Encode (For CI/CD)
```yaml
# In GitHub Actions
- name: Deploy
  run: |
    helm upgrade --install myapp ./chart \
      --set backend.env.DATABASE_URL_B64=$(echo -n "${{ secrets.DATABASE_URL }}" | base64)
```
Then decode in the Helm template.

### 2. Use --set-string
```bash
helm upgrade --install myapp ./chart \
  --set-string backend.env.DATABASE_URL="$DATABASE_URL"
```
Note: Still may fail with certain characters.

### 3. External Secrets Operator
For production, use External Secrets Operator to pull from Azure Key Vault or AWS Secrets Manager.

## Key Learnings

| Issue | Solution |
|-------|----------|
| `--set` truncates URLs | Use values file `-f` |
| Special chars in secrets | Quote properly in YAML |
| CI/CD secrets | Use GitHub secrets + values file |
| Production secrets | External Secrets Operator |

## Verification
```bash
# Check secret content after deployment
kubectl get secret myapp-secrets -o jsonpath='{.data.database-url}' | base64 -d
```

## References
- Helm Documentation: [Using --set](https://helm.sh/docs/intro/using_helm/#the-format-and-limitations-of---set)
- ADR-010: Azure AKS Cloud Deployment
