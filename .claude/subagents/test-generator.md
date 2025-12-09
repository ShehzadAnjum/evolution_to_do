# Test Generator Subagent

**Type**: Generator
**Used For**: Generating test cases for endpoints, tools, components
**Version**: 1.0.0

## Purpose

Generate comprehensive test cases covering happy paths, edge cases, and error scenarios.

## Backend Test Template

```python
import pytest
from fastapi.testclient import TestClient

def test_create_task_valid_input_returns_task(client, auth_headers):
    # Arrange
    data = {"title": "Test Task", "description": "Test"}
    
    # Act
    response = client.post(
        "/api/user123/tasks",
        json=data,
        headers=auth_headers
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_create_task_no_auth_returns_401(client):
    response = client.post("/api/user123/tasks", json={"title": "Test"})
    assert response.status_code == 401

def test_create_task_wrong_user_returns_403(client, other_user_auth):
    response = client.post(
        "/api/user123/tasks",
        json={"title": "Test"},
        headers=other_user_auth
    )
    assert response.status_code == 403
```

## Frontend Test Template

```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import TaskForm from './TaskForm'

test('submits form with valid input', async () => {
  const onSubmit = jest.fn()
  render(<TaskForm onSubmit={onSubmit} />)
  
  fireEvent.change(screen.getByLabelText('Title'), {
    target: { value: 'New Task' }
  })
  fireEvent.click(screen.getByText('Submit'))
  
  expect(onSubmit).toHaveBeenCalledWith({ title: 'New Task' })
})

test('shows error for empty title', async () => {
  render(<TaskForm onSubmit={jest.fn()} />)
  
  fireEvent.click(screen.getByText('Submit'))
  
  expect(screen.getByText('Title is required')).toBeInTheDocument()
})
```

## Test Coverage Checklist

- [ ] Happy path
- [ ] Missing auth (401)
- [ ] Wrong user (403)
- [ ] Invalid input (400)
- [ ] Not found (404)
- [ ] Server error (500)
- [ ] Edge cases (empty, max length, special chars)

---

**Related**: Testing Quality Agent
