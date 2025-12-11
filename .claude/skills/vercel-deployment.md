# Skill: Vercel Deployment

## Overview

This skill captures patterns for deploying Next.js frontend to Vercel, including environment variables, OAuth configuration, and troubleshooting.

## Core Concepts

### Vercel Project Structure

```
Vercel Project
├── Production (main branch)
│   └── https://your-app.vercel.app
├── Preview (feature branches)
│   └── https://your-app-branch.vercel.app
└── Development (local)
    └── http://localhost:3000
```

### Automatic Deployments

```
Git Push → Vercel Build → Deploy
   │
   ├── main branch → Production
   └── other branches → Preview
```

## Configuration

### vercel.json

**File**: `frontend/vercel.json`
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "regions": ["iad1"],
  "functions": {
    "app/api/**/*.ts": {
      "maxDuration": 30
    }
  }
}
```

### next.config.js

**File**: `frontend/next.config.js`
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // For Vercel serverless
  output: 'standalone',
  
  // Disable image optimization if not needed
  images: {
    unoptimized: false,
  },
  
  // Environment variables (build-time)
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL,
  },
};

module.exports = nextConfig;
```

## Environment Variables

### Required Variables

| Variable | Scope | Description |
|----------|-------|-------------|
| `DATABASE_URL` | Server | Neon PostgreSQL connection |
| `BETTER_AUTH_SECRET` | Server | JWT signing secret |
| `BETTER_AUTH_URL` | Server | Full production URL |
| `NEXT_PUBLIC_BETTER_AUTH_URL` | Client | Public auth URL |
| `NEXT_PUBLIC_API_URL` | Client | Backend API URL |
| `GOOGLE_CLIENT_ID` | Server | OAuth client ID |
| `GOOGLE_CLIENT_SECRET` | Server | OAuth client secret |

### Setting Variables

```bash
# Via Vercel CLI
vercel env add DATABASE_URL production
vercel env add BETTER_AUTH_SECRET production
vercel env add GOOGLE_CLIENT_ID production

# List variables
vercel env ls
```

### Preview Environment Handling

```typescript
// frontend/lib/auth/config/preview-url.ts
export function getBetterAuthUrl(): string {
  // Production
  if (process.env.BETTER_AUTH_URL) {
    return process.env.BETTER_AUTH_URL;
  }
  
  // Vercel Preview
  if (process.env.VERCEL_URL) {
    return `https://${process.env.VERCEL_URL}`;
  }
  
  // Development
  return 'http://localhost:3000';
}
```

## OAuth Configuration

### Vercel Domain Setup

1. **Get your Vercel domains**:
   - Production: `your-app.vercel.app`
   - Preview: `your-app-*.vercel.app`

2. **Google Cloud Console**:
   - Add authorized redirect URIs:
     ```
     https://your-app.vercel.app/api/auth/callback/google
     https://your-app-git-*.vercel.app/api/auth/callback/google
     ```

3. **Better Auth Config**:
   ```typescript
   export const auth = betterAuth({
     baseURL: getBetterAuthUrl(),
     trustedOrigins: [
       getBetterAuthUrl(),
       "https://*.vercel.app",  // All preview deployments
     ],
   });
   ```

## Common Issues & Solutions

### Issue: "Invalid origin" from Better Auth

**Symptoms**:
- 403 error on `/api/auth/sign-in/social` or `/api/auth/sign-in/email`
- Vercel logs show: `ERROR [Better Auth]: Invalid origin: https://...`

**Root Cause**: Better Auth does NOT support wildcard patterns in `trustedOrigins`.

**Solution**:
```typescript
// ❌ WRONG - wildcards don't work
trustedOrigins: [
  "https://*.vercel.app",
]

// ✅ CORRECT - list each origin explicitly
trustedOrigins: [
  process.env.BETTER_AUTH_URL!,
  "https://your-app.vercel.app",
  "https://your-app-v1.vercel.app",
]
```

### Issue: OAuth Redirect Loop / redirect_uri_mismatch

**Symptoms**:
- Google shows "Access blocked: This app's request is invalid"
- Error 400: redirect_uri_mismatch

**Solution**:
1. Check Google Cloud Console → Credentials → OAuth 2.0 Client
2. Add **exact** redirect URI (no wildcards):
   ```
   https://your-app.vercel.app/api/auth/callback/google
   ```
3. Wait 2-5 minutes for propagation
4. Clear browser cache or test in incognito

### Issue: 500 Error on API Routes

**Symptoms**:
- API routes return 500 in production
- Works locally

**Debugging**:
```bash
# Check function logs
vercel logs --follow

# Check build output
vercel build --debug
```

**Common Causes**:
- Missing environment variables
- Node.js API used in serverless
- Database connection issues

### Issue: Environment Variables Not Available

**Symptoms**:
- `undefined` values in production
- Works in local development

**Solution**:
```bash
# Verify variables are set
vercel env ls

# Redeploy after adding variables
vercel --prod
```

### Issue: Build Fails

**Symptoms**:
- "Module not found" errors
- TypeScript errors

**Debugging**:
```bash
# Test build locally
npm run build

# Check Vercel build logs
vercel logs
```

## Deployment Commands

```bash
# Install Vercel CLI
npm i -g vercel

# Link project
vercel link

# Deploy preview
vercel

# Deploy production
vercel --prod

# View deployments
vercel ls

# Rollback
vercel rollback

# View logs
vercel logs --follow
```

## Pre-Deployment Checklist

```markdown
- [ ] `npm run build` passes locally
- [ ] All environment variables set in Vercel
- [ ] OAuth redirect URIs configured (exact match, no wildcards)
- [ ] BETTER_AUTH_URL matches THIS deployment's domain
- [ ] trustedOrigins includes THIS deployment's URL explicitly
- [ ] Backend CORS allows THIS deployment's URL
- [ ] DATABASE_URL accessible from Vercel region
- [ ] No Node.js filesystem APIs in API routes
- [ ] Images optimized or unoptimized flag set
```

## Multi-Version Deployment

To deploy multiple versions (e.g., v1 and v2) simultaneously:

### Option 1: Separate Vercel Projects (Recommended)

```bash
# Create new project for v1
rm -rf .vercel
git checkout iteration-1
cd frontend
vercel --yes  # Creates new project

# Add env vars in Vercel dashboard with correct URLs:
# BETTER_AUTH_URL = https://your-app-v1.vercel.app
# NEXT_PUBLIC_APP_URL = https://your-app-v1.vercel.app

# Deploy to production
vercel --prod --yes
```

### Required Updates for Each Deployment

1. **Frontend trustedOrigins**:
   ```typescript
   trustedOrigins: [
     env.BETTER_AUTH_URL,
     "https://your-app.vercel.app",      // main
     "https://your-app-v1.vercel.app",   // v1
   ]
   ```

2. **Backend CORS**:
   ```python
   origins.extend([
     "https://your-app.vercel.app",
     "https://your-app-v1.vercel.app",
   ])
   ```

3. **Google OAuth** (Cloud Console):
   ```
   https://your-app.vercel.app/api/auth/callback/google
   https://your-app-v1.vercel.app/api/auth/callback/google
   ```

### Why Separate Projects?

| Approach | Problem |
|----------|---------|
| Branch previews | URLs change each deploy, break OAuth |
| Vercel aliases | Must re-apply after each deploy |
| Same project, different branches | Only one production URL |
| **Separate projects** | ✅ Stable URLs, independent deploys |

See: ADR-007 Multi-Version Deployment Strategy

## Serverless Compatibility

### ❌ Avoid These Patterns

```typescript
// Node.js filesystem - breaks on serverless
import fs from 'fs';
const data = fs.readFileSync('file.txt');

// Long-running processes
while (true) { /* ... */ }

// WebSocket connections
const ws = new WebSocket('...');
```

### ✅ Use These Patterns

```typescript
// Fetch from API
const data = await fetch('/api/data').then(r => r.json());

// Short-lived requests
export async function GET() {
  const result = await db.query();
  return Response.json(result);
}
```

## Version Display

```typescript
// frontend/lib/version.ts
export const APP_VERSION = process.env.NEXT_PUBLIC_APP_VERSION || "0.0.0";

// Usage in component
import { APP_VERSION } from "@/lib/version";

<div className="text-xs text-muted-foreground">
  v{APP_VERSION}
</div>
```

## Troubleshooting Checklist

When deployment isn't working:

```markdown
1. [ ] Check Vercel logs: `vercel logs --follow`
2. [ ] Verify env vars: `vercel env ls`
3. [ ] Test in incognito (clear OAuth cache)
4. [ ] Check Better Auth trustedOrigins (no wildcards!)
5. [ ] Check backend CORS origins
6. [ ] Verify Google OAuth redirect URIs (exact match)
7. [ ] Wait 2-5 min after Google OAuth changes
8. [ ] Check Vercel deployment protection settings
```

---

**Part of**: Evolution of Todo Reusable Intelligence
**Phase**: II, III, IV, V
**Last Updated**: 2025-12-12
**Related**: ADR-007, PHR-004
