# Backend Dockerfile for Evolution of Todo
# Multi-stage build for smaller production image

# ================================
# Stage 1: Builder
# ================================
FROM python:3.13-slim AS builder

WORKDIR /app

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pip dependencies directly (simpler than uv for Docker)
COPY backend/pyproject.toml ./

# Extract dependencies and install them
RUN pip install --no-cache-dir \
    "fastapi>=0.115.0" \
    "uvicorn[standard]>=0.32.0" \
    "sqlmodel>=0.0.22" \
    "psycopg2-binary>=2.9.9" \
    "python-jose[cryptography]>=3.3.0" \
    "python-dotenv>=1.0.0" \
    "pydantic-settings>=2.6.0" \
    "mcp>=1.23.3" \
    "openai>=2.9.0" \
    "httpx>=0.27.0" \
    "edge-tts>=6.1.0" \
    "aiomqtt>=2.0.0"

# ================================
# Stage 2: Production
# ================================
FROM python:3.13-slim AS production

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY backend/src ./src
COPY backend/main.py ./

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser
USER appuser

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PORT=8000

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

# Run the application
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
