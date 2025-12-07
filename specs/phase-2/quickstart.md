# Quickstart: Phase II Web Application

**Feature**: Phase II - Full-Stack Web Application
**Date**: 2025-12-06

---

## Prerequisites

- Python 3.13+ with UV
- Node.js 20+ with npm
- Neon PostgreSQL account (free tier)
- Vercel account (free tier)
- Git

---

## 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/your-username/evolution_to_do.git
cd evolution_to_do
```

---

## 2. Database Setup (Neon)

1. Create account at https://neon.tech
2. Create new project
3. Copy connection string from dashboard
4. Save as `DATABASE_URL` (format: `postgresql://user:pass@host/db?sslmode=require`)

---

## 3. Backend Setup

```bash
# Navigate to backend
cd backend

# Install dependencies
uv sync

# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
BETTER_AUTH_SECRET=your-32-character-secret-key-here
BETTER_AUTH_URL=http://localhost:8000
CORS_ORIGINS=http://localhost:3000
EOF

# Run database migrations (creates tables)
uv run python -c "from src.api.database import init_db; init_db()"

# Start development server
uv run uvicorn src.api.main:app --reload --port 8000
```

**Verify**: Open http://localhost:8000/health

---

## 4. Frontend Setup

```bash
# Navigate to frontend (from project root)
cd frontend

# Install dependencies
npm install

# Create .env.local file
cat > .env.local << EOF
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_AUTH_URL=http://localhost:8000
EOF

# Start development server
npm run dev
```

**Verify**: Open http://localhost:3000

---

## 5. Test the Application

### Register
1. Go to http://localhost:3000/signup
2. Enter email and password
3. Click "Sign Up"

### Login
1. Go to http://localhost:3000/login
2. Enter credentials
3. Click "Sign In"

### Create Task
1. After login, you're on /tasks
2. Enter task title
3. Click "Add Task"

### Complete Workflow
1. Add a few tasks
2. Click checkbox to mark complete
3. Click edit to update
4. Click delete to remove
5. Refresh page - tasks persist!

---

## 6. Run Tests

### Backend Tests
```bash
cd backend
uv run pytest -v
```

### Frontend Tests
```bash
cd frontend
npm run test
```

---

## 7. Production Deployment

### Deploy Backend (Railway)

1. Connect GitHub repo to Railway
2. Set root directory: `backend`
3. Add environment variables:
   - `DATABASE_URL`
   - `BETTER_AUTH_SECRET`
   - `BETTER_AUTH_URL` (your Railway URL)
   - `CORS_ORIGINS` (your Vercel URL)
4. Deploy

### Deploy Frontend (Vercel)

1. Connect GitHub repo to Vercel
2. Set root directory: `frontend`
3. Add environment variables:
   - `NEXT_PUBLIC_API_URL` (your Railway URL)
   - `NEXT_PUBLIC_AUTH_URL` (your Railway URL)
4. Deploy

---

## Environment Variables Reference

### Backend (.env)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Neon connection string | `postgresql://...` |
| `BETTER_AUTH_SECRET` | JWT signing secret (32+ chars) | `your-secret-key...` |
| `BETTER_AUTH_URL` | Backend URL for auth | `https://api.example.com` |
| `CORS_ORIGINS` | Allowed frontend origins | `https://app.vercel.app` |

### Frontend (.env.local)

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `https://api.example.com` |
| `NEXT_PUBLIC_AUTH_URL` | Auth endpoint URL | `https://api.example.com` |

---

## Troubleshooting

### "CORS error"
- Check `CORS_ORIGINS` includes your frontend URL
- Restart backend after changing .env

### "Database connection failed"
- Verify `DATABASE_URL` is correct
- Ensure `?sslmode=require` is included
- Check Neon dashboard for connection status

### "JWT invalid"
- Ensure `BETTER_AUTH_SECRET` matches on frontend/backend
- Clear browser cookies and re-login

### "Module not found"
- Run `uv sync` in backend
- Run `npm install` in frontend

---

## API Testing with curl

```bash
# Health check
curl http://localhost:8000/health

# Register
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Login (save token)
TOKEN=$(curl -X POST http://localhost:8000/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}' \
  | jq -r '.token')

# Create task
curl -X POST http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test task","description":"From curl"}'

# List tasks
curl http://localhost:8000/api/tasks \
  -H "Authorization: Bearer $TOKEN"
```

---

## Demo Video Checklist

Record < 90 second video showing:

- [ ] User registration (signup page)
- [ ] User login (signin page)
- [ ] Add task (with title and description)
- [ ] View task list
- [ ] Mark task complete
- [ ] Update task
- [ ] Delete task
- [ ] User logout
- [ ] Login as different user (show isolation)

---

**Quickstart Version**: 1.0.0
**Created**: 2025-12-06
