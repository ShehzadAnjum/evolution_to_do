# Dockerfile Creator Subagent

**Type**: Creator
**Used For**: Writing Dockerfiles for backend/frontend
**Version**: 1.0.0

## Purpose

Create optimized Dockerfiles for backend (Python) and frontend (Node.js).

## Backend Dockerfile Pattern

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Copy deps
COPY pyproject.toml uv.lock ./

# Install deps
RUN pip install uv && uv sync --frozen

# Copy code
COPY src/ ./src/

# Health check
HEALTHCHECK --interval=30s CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0"]
```

## Frontend Dockerfile Pattern

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
EXPOSE 3000
CMD ["node", "server.js"]
```

## Best Practices

- Multi-stage builds (smaller images)
- Layer caching (deps before code)
- Non-root user
- Health checks
- Explicit versions (not :latest)

---

**Related**: Infra DevOps Agent
