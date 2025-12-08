# Better Auth Reference Guide

**Date Created**: 2025-12-08
**Purpose**: Comprehensive reference for Better Auth implementation, especially for Vercel deployments
**Sources**: Grok analysis + Better Auth vs NextAuth comparison

---

## Table of Contents

1. [What is Better Auth](#what-is-better-auth)
2. [Critical Vercel Deployment Issues](#critical-vercel-deployment-issues)
3. [Correct Configuration](#correct-configuration)
4. [OAuth Flow (The Right Way)](#oauth-flow-the-right-way)
5. [Environment Variables](#environment-variables)
6. [Google OAuth Setup](#google-oauth-setup)
7. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
8. [Troubleshooting Checklist](#troubleshooting-checklist)

---

## What is Better Auth

### Core Philosophy

Better Auth is a **batteries-included** authentication framework for TypeScript that prioritizes:

- **Production-ready by default**: Enterprise-grade security, not a toy
- **Self-hosted**: Your database, your infrastructure, no vendor lock-in
- **Framework-agnostic**: Works with Next.js, React, Vue, Svelte, Astro, etc.
- **TypeScript-first**: Strong type inference across server and client
- **Plugin architecture**: Enable features like 2FA, organizations, SSO via plugins

### Built-in Features (vs Auth.js/NextAuth)

| Feature | Better Auth | Auth.js/NextAuth |
|---------|-------------|------------------|
| Rate Limiting | ✅ Built-in | ❌ Manual |
| Database Migrations | ✅ Automatic | ❌ Manual |
| Organizations/Multi-tenant | ✅ Plugin | ❌ Custom code |
| 2FA/MFA | ✅ Built-in | ❌ Custom code |
| Passkeys | ✅ Built-in | ⚠️ WebAuthn only |
| Setup Complexity | ✅ Simple | ⚠️ More config |

### When to Choose Better Auth

✅ **Use Better Auth when:**
- Starting a new TypeScript project
- Need fast setup with strong defaults
- Require organizations, 2FA, rate limiting
- Want self-hosted auth without external SaaS
- Building SaaS with multi-tenant needs

❌ **Consider Auth.js when:**
- Maintaining existing NextAuth codebase
- Need very specific custom callback logic
- Prefer standard Web API core

---

## Critical Vercel Deployment Issues

### Issue #1: Invalid Origin Errors

**Symptom**: OAuth fails on Vercel preview deployments
**Cause**: Preview URLs are dynamic (e.g., `branch-abc-123.vercel.app`), breaking static origin checks

**Fix**:
```typescript
advanced: {
  trustedOrigins: [
    process.env.BETTER_AUTH_URL || "http://localhost:3000",
    "https://*.vercel.app", // Wildcard for previews
  ],
}
```

### Issue #2: Cookies Not Saving/Persisting

**Symptom**: Session cookies fail to set after sign-in; auth breaks on refresh
**Cause**: Incorrect `sameSite`, `secure`, or `domain` attributes for production HTTPS

**Fix**:
```typescript
advanced: {
  cookies: {
    session_token: {
      sameSite: "none",  // CRITICAL for cross-site OAuth
      secure: true,      // REQUIRED for HTTPS
      httpOnly: true,    // Security
      domain: process.env.NODE_ENV === "production" ? ".vercel.app" : undefined,
    },
  },
}
```

**Why `sameSite: "none"` is Required:**
- OAuth redirects from `google.com` → `yourapp.vercel.app` are cross-site
- Modern browsers block `sameSite: "lax"` cookies in this scenario
- `sameSite: "none"` MUST be paired with `secure: true` (HTTPS only)

### Issue #3: OAuth State Mismatch

**Symptom**: Callback validation fails despite correct config
**Cause**: Vercel preview subdomains shift state param context

**Fix**:
```typescript
import { oAuthProxy } from "better-auth/plugins";

plugins: [
  oAuthProxy({
    oauthConfig: { skipStateCookieCheck: true },
  }),
]
```

### Issue #4: The `/api/auth/social/google` 404 Error

**⚠️ CRITICAL MISTAKE**: This path does NOT exist in Better Auth!

**Wrong Approach** (causes 404):
```typescript
// ❌ Never do this:
<a href="/api/auth/social/google">Sign in with Google</a>
```

**Correct Approach**:
```typescript
// ✅ Use the client SDK:
import { authClient } from "@/lib/auth/client";

await authClient.signIn.social({
  provider: "google",
  callbackURL: "/",
});
```

**What Actually Happens:**
1. Client calls `signIn.social()` → **POST** to `/api/auth/sign-in/social` (body: `{ provider: "google" }`)
2. Server responds with **302 redirect** to Google OAuth URL
3. Google redirects back via **GET** to `/api/auth/callback/google`
4. Server sets cookies and redirects to your app

**There is NO `/api/auth/social/google` endpoint!**

### Issue #5: Bot Protection Blocks

**Symptom**: Intermittent 429 errors, especially on Safari
**Cause**: Vercel Bot Management flags "better-auth" user-agent

**Fix**: Vercel Dashboard → Firewall → Bot Management → Set to "Log" mode

---

## Correct Configuration

### Server Configuration (`lib/auth/core/server.ts`)

```typescript
import { betterAuth } from "better-auth";
import { nextCookies } from "better-auth/next-js";
import { db } from "../adapters/db-adapter";

export const auth = betterAuth({
  // Database connection
  database: db, // Neon Pool or Prisma adapter

  // Base path (must match API route)
  basePath: "/api/auth",

  // Environment variables
  secret: process.env.BETTER_AUTH_SECRET!,
  baseURL: process.env.BETTER_AUTH_URL!,

  // Email/password authentication
  emailAndPassword: {
    enabled: true,
  },

  // Social providers (Google OAuth)
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
      redirectURI: `${process.env.BETTER_AUTH_URL}/api/auth/callback/google`,
    },
  },

  // CRITICAL: Production cookie configuration for Vercel
  advanced: {
    // Enable secure cookies in production
    useSecureCookies: process.env.NODE_ENV === "production",

    // Explicit cookie attributes for OAuth
    cookies: {
      session_token: {
        sameSite: process.env.NODE_ENV === "production" ? "none" : "lax",
        secure: process.env.NODE_ENV === "production",
        httpOnly: true,
        domain: process.env.NODE_ENV === "production" ? ".vercel.app" : undefined,
      },
    },

    // Trusted origins for cross-origin requests
    trustedOrigins: [
      process.env.BETTER_AUTH_URL || "http://localhost:3000",
      "https://*.vercel.app", // Wildcard for Vercel previews
    ],
  },

  // Plugins
  plugins: [
    nextCookies(), // Next.js cookie handling
  ],
});

export type Auth = typeof auth;
```

### API Route Handler (`app/api/auth/[...route]/route.ts`)

```typescript
import { auth } from "@/lib/auth/core/server";
import { toNextJsHandler } from "better-auth/next-js";

export const dynamic = "force-dynamic";

// Create handlers using the shared auth instance
// CRITICAL: Use single shared instance, not dynamic per-request
const handler = toNextJsHandler(auth);

export const { GET, POST } = handler;
```

**⚠️ Common Mistake**: Creating dynamic auth instances per request breaks OAuth session continuity!

### Client Configuration (`lib/auth/client.ts`)

```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
  // basePath defaults to "/api/auth" - don't override unless needed
});
```

---

## OAuth Flow (The Right Way)

### Step-by-Step Flow

```
1. User clicks "Sign in with Google"
   ↓
2. Frontend: authClient.signIn.social({ provider: "google" })
   ↓
3. POST /api/auth/sign-in/social (body: { provider: "google" })
   ↓
4. Server: 302 redirect to accounts.google.com/o/oauth2/...
   ↓
5. User authenticates on Google
   ↓
6. Google: 302 redirect to /api/auth/callback/google?code=...&state=...
   ↓
7. Server validates code, creates session, sets cookies
   ↓
8. Server: 302 redirect to your app (e.g., /dashboard)
   ↓
9. User is authenticated with session cookie
```

### Frontend Implementation

```typescript
// In your login component
"use client";

import { authClient } from "@/lib/auth/client";
import { useState } from "react";

export default function LoginPage() {
  const [loading, setLoading] = useState(false);

  const handleGoogleSignIn = async () => {
    setLoading(true);
    try {
      await authClient.signIn.social({
        provider: "google",
        callbackURL: "/dashboard", // Where to redirect after success
      });
    } catch (error) {
      console.error("Sign-in error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <button onClick={handleGoogleSignIn} disabled={loading}>
      {loading ? "Signing in..." : "Sign in with Google"}
    </button>
  );
}
```

---

## Environment Variables

### Required Environment Variables

| Variable | Example | Where Used | Notes |
|----------|---------|------------|-------|
| `BETTER_AUTH_SECRET` | `JU1I9zfPxGQAoOoeD+J/GWr0tyR3Zs4cO5kfQdmz/0E=` | Server | Generate: `openssl rand -base64 32` |
| `BETTER_AUTH_URL` | `https://yourapp.vercel.app` | Server | Exact production domain |
| `NEXT_PUBLIC_BETTER_AUTH_URL` | `https://yourapp.vercel.app` | Client | Must be public for browser |
| `DATABASE_URL` | `postgresql://user:pass@host/db?sslmode=require` | Server | Neon or other PostgreSQL |
| `GOOGLE_CLIENT_ID` | `123456789-abc.apps.googleusercontent.com` | Server | From Google Console |
| `GOOGLE_CLIENT_SECRET` | `GOCSPX-xyz123` | Server | Keep secret! |

### Vercel Dashboard Setup

1. Go to **Project Settings** → **Environment Variables**
2. Add each variable for **Production**, **Preview**, and **Development**
3. **Important**: Use exact production URL for `BETTER_AUTH_URL`, not wildcards
4. **Redeploy** after changes

---

## Google OAuth Setup

### Google Cloud Console Configuration

1. **Go to**: [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → Credentials

2. **Create OAuth 2.0 Client ID** (or edit existing):
   - Application type: **Web application**
   - Authorized JavaScript origins:
     - `https://yourapp.vercel.app`
     - `http://localhost:3000` (for development)

3. **Authorized redirect URIs** (CRITICAL):
   - Production: `https://yourapp.vercel.app/api/auth/callback/google`
   - Development: `http://localhost:3000/api/auth/callback/google`
   - **For Vercel Previews**: Add each preview URL manually
     - Example: `https://yourapp-git-branch-abc.vercel.app/api/auth/callback/google`
     - ⚠️ **Google does NOT support wildcards** in redirect URIs!

4. **Save and wait**: Changes can take 5-60 minutes to propagate

5. **Copy credentials**: Use Client ID and Client Secret in Vercel env vars

### Common Google OAuth Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `redirect_uri_mismatch` | Callback URL not in authorized list | Add exact URL to Google Console |
| `access_denied` | User canceled or insufficient scopes | User action, retry |
| `invalid_client` | Wrong Client ID or Secret | Check env vars match Google Console |

---

## Common Mistakes to Avoid

### ❌ Mistake #1: Creating Dynamic Auth Instances

```typescript
// ❌ WRONG: Creates new instance per request
async function GET(request: Request) {
  const auth = betterAuth({ ... }); // Different instance each time
  const handler = toNextJsHandler(auth);
  return handler.GET(request);
}
```

```typescript
// ✅ CORRECT: Single shared instance
const auth = betterAuth({ ... });
const handler = toNextJsHandler(auth);

export const { GET, POST } = handler;
```

**Why?** OAuth sign-in and callback must use the **same auth instance** for session continuity.

### ❌ Mistake #2: Using Direct Links for OAuth

```typescript
// ❌ WRONG: Direct link
<a href="/api/auth/social/google">Sign in with Google</a>
```

```typescript
// ✅ CORRECT: Use client SDK
<button onClick={() => authClient.signIn.social({ provider: "google" })}>
  Sign in with Google
</button>
```

### ❌ Mistake #3: Wrong Cookie Settings

```typescript
// ❌ WRONG: Default sameSite breaks OAuth in production
cookies: {
  session_token: {
    sameSite: "lax", // Fails on cross-site OAuth redirects
  },
}
```

```typescript
// ✅ CORRECT: sameSite "none" for production OAuth
cookies: {
  session_token: {
    sameSite: process.env.NODE_ENV === "production" ? "none" : "lax",
    secure: process.env.NODE_ENV === "production",
  },
}
```

### ❌ Mistake #4: Missing `NEXT_PUBLIC_` Prefix

```typescript
// ❌ WRONG: Client can't access this
baseURL: process.env.BETTER_AUTH_URL, // undefined in browser!
```

```typescript
// ✅ CORRECT: Use public env var for client
baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL,
```

### ❌ Mistake #5: Mismatched Environment Variables

```
# ❌ WRONG: Server and client URLs differ
BETTER_AUTH_URL=https://app1.vercel.app
NEXT_PUBLIC_BETTER_AUTH_URL=https://app2.vercel.app
```

```
# ✅ CORRECT: Must match exactly
BETTER_AUTH_URL=https://yourapp.vercel.app
NEXT_PUBLIC_BETTER_AUTH_URL=https://yourapp.vercel.app
```

---

## Troubleshooting Checklist

### OAuth Not Working on Vercel

- [ ] **Check cookies**: Browser DevTools → Application → Cookies → Look for `better-auth.session_token`
  - If missing: Cookie configuration issue
  - If present but auth fails: Session validation issue

- [ ] **Verify environment variables**:
  - [ ] `BETTER_AUTH_SECRET` is set (32+ characters)
  - [ ] `BETTER_AUTH_URL` matches exact Vercel domain
  - [ ] `NEXT_PUBLIC_BETTER_AUTH_URL` matches `BETTER_AUTH_URL`
  - [ ] `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET` are correct

- [ ] **Check Google Console**:
  - [ ] Redirect URI matches: `https://yourapp.vercel.app/api/auth/callback/google`
  - [ ] Wait 5-60 minutes after changes for propagation

- [ ] **Verify cookie configuration**:
  ```typescript
  // Must have these in production:
  sameSite: "none",
  secure: true,
  httpOnly: true,
  ```

- [ ] **Check Vercel logs**:
  - Dashboard → Deployments → Functions → Look for errors
  - Search for "OAuth callback" or "cookies"

- [ ] **Test the flow manually**:
  ```bash
  # Should return 302 to Google
  curl -X POST https://yourapp.vercel.app/api/auth/sign-in/social \
    -H "Content-Type: application/json" \
    -d '{"provider": "google"}' \
    -v
  ```

- [ ] **Verify auth instance is shared** (not created per request)

- [ ] **Check Vercel Bot Management**: Settings → Firewall → Set to "Log" mode

### Email/Password Works, OAuth Doesn't

**This is the classic symptom!**

Root causes:
1. ✅ Email/password doesn't cross sites → `sameSite: "lax"` works
2. ❌ OAuth crosses sites (google.com → yourapp.com) → Needs `sameSite: "none"`

**Fix**: Update cookie configuration to use `sameSite: "none"` in production.

### Build Succeeds, Runtime Fails

- [ ] **Check Better Auth version**: Should be `^1.3.24+`
  ```bash
  npm update better-auth
  ```

- [ ] **Clear Vercel cache**: Dashboard → Deployments → Redeploy → "Clear cache"

- [ ] **Check for ESM errors** in logs → Update to latest Better Auth

### 404 on `/api/auth/*` Endpoints

- [ ] **Verify route file location**: `app/api/auth/[...route]/route.ts`
- [ ] **Check `basePath` in config**: Should be `/api/auth`
- [ ] **Ensure `export const dynamic = "force-dynamic"`** is present

---

## Quick Reference Commands

### Generate Better Auth Secret
```bash
openssl rand -base64 32
```

### Test OAuth Endpoint Manually
```bash
curl -X POST https://yourapp.vercel.app/api/auth/sign-in/social \
  -H "Content-Type: application/json" \
  -d '{"provider": "google"}' \
  -v
```

### Check Vercel Logs
```bash
# Install Vercel CLI
npm i -g vercel

# View logs
vercel logs --follow
```

### Update Better Auth
```bash
npm update better-auth
npm install
```

---

## Key Resources

- **Better Auth Docs**: https://www.better-auth.com/docs
- **Better Auth GitHub**: https://github.com/better-auth/better-auth
- **Next.js Integration**: https://www.better-auth.com/docs/integrations/next
- **Social Providers**: https://www.better-auth.com/docs/authentication/social-providers
- **Google OAuth Setup**: https://www.better-auth.com/docs/authentication/google
- **Vercel Deployment**: https://www.better-auth.com/docs/deployment

---

## Summary: The Critical Fix for Vercel OAuth

**The #1 issue**: Cookies not being set due to `sameSite` restrictions.

**The solution**:
```typescript
advanced: {
  useSecureCookies: true, // In production
  cookies: {
    session_token: {
      sameSite: "none",  // CRITICAL for OAuth
      secure: true,      // Required with sameSite: "none"
      httpOnly: true,    // Security
    },
  },
}
```

**Why it works**:
- OAuth flows cross domains (google.com → yourapp.vercel.app)
- `sameSite: "lax"` (default) blocks cross-site cookies
- `sameSite: "none"` allows cross-site cookies
- `secure: true` is mandatory with `sameSite: "none"`

**This single configuration change fixes 80% of Vercel OAuth issues!**

---

*Last Updated: 2025-12-08*
*Generated from: Grok chat analysis + Better Auth comparison*
