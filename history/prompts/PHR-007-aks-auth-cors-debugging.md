# PHR-007: AKS Authentication and CORS Debugging

**Date**: 2025-12-14
**Phase**: V (Cloud Deployment)
**Duration**: ~2 hours
**Severity**: Critical (app non-functional)

---

## Context

After deploying Evolution Todo to Azure AKS with GitHub Actions CI/CD, users could log in successfully but immediately saw "Please log in to view your tasks" error. The app was completely non-functional despite login working.

## Initial Symptoms

1. Login works (both password and Google OAuth)
2. After redirect to /tasks, error: "Please log in to view your tasks. Retry"
3. User profile shows in header (logged in state)
4. No backend API calls visible in HAR file

## Root Causes Identified

### Issue 1: Secure Cookies over HTTP

**Problem**: Better Auth's `useSecureCookies` was set based on `NODE_ENV`:
```typescript
// WRONG - AKS uses HTTP but NODE_ENV=production
useSecureCookies: process.env.NODE_ENV === "production"
```

**Effect**:
1. AKS deployment runs in production mode
2. Cookies marked as `Secure`
3. Browser refuses to send Secure cookies over HTTP
4. `/api/auth/token` receives no session cookie
5. Returns 401 → frontend shows "Please log in"

**Fix**:
```typescript
// CORRECT - Base on actual URL scheme
useSecureCookies: (env.BETTER_AUTH_URL ?? "http://localhost:3000").startsWith("https://")
```

**File**: `frontend/lib/auth/core/server.ts:46`

### Issue 2: Pods Not Pulling New Images

**Problem**: `helm upgrade` doesn't restart pods if deployment spec unchanged. With `latest` tag and same spec, K8s assumes nothing changed.

**Effect**: Fix deployed to GHCR but pods still running old image.

**Fix**: Added `kubectl rollout restart` to CD workflow:
```yaml
- name: Force pod restart to pull latest images
  run: |
    kubectl rollout restart deployment/frontend
    kubectl rollout restart deployment/backend
```

**File**: `.github/workflows/cd.yml:83-88`

### Issue 3: Backend CORS Blocking

**Problem**: After auth fix, new error: "Cannot connect to backend server"

**Root Cause**: Browser blocking cross-origin requests from `http://172.171.119.133.nip.io:3000` to `http://48.200.16.149:8000` because nip.io URL not in allowed origins.

**Fix**: Added to CORS origins:
```python
origins.extend([
    ...
    "http://172.171.119.133.nip.io:3000",  # AKS deployment via nip.io
])
```

**File**: `backend/src/api/main.py:62`

## Debugging Approach

1. **HAR file analysis** - Showed NO backend API calls at all, indicating frontend was failing before trying backend
2. **Code tracing** - Followed flow from `loadTasks()` → `getAuthToken()` → `/api/auth/token`
3. **Identified early return** - If no token, sets error and returns without calling backend
4. **Root cause** - Session cookie not being sent due to Secure flag mismatch

## Key Learnings

### 1. Never Base Cookie Security on NODE_ENV Alone

```typescript
// ❌ WRONG
useSecureCookies: process.env.NODE_ENV === "production"

// ✅ CORRECT
useSecureCookies: BETTER_AUTH_URL.startsWith("https://")
```

### 2. Force Pod Restarts When Using `latest` Tag

```yaml
# After helm upgrade
kubectl rollout restart deployment/frontend
kubectl rollout restart deployment/backend
```

### 3. Always Include Deployment URLs in CORS

When deploying to a new environment, remember to add the frontend URL to backend CORS allowed origins.

### 4. HAR Files Are Gold for Debugging

If HAR shows NO requests to a service, the issue is on the client side before the request is even attempted.

## Files Changed

| File | Change |
|------|--------|
| `frontend/lib/auth/core/server.ts` | useSecureCookies based on URL scheme |
| `.github/workflows/cd.yml` | Added rollout restart step |
| `backend/src/api/main.py` | Added nip.io to CORS origins |
| `.claude/skills/better-auth-jwt.md` | Documented lesson learned |

## Time Investment

| Task | Time |
|------|------|
| Initial diagnosis | 30 min |
| Secure cookie fix | 20 min |
| CD restart fix | 15 min |
| CORS fix | 10 min |
| Documentation | 30 min |
| **Total** | ~2 hours |

## Prevention

1. **Checklist item**: When deploying to HTTP environment, verify cookie security settings
2. **CD best practice**: Always include rollout restart for `latest` tag deployments
3. **CORS checklist**: Add new deployment URLs to backend CORS before deploying

## Related Resources

- PHR-004: Better Auth secure cookies fix (Vercel)
- Skill: `.claude/skills/better-auth-jwt.md`
- Skill: `.claude/skills/azure-aks-deployment.md`

---

**Tags**: #aks #better-auth #cors #cookies #debugging #k8s
