# API Contract: Phase II Web Application

**Feature**: Phase II - Full-Stack Web Application
**Date**: 2025-12-06
**Base URL**: `https://api.example.com` (replace with actual deployment URL)

---

## Authentication

All task endpoints require JWT authentication via Bearer token.

```http
Authorization: Bearer <jwt_token>
```

---

## Endpoints Summary

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/health` | No | Health check |
| POST | `/auth/signup` | No | Register new user |
| POST | `/auth/signin` | No | Login user |
| POST | `/auth/signout` | Yes | Logout user |
| GET | `/api/tasks` | Yes | List user's tasks |
| POST | `/api/tasks` | Yes | Create task |
| GET | `/api/tasks/{id}` | Yes | Get single task |
| PUT | `/api/tasks/{id}` | Yes | Update task |
| DELETE | `/api/tasks/{id}` | Yes | Delete task |
| PATCH | `/api/tasks/{id}/complete` | Yes | Toggle completion |

---

## Health Check

### GET /health

Check if API is running.

**Request**:
```http
GET /health
```

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2025-12-06T12:00:00Z"
}
```

---

## Authentication Endpoints

### POST /auth/signup

Register a new user account.

**Request**:
```http
POST /auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Response** (201 Created):
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Errors**:
- `400 Bad Request` - Invalid email format or weak password
- `409 Conflict` - Email already registered

---

### POST /auth/signin

Login with existing credentials.

**Request**:
```http
POST /auth/signin
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response** (200 OK):
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

**Errors**:
- `401 Unauthorized` - Invalid credentials

---

### POST /auth/signout

Logout and invalidate session.

**Request**:
```http
POST /auth/signout
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "message": "Logged out successfully"
}
```

---

## Task Endpoints

### GET /api/tasks

List all tasks for the authenticated user.

**Request**:
```http
GET /api/tasks
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "tasks": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440001",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "is_complete": false,
      "created_at": "2025-12-06T10:00:00Z",
      "updated_at": "2025-12-06T10:00:00Z"
    },
    {
      "id": "550e8400-e29b-41d4-a716-446655440002",
      "user_id": "550e8400-e29b-41d4-a716-446655440000",
      "title": "Call dentist",
      "description": "",
      "is_complete": true,
      "created_at": "2025-12-06T09:00:00Z",
      "updated_at": "2025-12-06T11:00:00Z"
    }
  ],
  "total": 2,
  "completed": 1
}
```

**Errors**:
- `401 Unauthorized` - Missing or invalid token

---

### POST /api/tasks

Create a new task.

**Request**:
```http
POST /api/tasks
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_complete": false,
  "created_at": "2025-12-06T10:00:00Z",
  "updated_at": "2025-12-06T10:00:00Z"
}
```

**Errors**:
- `400 Bad Request` - Validation error (empty title, title too long)
- `401 Unauthorized` - Missing or invalid token

---

### GET /api/tasks/{id}

Get a single task by ID.

**Request**:
```http
GET /api/tasks/550e8400-e29b-41d4-a716-446655440001
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_complete": false,
  "created_at": "2025-12-06T10:00:00Z",
  "updated_at": "2025-12-06T10:00:00Z"
}
```

**Errors**:
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Task belongs to another user
- `404 Not Found` - Task does not exist

---

### PUT /api/tasks/{id}

Update an existing task.

**Request**:
```http
PUT /api/tasks/550e8400-e29b-41d4-a716-446655440001
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "Buy groceries and snacks",
  "description": "Milk, eggs, bread, chips"
}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries and snacks",
  "description": "Milk, eggs, bread, chips",
  "is_complete": false,
  "created_at": "2025-12-06T10:00:00Z",
  "updated_at": "2025-12-06T12:00:00Z"
}
```

**Errors**:
- `400 Bad Request` - Validation error
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Task belongs to another user
- `404 Not Found` - Task does not exist

---

### DELETE /api/tasks/{id}

Delete a task.

**Request**:
```http
DELETE /api/tasks/550e8400-e29b-41d4-a716-446655440001
Authorization: Bearer <token>
```

**Response** (204 No Content):
```
(empty body)
```

**Errors**:
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Task belongs to another user
- `404 Not Found` - Task does not exist

---

### PATCH /api/tasks/{id}/complete

Toggle task completion status.

**Request**:
```http
PATCH /api/tasks/550e8400-e29b-41d4-a716-446655440001/complete
Authorization: Bearer <token>
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440001",
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "is_complete": true,
  "created_at": "2025-12-06T10:00:00Z",
  "updated_at": "2025-12-06T12:00:00Z"
}
```

**Errors**:
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Task belongs to another user
- `404 Not Found` - Task does not exist

---

## Error Response Format

All errors follow a consistent format:

```json
{
  "detail": "Error message here",
  "status_code": 400
}
```

### Validation Errors (400):
```json
{
  "detail": [
    {
      "loc": ["body", "title"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Rate Limiting

| Endpoint | Limit |
|----------|-------|
| `/auth/*` | 10 requests/minute |
| `/api/tasks` | 100 requests/minute |

---

## CORS Configuration

```python
# Allowed origins
origins = [
    "https://your-app.vercel.app",
    "http://localhost:3000",  # Development
]
```

---

**Contract Version**: 1.0.0
**Created**: 2025-12-06
