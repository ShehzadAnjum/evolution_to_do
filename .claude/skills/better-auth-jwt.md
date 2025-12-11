# Skill: Better Auth + JWT Integration

## Overview

This skill captures patterns for integrating Better Auth with JWT verification across frontend (Next.js) and backend (FastAPI).

## Core Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Next.js       │────▶│   Better Auth   │────▶│   FastAPI       │
│   Frontend      │     │   (Auth Server) │     │   Backend       │
│                 │     │                 │     │                 │
│ - Login UI      │     │ - JWT issuing   │     │ - JWT verify    │
│ - Session       │     │ - OAuth         │     │ - User context  │
│ - API client    │     │ - Session mgmt  │     │ - Protected API │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Frontend Setup (Next.js)

### Auth Configuration

**File**: `frontend/lib/auth/config/auth.ts`
```typescript
import { betterAuth } from "better-auth";
import { nextCookies } from "better-auth/next-js";

export const auth = betterAuth({
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
  // ⚠️ IMPORTANT: Wildcards like "https://*.vercel.app" do NOT work!
  // You must list each origin explicitly
  trustedOrigins: [
    process.env.BETTER_AUTH_URL || "http://localhost:3000",
    "https://your-app.vercel.app",        // production
    "https://your-app-v1.vercel.app",     // secondary deployment
  ],
  database: {
    dialect: "postgresql",
    url: process.env.DATABASE_URL!,
    type: "neon",
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
  session: {
    cookieCache: {
      enabled: true,
      maxAge: 60 * 5, // 5 minutes
    },
  },
  plugins: [nextCookies()],
});
```

### Auth Client

**File**: `frontend/lib/auth/client.ts`
```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL,
});

export const { 
  signIn, 
  signUp, 
  signOut, 
  useSession 
} = authClient;
```

### Protected Route Pattern

**File**: `frontend/app/(protected)/layout.tsx`
```typescript
import { auth } from "@/lib/auth/config/auth";
import { headers } from "next/headers";
import { redirect } from "next/navigation";

export default async function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (!session) {
    redirect("/login");
  }

  return <>{children}</>;
}
```

## Backend Setup (FastAPI)

### JWT Verification

**File**: `backend/src/auth/jwt.py`
```python
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

security = HTTPBearer()

BETTER_AUTH_SECRET = os.environ.get("BETTER_AUTH_SECRET")

def verify_jwt(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Verify JWT token from Better Auth."""
    token = credentials.credentials
    
    try:
        payload = jwt.decode(
            token,
            BETTER_AUTH_SECRET,
            algorithms=["HS256"],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

def get_current_user_id(payload: dict = Depends(verify_jwt)) -> str:
    """Extract user ID from verified JWT."""
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User ID not found in token",
        )
    return user_id
```

### Protected Endpoint Pattern

**File**: `backend/src/api/routes/tasks.py`
```python
from fastapi import APIRouter, Depends
from ...auth.jwt import get_current_user_id

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.get("/")
async def list_tasks(
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """List tasks for current user."""
    return get_tasks(session, user_id)

@router.post("/")
async def create_task(
    task: TaskCreate,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Create task for current user."""
    return create_task_db(session, task, user_id)
```

## Frontend API Client

**File**: `frontend/lib/api/client.ts`
```typescript
import { authClient } from "@/lib/auth/client";

const API_URL = process.env.NEXT_PUBLIC_API_URL;

async function fetchWithAuth(endpoint: string, options: RequestInit = {}) {
  const session = await authClient.getSession();
  
  if (!session?.session?.token) {
    throw new Error("Not authenticated");
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers: {
      ...options.headers,
      "Authorization": `Bearer ${session.session.token}`,
      "Content-Type": "application/json",
    },
  });

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }

  return response.json();
}

export const api = {
  tasks: {
    list: () => fetchWithAuth("/api/tasks"),
    create: (task: { title: string }) => 
      fetchWithAuth("/api/tasks", {
        method: "POST",
        body: JSON.stringify(task),
      }),
    update: (id: string, task: { title?: string; completed?: boolean }) =>
      fetchWithAuth(`/api/tasks/${id}`, {
        method: "PATCH",
        body: JSON.stringify(task),
      }),
    delete: (id: string) =>
      fetchWithAuth(`/api/tasks/${id}`, {
        method: "DELETE",
      }),
  },
};
```

## OAuth Setup (Google)

### Environment Variables

```bash
# Frontend (.env.local)
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxx
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-secret-key

# Backend (.env)
BETTER_AUTH_SECRET=your-secret-key  # Must match frontend!
```

### Vercel Deployment

```bash
# Vercel Environment Variables
BETTER_AUTH_URL=https://your-app.vercel.app
NEXT_PUBLIC_BETTER_AUTH_URL=https://your-app.vercel.app
GOOGLE_CLIENT_ID=xxx
GOOGLE_CLIENT_SECRET=xxx
```

### Google Cloud Console

1. Create OAuth 2.0 credentials
2. Add authorized redirect URIs:
   - `http://localhost:3000/api/auth/callback/google`
   - `https://your-app.vercel.app/api/auth/callback/google`

## Troubleshooting

| Issue | Solution |
|-------|----------|
| 401 on API calls | Check BETTER_AUTH_SECRET matches |
| OAuth redirect loop | Verify trustedOrigins includes domain |
| Session not persisting | Check cookie settings |
| Token expired | Implement token refresh |
| **Post-login redirect loop on Vercel** | **Check BOTH cookie names in middleware (see below)** |
| **"Invalid origin" 403 error** | **Add origin explicitly to trustedOrigins (no wildcards!)** |
| **redirect_uri_mismatch from Google** | **Add exact URI to Google Console, clear browser cache** |

### CRITICAL: trustedOrigins Does NOT Support Wildcards

```typescript
// ❌ WRONG - This will NOT work
trustedOrigins: ["https://*.vercel.app"]

// ✅ CORRECT - List each domain explicitly
trustedOrigins: [
  env.BETTER_AUTH_URL,
  "https://your-app.vercel.app",
  "https://your-app-v1.vercel.app",
]
```

**Error you'll see if using wildcards:**
```
ERROR [Better Auth]: Invalid origin: https://your-app.vercel.app
```

### CRITICAL: Secure Cookie Names in Production

**This fix saved 8+ hours of debugging.**

When `useSecureCookies: true` (automatic in production/HTTPS), Better Auth prefixes cookies with `__Secure-`:

| Environment | Cookie Name |
|-------------|-------------|
| Development (HTTP) | `better-auth.session_token` |
| Production (HTTPS) | `__Secure-better-auth.session_token` |

**Middleware MUST check both:**

```typescript
// frontend/lib/auth/http/middleware.ts
export function hasSessionCookie(request: NextRequest): boolean {
  // Check BOTH cookie names!
  const devCookie = request.cookies.get("better-auth.session_token");
  const secureCookie = request.cookies.get("__Secure-better-auth.session_token");
  return !!(devCookie || secureCookie);
}
```

**Why this matters:**
1. User logs in on Vercel (HTTPS)
2. Better Auth sets `__Secure-better-auth.session_token`
3. Middleware checks only `better-auth.session_token` → not found!
4. Middleware thinks user isn't authenticated → redirects to login
5. **Infinite redirect loop**

See: `history/prompts/001-ai-chatbot-mcp/0004-better-auth-secure-cookies-fix.fix.prompt.md`

## Anti-Patterns

### ❌ Hardcoded Secrets

```typescript
const secret = "my-hardcoded-secret";
```

### ✅ Environment Variables

```typescript
const secret = process.env.BETTER_AUTH_SECRET!;
```

### ❌ Missing User Isolation

```python
# Gets ALL tasks - security vulnerability!
return session.exec(select(Task)).all()
```

### ✅ Always Filter by User

```python
return session.exec(
    select(Task).where(Task.user_id == user_id)
).all()
```

---

**Part of**: Evolution of Todo Reusable Intelligence
**Phase**: II, III, IV, V
**Last Updated**: 2025-12-12
**Related**: ADR-007, PHR-004
