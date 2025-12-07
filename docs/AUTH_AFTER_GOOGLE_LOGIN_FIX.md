# Fixing "Authentication required" After Google Login

## Problem
After successfully logging in with Google OAuth, you can see your name/email in the header, but the tasks page shows "Authentication required. Please log in to view your tasks."

This means:
- ✅ Google OAuth login worked (Better Auth session is valid)
- ❌ JWT token generation or backend API call is failing

## Root Causes

The most common causes are:

1. **Backend not running** - FastAPI backend must be running on port 8000
2. **BETTER_AUTH_SECRET mismatch** - Frontend and backend must use the SAME secret
3. **CORS configuration** - Backend must allow requests from your frontend port
4. **NEXT_PUBLIC_API_URL not set** - Frontend needs to know where the backend is

## Solution Steps

### Step 1: Check if Backend is Running

The backend must be running for the tasks API to work:

```bash
# Check if backend is running
curl http://localhost:8000/health

# Should return: {"status":"ok","timestamp":"..."}
```

**If backend is not running:**

```bash
cd backend
uv sync
uv run uvicorn src.api.main:app --reload --port 8000
```

Keep this terminal window open - the backend needs to stay running.

### Step 2: Verify BETTER_AUTH_SECRET Matches

**Critical**: The `BETTER_AUTH_SECRET` must be EXACTLY the same in both frontend and backend.

**Frontend (`frontend/.env.local`):**
```env
BETTER_AUTH_SECRET=your-secret-here-must-be-32-chars-minimum
```

**Backend (`backend/.env` or environment variables):**
```env
BETTER_AUTH_SECRET=your-secret-here-must-be-32-chars-minimum
```

**Check both files match exactly:**
```bash
# Frontend
cd frontend
grep BETTER_AUTH_SECRET .env.local

# Backend  
cd backend
grep BETTER_AUTH_SECRET .env
# or check environment variables if deployed
```

**If they don't match:**
1. Choose one secret (generate a new one if needed: `openssl rand -hex 32`)
2. Update BOTH frontend `.env.local` AND backend `.env`
3. Restart BOTH frontend and backend servers

### Step 3: Verify CORS Configuration

The backend must allow requests from your frontend port.

**Backend (`backend/.env` or environment):**
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://localhost:3002
```

Or if you're using the default config, update `backend/src/api/config.py`:
```python
cors_origins: str = "http://localhost:3000,http://localhost:3001"
```

**Restart backend after changing CORS settings.**

### Step 4: Verify NEXT_PUBLIC_API_URL

**Frontend (`frontend/.env.local`):**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

If not set, it defaults to `http://localhost:8000`, which should be correct.

**Restart frontend after changing this.**

### Step 5: Check Browser Console

Open browser DevTools (F12) → Console tab, and look for errors when loading the tasks page:

- `Failed to fetch` → Backend not running or CORS issue
- `401 Unauthorized` → JWT secret mismatch or token generation failed
- Network errors → Check if backend URL is correct

### Step 6: Check Server Logs

**Frontend logs** (terminal where `npm run dev` is running):
- Look for errors about token generation
- Check if `/api/auth/token` is being called

**Backend logs** (terminal where `uvicorn` is running):
- Look for JWT validation errors
- Check for CORS errors
- Verify requests are reaching the backend

### Step 7: Test the Token Endpoint

Test if the JWT token generation works:

```bash
# In browser console or using curl
# First, make sure you're logged in, then:
curl http://localhost:3001/api/auth/token \
  -H "Cookie: better-auth.session_token=YOUR_SESSION_COOKIE"

# Should return: {"token":"eyJ..."}
```

### Step 8: Test Backend API Directly

Test if the backend accepts JWT tokens:

```bash
# Get a token first (from browser or token endpoint)
TOKEN="your-jwt-token-here"

# Test backend
curl http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer $TOKEN"

# Should return: {"tasks":[],"total":0,"completed":0}
```

## Quick Checklist

- [ ] Backend is running on port 8000 (`curl http://localhost:8000/health`)
- [ ] `BETTER_AUTH_SECRET` matches in frontend `.env.local` and backend `.env`
- [ ] `CORS_ORIGINS` in backend includes your frontend port (3001)
- [ ] `NEXT_PUBLIC_API_URL` is set to `http://localhost:8000` in frontend
- [ ] Restarted both frontend and backend after changing env vars
- [ ] Checked browser console for errors
- [ ] Checked backend logs for JWT validation errors

## Common Error Messages

### "Cannot connect to server. Is the backend running on port 8000?"
**Fix**: Start the backend server

### "Could not validate credentials" (401)
**Fix**: `BETTER_AUTH_SECRET` mismatch between frontend and backend

### CORS errors in browser console
**Fix**: Add your frontend port to `CORS_ORIGINS` in backend config

### "Failed to get token" (500)
**Fix**: Check frontend logs - likely `BETTER_AUTH_SECRET` not set in `.env.local`

## Still Having Issues?

1. **Clear browser cookies** for localhost and try logging in again
2. **Check all environment variables** are loaded correctly:
   ```bash
   # Frontend
   cd frontend
   node -e "require('dotenv').config({path:'.env.local'}); console.log(process.env.BETTER_AUTH_SECRET)"
   
   # Backend (while it's running, check the actual value)
   ```
3. **Verify database connection** - Backend needs database to store tasks
4. **Check network tab** in browser DevTools to see the exact API request/response

## Debug Mode

Add logging to see what's happening:

**In browser console:**
```javascript
// Test token generation
fetch('/api/auth/token', {credentials: 'include'})
  .then(r => r.json())
  .then(console.log)

// Test backend API with token
fetch('http://localhost:8000/api/tasks/', {
  headers: {
    'Authorization': 'Bearer YOUR_TOKEN_HERE'
  }
})
  .then(r => r.json())
  .then(console.log)
```

Replace `YOUR_TOKEN_HERE` with the token from the first call.

