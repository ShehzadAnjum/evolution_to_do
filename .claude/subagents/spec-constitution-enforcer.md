# Spec Constitution Enforcer Subagent

**Type**: Validator/Auditor
**Used For**: Pre-commit checks, phase gate validation, drift detection
**Version**: 1.0.0

## Purpose

Detect drift and inconsistencies between specs, constitution, and implementation. Ensure code aligns with specifications and constitutional principles.

## When to Use

- Before major commits
- Before phase submissions
- Before major refactors
- When specs and code seem out of sync
- During code reviews

## Inputs

- Spec files (specs/*)
- Code files (backend/, frontend/)
- Constitution (specs/constitution.md)
- Phase definitions

## Process

1. **Read Specifications**
   - Current phase spec
   - Feature specs
   - API/database specs

2. **Check Implementation**
   - Verify features match specs
   - Check API endpoints exist as specified
   - Validate database schema matches
   - Ensure test coverage per specs

3. **Detect Drift**
   - Code implements unspecified features (scope creep)
   - Specified features not implemented
   - API contracts don't match specs
   - Database schema mismatches

4. **Generate Report**
   - List discrepancies
   - Severity (critical, high, medium, low)
   - Recommendations for fixes

## Example Check

```bash
# Check Phase II alignment
- Spec says: GET /api/{user_id}/tasks
- Code has: GET /api/{user_id}/tasks ✅
- Tests exist: ✅
- User isolation enforced: ✅

# Check for spec drift
- Code has: GET /api/admin/users
- Spec mentions this: ❌ (scope creep)
```

## Success Criteria

- All specified features implemented
- No unspecified features
- API contracts match specs
- Test coverage meets standards
- Phase gates pass

---

**Related**: System Architect Agent, Testing Quality Agent
