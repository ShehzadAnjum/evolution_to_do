# PHR-004: Vercel Multi-Deployment Troubleshooting

## Date
2025-12-12

## Context
Deploying iteration-1 (v1.0.0) frontend alongside main (v2.0.0) on Vercel.

## Problem Statement
Need to deploy two versions of the frontend with stable URLs for demo/comparison purposes.

## Approaches Tried

### Attempt 1: Branch Preview Deployment
**Action**: Push `iteration-1` branch, expect Vercel auto-deploy
**Result**: No automatic deployment - preview deployments weren't triggering
**Learning**: Vercel preview deployments depend on project settings and may not trigger for all branches

### Attempt 2: Vercel CLI Deploy + Alias
**Action**:
```bash
git checkout iteration-1
cd frontend
vercel --yes
vercel alias <deployment-url> iteration1-evolution-todo.vercel.app
```
**Result**: Deployment worked but was using wrong Vercel project (no env vars)
**Learning**: CLI deployments create `.vercel/` config that links to a specific project

### Attempt 3: Link to Existing Project
**Action**:
```bash
vercel link --project evolution-to-do
vercel --yes
```
**Result**: "Invalid origin" errors from Better Auth
**Learning**: Even same project, `BETTER_AUTH_URL` env var was set to production URL, not the preview alias

### Attempt 4: Vercel Deployment Protection
**Action**: Check if deployment protection was blocking
**Result**: Deployment protection was enabled, requiring Vercel auth for previews
**Learning**: Disable deployment protection for preview URLs or use bypass tokens

### Attempt 5: Separate Vercel Project (SUCCESS)
**Action**:
```bash
rm -rf .vercel
cd frontend
vercel --yes --name evolution-todo-v1
# Then add env vars in Vercel dashboard with correct URLs
vercel --prod --yes
```
**Result**: Working deployment at https://evolution-todo-v1.vercel.app

## Root Causes Identified

### 1. Better Auth trustedOrigins
Better Auth validates request origin against `trustedOrigins` array. **Wildcard patterns like `https://*.vercel.app` do NOT work** - each origin must be explicitly listed.

### 2. BETTER_AUTH_URL Environment Variable
The `BETTER_AUTH_URL` must match the deployment URL, not a different deployment. This affects:
- OAuth redirect URIs
- Cookie domain
- Session validation

### 3. Google OAuth Redirect URI
Google OAuth requires **exact match** of redirect URIs. Each deployment URL needs its own entry:
```
https://evolution-to-do.vercel.app/api/auth/callback/google
https://evolution-todo-v1.vercel.app/api/auth/callback/google
```

### 4. Backend CORS
Backend must allow requests from all frontend deployment URLs in CORS origins.

### 5. Browser Cache
Google OAuth state can be cached. After changing OAuth config, clear browser cache or use incognito.

## Solution Checklist

For deploying a new version to a separate Vercel project:

```markdown
### Vercel Project Setup
- [ ] Create new Vercel project: `vercel --name <project-name>`
- [ ] Add environment variables in Vercel dashboard:
  - [ ] DATABASE_URL (same as production)
  - [ ] BETTER_AUTH_SECRET (same as production)
  - [ ] BETTER_AUTH_URL = https://<new-project>.vercel.app
  - [ ] NEXT_PUBLIC_APP_URL = https://<new-project>.vercel.app
  - [ ] NEXT_PUBLIC_API_URL (same as production)
  - [ ] GOOGLE_CLIENT_ID (same as production)
  - [ ] GOOGLE_CLIENT_SECRET (same as production)

### Code Updates
- [ ] Add new URL to trustedOrigins in frontend auth config
- [ ] Add new URL to CORS origins in backend

### Google Cloud Console
- [ ] Add authorized JavaScript origin: https://<new-project>.vercel.app
- [ ] Add redirect URI: https://<new-project>.vercel.app/api/auth/callback/google
- [ ] Wait 2-5 minutes for propagation

### Deploy
- [ ] Deploy to production: `vercel --prod --yes`
- [ ] Test in incognito window (avoid OAuth cache issues)
```

## Key Learnings

1. **Vercel CLI creates project-specific `.vercel/` config** - Remove it to link to different project
2. **Better Auth wildcards don't work** - List all origins explicitly
3. **Each Vercel project needs its own env vars** - Even if values are mostly the same
4. **Google OAuth is strict** - Exact URI match required, propagation can take minutes
5. **Clear browser cache after OAuth changes** - Cached state causes confusing errors
6. **Vercel deployment protection blocks programmatic access** - Disable for preview URLs or use bypass tokens

## Error Messages Reference

| Error | Cause | Fix |
|-------|-------|-----|
| `Invalid origin: https://...` | Origin not in trustedOrigins | Add URL to trustedOrigins array |
| `redirect_uri_mismatch` | OAuth redirect URI not registered | Add exact URI to Google Console |
| `Access blocked: This app's request is invalid` | OAuth misconfiguration | Check redirect URI + clear cache |
| `Cannot connect to backend server` | CORS blocking or wrong API URL | Add origin to backend CORS |
| `Authentication Required` (Vercel page) | Deployment protection enabled | Disable in project settings |

## Related
- ADR-007: Multi-Version Deployment Strategy
- `.claude/skills/vercel-deployment.md`
- `.claude/skills/better-auth-jwt.md`
