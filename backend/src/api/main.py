"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .routes import health, tasks, chat, events
from .database import init_db
from .config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown."""
    # Startup: Initialize database tables
    import os
    port = os.environ.get("PORT", "NOT_SET")
    print(f"🚀 Starting FastAPI application...")
    print(f"🔍 DEBUG: PORT environment variable = {port}")
    print(f"🔍 DEBUG: All PORT-related env vars: {[k for k in os.environ.keys() if 'PORT' in k]}")
    try:
        init_db()
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️  Warning: Database initialization failed: {e}")
        print("   Tables may need to be created manually")
        import traceback
        traceback.print_exc()

    yield

    # Shutdown: Cleanup if needed
    print("🛑 Shutting down FastAPI application...")


# Create FastAPI app
app = FastAPI(
    title="Todo App API",
    description="Phase II - Full-Stack Web Application API",
    version="0.2.0",
    lifespan=lifespan,
)

# Configure CORS
settings = get_settings()
origins = settings.cors_origins.split(",") if "," in settings.cors_origins else [settings.cors_origins]
# Add common development ports and known frontend deployments
origins.extend([
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3001",
    "https://evolution-to-do.vercel.app",
    "https://evolution-todo-v1.vercel.app",  # iteration-1 deployment
])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router)
app.include_router(tasks.router)
app.include_router(chat.router)
app.include_router(events.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Todo App API",
        "version": "0.2.0",
        "docs": "/docs"
    }
