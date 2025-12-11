# ADR-006: Schema Evolution Strategy for Iterative Development

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together.

- **Status:** Accepted
- **Date:** 2025-12-12
- **Feature:** Phase II/III 2nd Iteration - Adding priority, category, due_date
- **Context:** Need to evolve database schema while maintaining backward compatibility and zero-downtime deployments

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - Schema evolution affects all future iterations
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - Alembic, manual SQL, SQLModel auto-migrate
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - Affects backend, frontend, database, deployment
-->

## Decision

Adopt a **manual idempotent migration script** strategy for schema evolution:

**Migration Approach:**
- **Scripts Location:** `backend/scripts/migrate_v*.py`
- **Execution:** Manual run before deployment (`uv run python scripts/migrate_v2.py`)
- **Safety:** Idempotent (check column existence, use `IF NOT EXISTS`)
- **Defaults:** Always provide defaults for new columns
- **Indexes:** Create indexes for columns used in filtering

**Backward Compatibility Rules:**
1. New columns must have sensible defaults (not NULL without default)
2. Old API clients must continue working (new fields optional in requests)
3. New API responses include new fields (clients ignore unknown fields)
4. Database changes deploy BEFORE application changes

**Version Tagging:**
- Tag before schema changes: `v1.0.0-phase2-3-web`
- Tag after schema changes: `v2.0.0-phase2-3-web` (future)

## Consequences

### Positive

1. **Zero Downtime:** Schema changes can be applied without stopping the application
2. **Backward Compatible:** Old API clients continue working until upgraded
3. **Idempotent:** Safe to run migrations multiple times (no errors on re-run)
4. **Explicit:** Migration steps are visible and auditable in version control
5. **Simple:** No complex migration tooling to maintain (no Alembic dependency)
6. **Testable:** Can test migration on staging before production
7. **Rollback Friendly:** Tags allow reverting to previous schema if needed

### Negative

1. **Manual Process:** Must remember to run migration scripts before deployment
2. **No Auto-Rollback:** Rolling back requires manual SQL or restoring from backup
3. **Schema Drift Risk:** Production schema might differ if migration skipped
4. **No Migration History:** No automatic tracking of which migrations have run

## Alternatives Considered

### Alternative A: Alembic Migrations
- **Components:** Alembic + SQLAlchemy
- **Pros:**
  - Industry standard for SQLAlchemy projects
  - Automatic migration generation
  - Tracks migration history in database
  - Supports rollback
- **Cons:**
  - Additional dependency and complexity
  - Overkill for simple column additions
  - Requires learning Alembic DSL
  - Can generate incorrect migrations requiring manual fixes
- **Why Rejected:** Too heavyweight for current scope; simple scripts sufficient

### Alternative B: SQLModel Auto-Migrate
- **Components:** `SQLModel.metadata.create_all(engine)`
- **Pros:**
  - Zero configuration
  - Automatic table creation
- **Cons:**
  - Only creates tables, doesn't add columns to existing tables
  - No support for ALTER TABLE operations
  - Would lose existing data (DROP + CREATE)
- **Why Rejected:** Doesn't support column additions to existing tables

### Alternative C: Raw SQL Files
- **Components:** `.sql` files run via psql
- **Pros:**
  - Pure SQL, no Python dependency
  - Can be run directly by DBA
- **Cons:**
  - No Python environment access
  - No conditional logic (check if column exists)
  - Connection string management separate
- **Why Rejected:** Python scripts provide better error handling and logging

## Implementation Evidence

**Migration Script Pattern** (`backend/scripts/migrate_v2.py`):
```python
def run_migration():
    engine = create_engine(os.getenv("DATABASE_URL"))

    with Session(engine) as session:
        # Check existing schema
        result = session.exec(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'tasks'
        """))
        existing_columns = [row[0] for row in result]

        # Idempotent column addition
        if "priority" not in existing_columns:
            session.exec(text("""
                ALTER TABLE tasks
                ADD COLUMN IF NOT EXISTS priority VARCHAR(10) DEFAULT 'medium'
            """))
            session.commit()

        # Safe index creation
        session.exec(text("""
            CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority)
        """))
        session.commit()
```

**v2.0.0 Schema Changes:**
- `priority` VARCHAR(10) DEFAULT 'medium'
- `category` VARCHAR(50) DEFAULT 'general'
- `due_date` DATE NULL

**API Backward Compatibility:**
- `TaskCreate` accepts new fields as optional
- `TaskRead` returns new fields (clients ignore if not needed)
- Existing v1 API calls continue working

## References

- Feature Spec: `specs/ui/design-spec-v2.md`
- Migration Script: `backend/scripts/migrate_v2.py`
- Model Changes: `backend/src/models/task.py`
- Related Skill: `.claude/skills/neon-sqlmodel.md` (Migration Patterns section)
- Related ADRs: ADR-002 (Neon PostgreSQL), ADR-003 (SQLModel ORM)
