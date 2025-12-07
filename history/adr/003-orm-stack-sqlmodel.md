# ADR-003: ORM Stack with SQLModel

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together.

- **Status:** Accepted
- **Date:** 2025-12-07
- **Feature:** Phase II - Full-Stack Web Application
- **Context:** Phase II requires type-safe database ORM that integrates with FastAPI and PostgreSQL

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - ORM choice affects data modeling, queries, migrations
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - SQLAlchemy, Django ORM, Tortoise ORM, SQLModel
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - Affects backend models, API layer, database schema
-->

## Decision

Use SQLModel as the ORM stack with the following components:

**ORM Layer:**
- **Framework:** SQLModel v0.0.22
- **Underlying Engine:** SQLAlchemy Core (SQLModel is built on top)
- **Validation:** Pydantic v2 (built into SQLModel)
- **Type System:** Full Python type hints
- **Schema Definition:** Python classes with Field() descriptors
- **Session Management:** SQLModel Session (async support via SQLAlchemy)
- **Query Builder:** SQLModel select() (type-safe queries)

**Integration Pattern:**
- Single model class serves as both SQLAlchemy table AND Pydantic schema
- Automatic API request/response validation via FastAPI
- Database connection via `create_engine()` with asyncpg
- Session dependency injection via FastAPI `Depends(get_session)`

## Consequences

### Positive

1. **Type Safety:** Full Python type hints - IDE autocomplete, static analysis (mypy)
2. **Pydantic Integration:** Automatic request/response validation in FastAPI (no duplicate schemas)
3. **Developer Experience:** Single model definition serves multiple purposes (DRY principle)
4. **FastAPI Native:** Designed by FastAPI creator (Sebastian Ramirez) for seamless integration
5. **SQLAlchemy Foundation:** Inherits battle-tested SQLAlchemy Core (mature, stable)
6. **Learning Curve:** Simpler than raw SQLAlchemy (less boilerplate)
7. **Migration Path:** Can drop down to SQLAlchemy when needed (e.g., complex joins)
8. **Async Support:** Full async/await support for modern Python (Python 3.13+)
9. **Schema Reuse:** TaskBase, TaskCreate, TaskUpdate, TaskRead share base fields (line 53-97 in task.py)

### Negative

1. **Ecosystem Maturity:** Newer than SQLAlchemy (v0.0.x - not 1.0 yet)
2. **Limited Documentation:** Smaller community compared to SQLAlchemy
3. **Migration Tools:** No built-in migration tool (would need Alembic for complex migrations)
4. **Advanced Features:** Some SQLAlchemy features require dropping down to Core
5. **Breaking Changes:** Pre-1.0 version may have API changes (risk for long-term maintenance)
6. **Relationship Complexity:** Complex relationships easier in SQLAlchemy ORM than SQLModel

## Alternatives Considered

### Alternative A: Raw SQLAlchemy ORM
- **Components:** SQLAlchemy 2.0 ORM + Pydantic schemas
- **Pros:**
  - Mature ecosystem (v2.0 stable)
  - Extensive documentation
  - Advanced relationship handling
  - Alembic migrations built-in
- **Cons:**
  - Duplicate model definitions (SQLAlchemy model + Pydantic schema)
  - More boilerplate code (~2x lines vs SQLModel)
  - Steeper learning curve
  - Manual synchronization between database model and API schema
- **Why Rejected:** Violates DRY principle - SQLModel eliminates duplicate schemas while providing same power

### Alternative B: Django ORM
- **Components:** Django 5.0 + Django REST Framework
- **Pros:**
  - Mature ORM (15+ years)
  - Built-in migration system (makemigrations/migrate)
  - Admin interface
  - Extensive ecosystem
- **Cons:**
  - Requires full Django framework (heavyweight for API-only)
  - Different paradigm from FastAPI (MTV vs dependency injection)
  - No Pydantic integration (manual serializers)
  - Synchronous by default (async support limited)
  - **Violates Phase II spec** - requires FastAPI, not Django
- **Why Rejected:** Constitution violation - Phase II mandates FastAPI

### Alternative C: Tortoise ORM
- **Components:** Tortoise ORM (async-first ORM)
- **Pros:**
  - Async-native (no sync overhead)
  - Django-like API (familiar)
  - Built-in migration support (aerich)
  - Pydantic integration
- **Cons:**
  - Smaller ecosystem than SQLAlchemy
  - Less mature (fewer edge cases handled)
  - No SQLAlchemy compatibility (harder to drop down)
  - Less FastAPI integration examples
- **Why Rejected:** SQLModel offers better FastAPI integration + SQLAlchemy foundation

### Alternative D: Peewee
- **Components:** Peewee ORM
- **Pros:**
  - Lightweight
  - Simple API
  - Built-in migrations
- **Cons:**
  - Synchronous only (no async support)
  - No Pydantic integration
  - Smaller community
  - **Violates Phase II async requirement** - FastAPI is async-first
- **Why Rejected:** No async support incompatible with FastAPI best practices

## Implementation Evidence

**Model Definition** (`backend/src/models/task.py` lines 53-97):
```python
class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)
    is_complete: bool = Field(default=False)

class TaskDB(TaskBase, table=True):
    # Database model (extends base)
    __tablename__ = "tasks"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreate(SQLModel):
    # API request schema (reuses base fields)
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", max_length=2000)

class TaskRead(TaskBase):
    # API response schema (extends base)
    id: UUID
    user_id: str
    created_at: datetime
```

**Query Pattern** (`backend/src/api/routes/tasks.py` line 25):
```python
statement = select(TaskDB).where(TaskDB.user_id == user_id).order_by(TaskDB.created_at.desc())
tasks = session.exec(statement).all()
```

**Validation** - Automatic via FastAPI + SQLModel:
- Title length validated by `Field(min_length=1, max_length=200)`
- Type checking enforced at runtime (400 error if invalid)
- No manual validation code needed

## References

- Feature Spec: `specs/phase-2/spec.md` (FR-006 through FR-010, Technology Stack)
- Implementation Plan: `specs/phase-2/plan.md` (lines 27, 89-97 data model section)
- Data Model: `specs/phase-2/data-model.md` (lines 88-130)
- Related ADRs: ADR-002 (Neon PostgreSQL), ADR-004 (user_id as TEXT)
- SQLModel Documentation: https://sqlmodel.tiangolo.com/
- Implementation Evidence: `backend/src/models/task.py`, `backend/src/api/routes/tasks.py`
- Constitution: `.specify/memory/constitution.md` (Type safety principle)
