---
id: "0004"
title: "Better Auth Secure Cookies Production Fix"
stage: fix
date: 2025-12-10
surface: claude-code
model: claude-opus-4-5-20251101
feature: 001-ai-chatbot-mcp
branch: main
user: anjum
command: manual-debug
labels: [better-auth, cookies, vercel, production, critical-fix, auth-security]
links:
  spec: specs/001-ai-chatbot-mcp/spec.md
  ticket:
  adr:
  pr:
files:
  - path: frontend/lib/auth/http/middleware.ts
    action: modified
  - path: frontend/lib/auth/config/routes.ts
    action: modified
  - path: frontend/lib/auth/ui/pages/LoginPage.tsx
    action: modified
tests:
  - Manual verification on Vercel production
---

## Problem Statement

**Symptoms**:
1. Protected routes (`/chat`, `/tasks`) were accessible without login on Vercel
2. After successful login, users were redirected back to login page instead of target route
3. Google OAuth was broken (same redirect loop issue)

**Time Previously Wasted**: ~8 hours debugging similar issues with Google OAuth

## Root Cause Analysis

### Issue 1: Protected Routes Not Protected

**File**: `frontend/lib/auth/config/routes.ts`

The `protectedRoutes` array was missing `/chat` and `/tasks`:

```typescript
// BEFORE (broken)
export const protectedRoutes = [
  "/dashboard",
  "/app",
  "/account",
] as const;

// AFTER (fixed)
export const protectedRoutes = [
  "/dashboard",
  "/app",
  "/account",
  "/tasks",
  "/chat",
] as const;
```

**Why it mattered**: The middleware matcher ran, but `isProtectedRoute()` returned false because these routes weren't in the array.

### Issue 2: Post-Login Redirect Not Working

**File**: `frontend/lib/auth/ui/pages/LoginPage.tsx`

The page was hardcoding `/tasks` instead of reading the `redirect` query param:

```typescript
// BEFORE (broken)
router.push("/tasks");

// AFTER (fixed)
const searchParams = useSearchParams();
const redirectTo = searchParams.get("redirect") || "/tasks";
router.push(redirectTo);
```

### Issue 3: Secure Cookie Name in Production (THE CRITICAL ONE)

**File**: `frontend/lib/auth/http/middleware.ts`

**THIS IS THE 8-HOUR FIX**: Better Auth uses different cookie names based on environment:

| Environment | Cookie Name |
|-------------|-------------|
| Development (HTTP) | `better-auth.session_token` |
| Production (HTTPS) | `__Secure-better-auth.session_token` |

When `useSecureCookies: true` is set (which happens automatically in production), Better Auth prefixes cookies with `__Secure-`.

```typescript
// BEFORE (broken - only checked dev cookie)
export function hasSessionCookie(request: NextRequest): boolean {
  const sessionCookie = request.cookies.get("better-auth.session_token");
  return !!sessionCookie;
}

// AFTER (fixed - checks both cookie names)
export function hasSessionCookie(request: NextRequest): boolean {
  const devCookie = request.cookies.get("better-auth.session_token");
  const secureCookie = request.cookies.get("__Secure-better-auth.session_token");
  return !!(devCookie || secureCookie);
}
```

## The Golden Rule

> **When using Better Auth with `useSecureCookies: true` in production, ALWAYS check for BOTH cookie names in middleware:**
> - `better-auth.session_token` (development/HTTP)
> - `__Secure-better-auth.session_token` (production/HTTPS)

## Why This Fixes Google OAuth Too

Google OAuth was experiencing the same redirect loop because:
1. User completes Google OAuth flow
2. Better Auth sets `__Secure-better-auth.session_token` cookie
3. Middleware checks for `better-auth.session_token` (wrong name!)
4. Middleware thinks user isn't authenticated → redirects to login
5. Infinite loop

By fixing the cookie check, ALL auth methods now work:
- Email/password login
- Google OAuth
- Any future OAuth providers

## Commits

1. `d68a62e` - `fix(auth): add /chat and /tasks to protectedRoutes config`
2. `f065b37` - `fix(auth): use redirect param for post-login navigation`
3. `f0aa329` - `fix(auth): check both secure and non-secure cookie names in middleware`

## Prevention Checklist

When implementing Better Auth middleware:

- [ ] Check for BOTH `better-auth.session_token` AND `__Secure-better-auth.session_token`
- [ ] Add ALL protected routes to `protectedRoutes` array
- [ ] Read `redirect` query param in login page
- [ ] Test on actual Vercel deployment (not just localhost)
- [ ] Verify with browser DevTools → Application → Cookies to see actual cookie names

## Outcome

- ✅ Impact: All auth flows now work correctly on Vercel production
- ✅ Email/password login works
- ✅ Google OAuth works (previously broken for 8+ hours)
- ✅ Protected routes properly protected
- ✅ Post-login redirect works correctly
- 🧠 Reflection: The `__Secure-` prefix is a browser security feature for HTTPS-only cookies. Better Auth implements this automatically but documentation doesn't emphasize the middleware implications.

## Evaluation notes (flywheel)

- Failure modes observed: Secure cookie prefix not documented prominently in Better Auth
- Graders run and results: Manual verification on Vercel PASS
- Prompt variant: Manual debugging session
- Next experiment: Add automated E2E test for auth flow on preview deployments

---

**CRITICAL MEMORY**: This fix took 8+ hours previously. The secure cookie prefix (`__Secure-`) is the key insight. Always check both cookie names in middleware.
