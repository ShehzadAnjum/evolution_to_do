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

### Issue: OAuth Redirect Loop

**Symptoms**: 
- Login redirects indefinitely
- Console shows "invalid redirect_uri"

**Solution**:
```typescript
// Ensure trustedOrigins includes Vercel domain
trustedOrigins: [
  process.env.BETTER_AUTH_URL!,
  "https://*.vercel.app",
]
```

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
- [ ] OAuth redirect URIs configured
- [ ] BETTER_AUTH_URL matches production domain
- [ ] DATABASE_URL accessible from Vercel region
- [ ] No Node.js filesystem APIs in API routes
- [ ] Images optimized or unoptimized flag set
```

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

---

**Part of**: Evolution of Todo Reusable Intelligence
**Phase**: II, III, IV, V
**Last Updated**: 2025-12-10
