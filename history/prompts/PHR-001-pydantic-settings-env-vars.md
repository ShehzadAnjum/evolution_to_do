# PHR-001: Pydantic Settings Extra Inputs Error

**Date**: 2025-12-10
**Phase**: Phase III
**Category**: Configuration / Environment Variables

## Problem

When adding a new environment variable (e.g., `OPENAI_API_KEY`) to `.env`, pydantic-settings throws:

```
pydantic_core._pydantic_core.ValidationError: 1 validation error for Settings
openai_api_key
  Extra inputs are not permitted [type=extra_forbidden, input_value='sk-...', input_type=str]
```

## Root Cause

Pydantic Settings (v2) by default forbids extra fields not defined in the Settings class. When you add a new env var to `.env` but don't define it in `config.py`, it rejects it.

## Solution

**Always add new environment variables to the Settings class in `backend/src/api/config.py`:**

```python
class Settings(BaseSettings):
    # ... existing fields ...

    # OpenAI (Phase III - AI Chatbot)
    openai_api_key: str = ""  # Default empty, set in .env
```

## Checklist for New Env Vars

1. Add variable to `backend/.env.example` (placeholder)
2. Add field to `Settings` class in `backend/src/api/config.py`
3. Add actual value to `backend/.env` (not committed)
4. Access via `get_settings().your_variable_name`

## Prevention

Before adding any new `.env` variable:
- Check `backend/src/api/config.py`
- Add the corresponding field to `Settings` class
- Use appropriate type hints and defaults

## Related Files

- `backend/src/api/config.py` - Settings class definition
- `backend/.env.example` - Template with placeholders
- `backend/.env` - Actual secrets (gitignored)

---

## Additional Lesson: Accessing Settings Values

### Problem

Using `os.getenv("VAR_NAME")` doesn't work with pydantic-settings because it loads `.env` into the Settings class, NOT into `os.environ`.

```python
# WRONG - returns None even if set in .env
api_key = os.getenv("OPENAI_API_KEY")
```

### Solution

Always access env vars through the Settings class:

```python
# CORRECT - reads from Settings which loads .env
from src.api.config import get_settings

settings = get_settings()
api_key = settings.openai_api_key
```

### Pattern for New Services

```python
from src.api.config import get_settings

def get_client():
    settings = get_settings()
    return SomeClient(api_key=settings.some_api_key)
```

---

**Part of**: Evolution of Todo Reusable Intelligence
**Tags**: pydantic, settings, environment, configuration, error-fix, os.getenv
