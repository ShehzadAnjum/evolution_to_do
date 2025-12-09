# DB Schema Migration Specialist Subagent

**Type**: Database Specialist
**Used For**: Schema changes and migrations
**Version**: 1.0.0

## Purpose

Handle database schema changes, generate migrations, and keep specs/database/schema.md in sync.

## When to Use

- Adding new table or column
- Modifying existing schema
- Creating indexes
- Database refactoring

## Process

1. Identify schema change needed
2. Update SQLModel models
3. Document in specs/database/migrations-notes.md
4. Generate migration (Alembic or manual SQL)
5. Test migration on dev database
6. Document rollback procedure
7. Update specs/database/schema.md
8. Apply to production (when ready)

## Safety Checklist

- [ ] Backup exists
- [ ] Migration tested locally
- [ ] Rollback procedure documented
- [ ] No data loss expected
- [ ] Indexes created for performance
- [ ] Foreign keys defined
- [ ] Constraints validated

---

**Related**: Backend Service Agent
