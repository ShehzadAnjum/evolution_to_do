# ADR-004: User ID as TEXT in Tasks Table

> **Scope**: Technical decision for database schema compatibility between Better Auth and SQLModel.

- **Status:** Accepted
- **Date:** 2025-12-07
- **Feature:** Phase II - Full-Stack Web Application
- **Context:** Better Auth manages users table with user.id as TEXT, but tasks table needs UUID for task.id

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - Foreign key constraint affects data integrity
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - UUID foreign key, custom Better Auth adapter, dual ID system
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - Affects database schema, API queries, type system
-->

## Decision

Use TEXT (string) for `tasks.user_id` column instead of UUID to match Better Auth's user.id type:

**Schema Decision:**
- **tasks.id**: UUID (task identifier - our choice)
- **tasks.user_id**: TEXT (foreign key to users.id - Better Auth's choice)
- **users.id**: TEXT (managed by Better Auth - not configurable)

**Type System:**
```python
# backend/src/models/task.py
class TaskDB(TaskBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True)  # TEXT, not UUID
    # Note: FK constraint at DB level only (not in SQLModel)
```

**Rationale:**
- Better Auth controls users table schema (cannot change user.id to UUID)
- Foreign key must match referenced column type (TEXT = TEXT)
- SQLModel allows mixing UUID (tasks.id) with TEXT (tasks.user_id)

## Consequences

### Positive

1. **Database Integrity:** Foreign key constraint enforces referential integrity (`tasks.user_id` must exist in `users.id`)
2. **Better Auth Compatibility:** No custom adapter or schema overrides needed
3. **Automatic Cascade:** `ON DELETE CASCADE` removes user's tasks when user deleted
4. **Index Performance:** Index on user_id enables fast task lookups by user
5. **Type Safety:** Python type hints preserve type checking (`user_id: str`)
6. **JWT Compatibility:** JWT sub claim is string anyway (matches user_id type)

### Negative

1. **Type Inconsistency:** tasks.id is UUID but tasks.user_id is TEXT (mixed types in same table)
2. **Storage Overhead:** TEXT user_id uses more bytes than UUID (36 chars vs 16 bytes)
3. **SQLModel Metadata:** Cannot define foreign key in SQLModel (would cause metadata resolution errors)
4. **Migration Complexity:** If switching away from Better Auth, would need to migrate user_id column type
5. **Type Confusion:** Developers might expect user_id to be UUID like task_id

## Alternatives Considered

### Alternative A: UUID Foreign Key (Custom Better Auth Adapter)
- **Approach:** Override Better Auth user table to use UUID for user.id
- **Pros:**
  - Type consistency (both task.id and task.user_id would be UUID)
  - Smaller storage footprint (UUID is 16 bytes vs 36-char TEXT)
- **Cons:**
  - Requires custom Better Auth adapter (undocumented, high complexity)
  - Better Auth migrations wouldn't work (`npx @better-auth/cli migrate`)
  - Risk of breaking Better Auth updates
  - **Estimated 4-6 hours additional work** (adapter development + testing)
- **Why Rejected:** Violates "Quality Over Speed" - custom adapter adds complexity without proportional value

### Alternative B: Dual ID System (UUID + TEXT)
- **Approach:** Store both UUID and TEXT in users table, use UUID for foreign key
- **Schema:**
  ```sql
  users.id (TEXT, primary key) -- Better Auth
  users.uuid (UUID, unique) -- Custom column
  tasks.user_id (UUID) -- Foreign key to users.uuid
  ```
- **Pros:**
  - Type consistency in tasks table
  - Better Auth compatibility maintained
- **Cons:**
  - Duplicate IDs in users table (violates normalization)
  - Additional index required (users.uuid)
  - Must maintain UUID generation alongside Better Auth
  - Confusing for developers (two user identifiers)
- **Why Rejected:** Adds unnecessary complexity, violates database normalization principles

### Alternative C: No Foreign Key Constraint
- **Approach:** Store user_id as TEXT but don't define foreign key constraint
- **Pros:**
  - No type mismatch issues
  - Simpler SQLModel definition
- **Cons:**
  - **Data integrity risk:** Orphaned tasks if user deleted manually
  - No automatic cascade delete
  - Can insert invalid user_id (referential integrity lost)
  - **Violates data-model.md specification** (line 75 requires FK constraint)
- **Why Rejected:** Sacrifices data integrity for convenience (unacceptable for production)

### Alternative D: Use Different Auth System
- **Approach:** Replace Better Auth with auth system that uses UUID for user.id
- **Candidates:** Custom auth with UUID, Supabase Auth (supports UUID)
- **Pros:**
  - Type consistency throughout database
  - Full control over user schema
- **Cons:**
  - **Violates ADR-001 decision** (Better Auth already chosen)
  - Would require rewriting all auth code (~8 hours)
  - Loses Better Auth benefits (security, session management)
  - **Violates sunk cost principle** (auth already implemented and tested)
- **Why Rejected:** Constitution principle "Finish One Thing Before Starting Next" - auth is complete

## Implementation Details

**Database Foreign Key** (applied manually, not in SQLModel):
```sql
ALTER TABLE tasks
ADD CONSTRAINT fk_tasks_user
FOREIGN KEY (user_id)
REFERENCES users(id)
ON DELETE CASCADE;
```

**SQLModel Definition** (`backend/src/models/task.py` line 70):
```python
# Cannot define FK in SQLModel due to metadata resolution issues
# FK constraint exists at database level only
user_id: str = Field(index=True, description="Owner user ID")
```

**Comment Justification** (line 67-69):
```python
# Note: Foreign key constraint exists at database level
# We don't define it here to avoid SQLModel metadata resolution issues
# The user table is managed by Better Auth (uses TEXT for user.id)
```

## Migration Strategy

If migrating away from Better Auth in future:

1. **Option A:** Keep TEXT user_id (simplest)
2. **Option B:** Migrate user_id to UUID:
   ```sql
   -- 1. Add uuid column
   ALTER TABLE users ADD COLUMN uuid_id UUID DEFAULT gen_random_uuid();
   -- 2. Update tasks FK
   ALTER TABLE tasks ALTER COLUMN user_id TYPE UUID USING uuid_id::uuid;
   -- 3. Re-create FK constraint
   ```

## References

- Feature Spec: `specs/phase-2/spec.md` (FR-007: Associate tasks with authenticated user)
- Data Model: `specs/phase-2/data-model.md` (lines 62-84 - tasks table schema)
- Related ADRs: ADR-001 (Better Auth), ADR-002 (Neon PostgreSQL), ADR-003 (SQLModel)
- Implementation Evidence: `backend/src/models/task.py` lines 67-72
- Better Auth User Schema: Uses TEXT for user.id (not configurable)
- Constitution: `.specify/memory/constitution.md` (Data integrity principle)
