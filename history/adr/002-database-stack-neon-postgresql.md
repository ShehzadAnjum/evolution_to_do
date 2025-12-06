# ADR-002: Database Stack with Neon PostgreSQL

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together.

- **Status:** Accepted
- **Date:** 2025-12-07
- **Feature:** Phase II - Full-Stack Web Application
- **Context:** Phase II requires persistent storage with multi-user isolation, moving from Phase I in-memory storage

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - Database choice affects scalability, deployment, cost
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - Self-hosted PostgreSQL, PlanetScale, Supabase, Neon
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - Affects backend, migrations, deployment, scaling
-->

## Decision

Use Neon Serverless PostgreSQL as the database stack with the following components:

**Database Layer:**
- **Provider:** Neon (https://neon.tech)
- **Database:** PostgreSQL 16+
- **Connection Type:** Serverless (automatic connection pooling)
- **ORM:** SQLModel (FastAPI integration)
- **Connection Library:** asyncpg (async Python PostgreSQL driver)
- **Connection Pooling:** NullPool (Neon handles pooling at infrastructure level)
- **SSL Mode:** Required

**Integration Pattern:**
- Connection string via environment variable (`DATABASE_URL`)
- SQLModel engine with NullPool
- Better Auth manages `users` table via migrations
- SQLModel creates `tasks` table via `SQLModel.metadata.create_all()`

## Consequences

### Positive

1. **Serverless Architecture:** Pay-per-use pricing, automatic scaling, no server management
2. **Free Tier Generous:** 3 GB storage, 100 hours compute per month (sufficient for Phase II-III)
3. **Instant Provisioning:** Database created in seconds, no manual setup
4. **Branching Support:** Database branching for development/staging environments (future use)
5. **Connection Pooling:** Built-in at infrastructure level (no PgBouncer needed)
6. **PostgreSQL Compliance:** Full PostgreSQL compatibility (no proprietary extensions)
7. **Backup & Recovery:** Automatic point-in-time recovery (1-day retention on free tier)
8. **Fast Performance:** Low latency via global edge network
9. **SQL Support:** Full SQL support (no limitations like some serverless databases)

### Negative

1. **Vendor Lock-in:** Migrating away from Neon requires database export/import
2. **Cold Start:** Inactive databases may have cold start latency (mitigated by free tier keeping DB warm)
3. **Regional Limitations:** Database region selection impacts latency (must choose closest to backend)
4. **Network Dependency:** Requires internet connection (no local development without Neon)
5. **Free Tier Limits:** 3 GB storage, 100 hours compute (may hit limits in Phase IV-V with heavy usage)
6. **Relatively New:** Neon is newer than traditional PostgreSQL providers (potential for edge cases)

## Alternatives Considered

### Alternative A: Self-Hosted PostgreSQL (Railway/Render)
- **Components:** Railway PostgreSQL addon or Render PostgreSQL
- **Pros:**
  - Full control over configuration
  - Traditional PostgreSQL experience
  - No vendor-specific features
- **Cons:**
  - Manual connection pooling (PgBouncer required)
  - Higher cost ($5-10/month minimum)
  - Manual backups and scaling
  - Requires more DevOps expertise
- **Why Rejected:** Violates "Quality Over Speed" - additional DevOps overhead not justified for Phase II

### Alternative B: PlanetScale (MySQL)
- **Components:** PlanetScale serverless MySQL
- **Pros:**
  - Serverless architecture
  - Generous free tier
  - Branching support
- **Cons:**
  - MySQL not PostgreSQL (Better Auth expects PostgreSQL)
  - Different SQL dialect (incompatible with Better Auth migrations)
  - No foreign key support on free tier (violates data integrity)
  - Would require custom Better Auth adapter
- **Why Rejected:** Constitution requirement - Phase II spec mandates PostgreSQL, not MySQL

### Alternative C: Supabase PostgreSQL
- **Components:** Supabase-hosted PostgreSQL
- **Pros:**
  - PostgreSQL-based
  - Free tier (500 MB storage)
  - Integrated with Supabase ecosystem (Auth, Storage, Realtime)
- **Cons:**
  - Free tier pauses after 7 days inactivity (unacceptable for demo)
  - Smaller storage limit (500 MB vs Neon 3 GB)
  - Vendor lock-in to Supabase ecosystem
  - Row Level Security patterns not needed (we handle auth in backend)
- **Why Rejected:** Neon offers better free tier limits and no automatic pausing

### Alternative D: Local PostgreSQL + Migrations
- **Components:** Local Docker PostgreSQL + Alembic migrations
- **Pros:**
  - Full local development
  - No vendor lock-in
  - No network dependency
- **Cons:**
  - Requires Docker setup (violates Phase II rules - Docker is Phase IV)
  - Requires Alembic migration management (additional complexity)
  - Deployment requires PostgreSQL hosting anyway
  - Team members need identical local setup
- **Why Rejected:** Docker prohibited in Phase II, additional migration tooling overhead

### Alternative E: SQLite
- **Components:** Local SQLite file
- **Pros:**
  - Zero setup
  - No network dependency
  - Perfect for local development
- **Cons:**
  - **Explicitly prohibited in Phase II spec** (specs/phase-2/spec.md line 28)
  - No multi-user concurrency at scale
  - Deployment requires migration to PostgreSQL anyway
- **Why Rejected:** Constitution violation - Phase II spec explicitly prohibits SQLite

## References

- Feature Spec: `specs/phase-2/spec.md` (FR-009, Technology Stack table)
- Implementation Plan: `specs/phase-2/plan.md` (lines 30, 337-376)
- Related ADRs: ADR-001 (Better Auth), ADR-003 (SQLModel)
- Neon Documentation: https://neon.tech/docs
- Implementation Evidence: `backend/src/api/database.py`, `backend/src/api/config.py`
- Constitution: `.specify/memory/constitution.md` (Phase II rules lines 702-762)
