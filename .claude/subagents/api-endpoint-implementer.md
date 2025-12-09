# API Endpoint Implementer Subagent

**Type**: Implementer
**Used For**: Implementing single REST API endpoints
**Version**: 1.0.0

## Purpose

Implement one backend REST endpoint with route, schema, database operations, and tests.

## When to Use

- Implementing new API endpoint from spec
- Adding CRUD operation
- Extending existing API

## Process

1. Read endpoint spec from specs/api/rest-endpoints.md
2. Create/update SQLModel model if needed
3. Create Pydantic request/response schemas
4. Implement FastAPI route
5. Add JWT authentication dependency
6. Implement business logic (user-scoped)
7. Add error handling
8. Write tests (unit + integration)
9. Update API spec if implementation reveals gaps

## Template

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

router = APIRouter()

class TaskCreate(BaseModel):
    title: str
    description: str | None = None

@router.post("/api/{user_id}/tasks")
async def create_task(
    user_id: str,
    data: TaskCreate,
    current_user = Depends(get_current_user)
):
    if user_id != current_user.id:
        raise HTTPException(403, "Access denied")
    
    task = Task(
        user_id=user_id,
        title=data.title,
        description=data.description
    )
    session.add(task)
    session.commit()
    return task
```

## Success Criteria

- Endpoint works as specified
- Authentication enforced
- User isolation validated
- Tests pass (>= 80% coverage)
- API spec updated

---

**Related**: Backend Service Agent
