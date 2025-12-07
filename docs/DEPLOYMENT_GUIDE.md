# Phase II Deployment Guide

**Last Updated**: 2025-12-07  
**Status**: Ready for Deployment  
**Phase**: II - Full-Stack Web Application

---

## Prerequisites

Before deploying, ensure you have:

1. ✅ Neon PostgreSQL database (free tier available at https://neon.tech)
2. ✅ GitHub repository connected
3. ✅ Railway/Render/Fly.io account (for backend)
4. ✅ Vercel account (for frontend)
5. ✅ All tests passing locally (81/81 ✅)

---

## Step 1: Database Setup (Neon PostgreSQL)

### 1.1 Create Neon Database

1. Go to https://neon.tech and sign up/login
2. Create a new project
3. Copy the connection string (format: `postgresql://user:password@host/database?sslmode=require`)

### 1.2 Run Better Auth Migrations

**Important**: Run this FIRST before deploying backend, as the `tasks` table has a foreign key to `user`.

```bash
cd frontend

# Set your DATABASE_URL
export DATABASE_URL="postgresql://user:password@host/database?sslmode=require"

# Run migrations
npx @better-auth/cli migrate
```

This creates:
- `user` table
- `session` table
- `account` table (for OAuth)
- Other Better Auth tables

### 1.3 Create Tasks Table

The backend will create the `tasks` table automatically on first startup, or you can run:

```bash
cd backend

# Set your DATABASE_URL
export DATABASE_URL="postgresql://user:password@host/database?sslmode=require"

# Create tasks table
uv run python -c "from src.api.database import init_db; init_db()"
```

---

## Step 2: Generate Secrets

### 2.1 Generate Better Auth Secret

```bash
# Generate a secure 32+ character secret
openssl rand -hex 32
```

**Important**: Use the SAME secret for both backend and frontend!

---

## Step 3: Deploy Backend

### Option A: Railway (Recommended)

1. **Connect Repository**
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository

2. **Configure Project**
   - Set root directory: `backend`
   - Set start command: `uv run uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**
   ```
   DATABASE_URL=postgresql://user:password@host/database?sslmode=require
   BETTER_AUTH_SECRET=your-generated-secret-here
   BETTER_AUTH_URL=https://your-backend.railway.app
   CORS_ORIGINS=https://your-frontend.vercel.app
   ```

4. **Deploy**
   - Railway will automatically detect Python and install dependencies
   - Wait for deployment to complete
   - Copy the public URL (e.g., `https://your-backend.railway.app`)

### Option B: Render

1. **Create Web Service**
   - Go to https://render.com
   - Click "New" → "Web Service"
   - Connect your GitHub repository

2. **Configure**
   - Root Directory: `backend`
   - Build Command: `uv sync`
   - Start Command: `uv run uvicorn src.api.main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables** (same as Railway)

4. **Deploy**

### Option C: Fly.io

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login and Create App**
   ```bash
   fly auth login
   cd backend
   fly launch
   ```

3. **Set Secrets**
   ```bash
   fly secrets set DATABASE_URL="postgresql://..."
   fly secrets set BETTER_AUTH_SECRET="your-secret"
   fly secrets set BETTER_AUTH_URL="https://your-app.fly.dev"
   fly secrets set CORS_ORIGINS="https://your-frontend.vercel.app"
   ```

4. **Deploy**
   ```bash
   fly deploy
   ```

### Verify Backend Deployment

```bash
# Health check
curl https://your-backend-url.com/health

# Should return: {"status":"ok"}
```

---

## Step 4: Deploy Frontend (Vercel)

### 4.1 Connect Repository

1. Go to https://vercel.com
2. Click "Add New" → "Project"
3. Import your GitHub repository

### 4.2 Configure Project

1. **Root Directory**: Set to `frontend`
2. **Framework Preset**: Next.js (auto-detected)
3. **Build Command**: `npm run build` (default)
4. **Output Directory**: `.next` (default)

### 4.3 Set Environment Variables

```
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
BETTER_AUTH_SECRET=your-generated-secret-here (MUST MATCH BACKEND)
BETTER_AUTH_URL=https://your-frontend.vercel.app
NEXT_PUBLIC_APP_URL=https://your-frontend.vercel.app
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

**Important Notes**:
- `BETTER_AUTH_SECRET` must be EXACTLY the same as backend
- `NEXT_PUBLIC_API_URL` should be your backend URL
- `BETTER_AUTH_URL` should be your frontend URL (Vercel)

### 4.4 Deploy

1. Click "Deploy"
2. Wait for build to complete
3. Copy the Vercel URL (e.g., `https://your-app.vercel.app`)

### 4.5 Update Backend CORS

After getting your Vercel URL, update the backend's `CORS_ORIGINS` environment variable:

```
CORS_ORIGINS=https://your-app.vercel.app
```

Redeploy backend if needed.

---

## Step 5: Verify Deployment

### 5.1 Test Authentication

1. Visit your Vercel URL
2. Try to sign up with a new account
3. Verify you can log in
4. Check that you're redirected to `/tasks`

### 5.2 Test Task Operations

1. **Add Task**: Create a new task with title and description
2. **View Tasks**: Verify task appears in list
3. **Update Task**: Edit title/description
4. **Mark Complete**: Toggle completion checkbox
5. **Delete Task**: Delete a task
6. **Persistence**: Refresh page - tasks should persist

### 5.3 Test Multi-User Isolation

1. Create two accounts (User A and User B)
2. Log in as User A, create tasks
3. Log out, log in as User B
4. Verify User B cannot see User A's tasks
5. Try to access User A's task by ID - should get 403/404

### 5.4 Test API Endpoints

```bash
# Get JWT token (from browser dev tools or login flow)
TOKEN="your-jwt-token"

# List tasks
curl -H "Authorization: Bearer $TOKEN" \
  https://your-backend-url.com/api/tasks

# Create task
curl -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Task","description":"Test"}' \
  https://your-backend-url.com/api/tasks
```

---

## Step 6: Troubleshooting

### Issue: CORS Errors

**Symptoms**: Browser console shows CORS errors

**Solution**:
1. Verify `CORS_ORIGINS` in backend includes your Vercel URL
2. Check for trailing slashes (should be `https://app.vercel.app`, not `https://app.vercel.app/`)
3. Restart backend after changing CORS settings

### Issue: JWT Invalid

**Symptoms**: 401 Unauthorized errors

**Solution**:
1. Verify `BETTER_AUTH_SECRET` matches exactly in both frontend and backend
2. Clear browser cookies and re-login
3. Check that JWT token is being sent in `Authorization: Bearer <token>` header

### Issue: Database Connection Failed

**Symptoms**: 500 errors, database connection errors

**Solution**:
1. Verify `DATABASE_URL` is correct
2. Ensure `?sslmode=require` is included
3. Check Neon dashboard for connection status
4. Verify Better Auth migrations were run

### Issue: Tasks Table Not Found

**Symptoms**: 500 errors when creating tasks

**Solution**:
1. Run Better Auth migrations first: `npx @better-auth/cli migrate`
2. Then create tasks table: `uv run python -c "from src.api.database import init_db; init_db()"`

### Issue: Frontend Build Fails

**Symptoms**: Vercel build fails

**Solution**:
1. Check build logs for specific errors
2. Verify all environment variables are set
3. Ensure `package.json` has correct scripts
4. Check Node.js version (should be 20+)

---

## Step 7: Production Checklist

Before submitting Phase II:

- [ ] Backend deployed and accessible (public URL)
- [ ] Frontend deployed on Vercel (public URL)
- [ ] Better Auth migrations run
- [ ] Tasks table created
- [ ] All environment variables set correctly
- [ ] CORS configured properly
- [ ] User registration works
- [ ] User login/logout works
- [ ] All 5 task operations work (Add, View, Update, Delete, Complete)
- [ ] Tasks persist across refresh
- [ ] Multi-user isolation verified
- [ ] API endpoints accessible with JWT
- [ ] Health check endpoint works
- [ ] No console errors in browser
- [ ] Mobile responsive (test on phone)
- [ ] Demo video recorded (< 90 seconds)
- [ ] Submitted via hackathon form before Dec 14, 11:59 PM

---

## Environment Variables Reference

### Backend (.env or Platform Settings)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Neon PostgreSQL connection string | `postgresql://user:pass@host/db?sslmode=require` |
| `BETTER_AUTH_SECRET` | JWT signing secret (32+ chars) | `abc123...` (generate with `openssl rand -hex 32`) |
| `BETTER_AUTH_URL` | Backend URL for auth | `https://api.railway.app` |
| `CORS_ORIGINS` | Allowed frontend origins (comma-separated) | `https://app.vercel.app` |

### Frontend (.env.local or Vercel Settings)

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Neon PostgreSQL connection string (same as backend) | `postgresql://user:pass@host/db?sslmode=require` |
| `BETTER_AUTH_SECRET` | JWT signing secret (MUST MATCH BACKEND) | `abc123...` (same as backend) |
| `BETTER_AUTH_URL` | Frontend URL for Better Auth | `https://app.vercel.app` |
| `NEXT_PUBLIC_APP_URL` | Public app URL | `https://app.vercel.app` |
| `NEXT_PUBLIC_API_URL` | Backend API URL | `https://api.railway.app` |

---

## Quick Reference Commands

### Local Development

```bash
# Backend
cd backend
uv sync
uv run uvicorn src.api.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev

# Run Better Auth migrations
cd frontend
npx @better-auth/cli migrate
```

### Testing

```bash
# Backend tests
cd backend
uv run pytest -v

# Frontend tests
cd frontend
npm run test
```

### Database

```bash
# Create tasks table
cd backend
uv run python -c "from src.api.database import init_db; init_db()"
```

---

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review backend/README.md and frontend/README.md
3. Check deployment platform logs
4. Verify all environment variables are set correctly
5. Ensure database migrations were run

---

**Last Updated**: 2025-12-07  
**Next Steps**: After deployment, record demo video and submit Phase II


