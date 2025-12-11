# PHR-003: datetime.utcnow() Deprecation in Python 3.12+

**Date**: 2025-12-12
**Phase**: Phase II/III (2nd Iteration)
**Category**: Python / Datetime / Deprecation

## Problem

When running tests or application, Python 3.12+ shows deprecation warnings:

```
DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for
removal in a future version. Use timezone-aware objects to represent datetimes
in UTC: datetime.datetime.now(datetime.UTC).
```

This warning appears in:
- SQLModel model definitions with `default_factory=datetime.utcnow`
- Manual datetime assignments like `task.updated_at = datetime.utcnow()`

## Root Cause

Python 3.12 deprecated `datetime.utcnow()` and `datetime.utcfromtimestamp()` because:

1. They return **naive** datetime objects (no timezone info)
2. Naive datetimes can cause subtle bugs when mixed with aware datetimes
3. The Python community is moving toward timezone-aware datetimes by default

## Solution

Use `datetime.now(UTC)` instead of `datetime.utcnow()`:

### 1. Import UTC from datetime module

```python
# ❌ OLD
from datetime import datetime

# ✅ NEW
from datetime import datetime, UTC
```

### 2. In SQLModel Field definitions

```python
# ❌ OLD - triggers deprecation warning
created_at: datetime = Field(default_factory=datetime.utcnow)

# ✅ NEW - use lambda wrapper
created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
```

**Why lambda?** `default_factory` expects a callable that takes no arguments. `datetime.now(UTC)` is not a callable - it's a method call. The lambda wraps it properly.

### 3. In manual assignments

```python
# ❌ OLD
task.updated_at = datetime.utcnow()

# ✅ NEW
task.updated_at = datetime.now(UTC)
```

## Files Fixed

- `backend/src/models/task.py` - Model definitions
- `backend/src/api/routes/tasks.py` - Route handlers

## Verification

Run tests and confirm no deprecation warnings:

```bash
cd backend
uv run pytest -W error::DeprecationWarning  # Fail on deprecation
```

Or filter to just see datetime warnings:

```bash
uv run pytest 2>&1 | grep -i "utcnow"  # Should return nothing
```

## Prevention Checklist

When writing new code with datetimes:

1. **Import UTC**: `from datetime import datetime, UTC`
2. **Use now(UTC)**: `datetime.now(UTC)` instead of `datetime.utcnow()`
3. **Lambda for default_factory**: `Field(default_factory=lambda: datetime.now(UTC))`
4. **Test with warnings**: `pytest -W error::DeprecationWarning`

## Related

- Python 3.12 What's New: https://docs.python.org/3.12/whatsnew/3.12.html
- PEP 615 (IANA Time Zone Database): https://peps.python.org/pep-0615/
- Skill Update: `.claude/skills/neon-sqlmodel.md` (Datetime Best Practices section)

---

**Part of**: Evolution of Todo Reusable Intelligence
**Tags**: python, datetime, deprecation, utcnow, timezone, UTC, SQLModel
