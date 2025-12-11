# ADR-007: Multi-Version Deployment Strategy

## Status
Accepted

## Date
2025-12-12

## Context

We needed to deploy multiple versions of the frontend simultaneously:
- **v2.0.0** (main): New GUI with sidebar, filters, dark mode
- **v1.0.0** (iteration-1): Original iteration design for comparison/demo

Vercel's default model deploys one production URL per project. We explored several approaches:
1. Path-based routing (`/v1`, `/v2`) - Not supported by Vercel
2. Branch preview deployments - URLs change on each deploy
3. Vercel aliases on preview deployments - URLs change, alias must be re-applied
4. Separate Vercel projects - Requires separate environment configuration

## Decision

**Use separate Vercel projects for each version** with explicit environment configuration.

### Architecture

```
GitHub Repository (main + iteration-1 branches)
         │
         ├── evolution-to-do (Vercel Project - Production)
         │   └── Connected to: main branch
         │   └── URL: https://evolution-to-do.vercel.app
         │   └── Auto-deploy: Yes (GitHub integration)
         │
         └── evolution-todo-v1 (Vercel Project - Iteration 1)
             └── Deployed via: Vercel CLI from iteration-1 branch
             └── URL: https://evolution-todo-v1.vercel.app
             └── Auto-deploy: No (manual CLI deployment)
```

### Configuration Requirements

Each project requires its own environment variables:

| Variable | evolution-to-do | evolution-todo-v1 |
|----------|-----------------|-------------------|
| `BETTER_AUTH_URL` | `https://evolution-to-do.vercel.app` | `https://evolution-todo-v1.vercel.app` |
| `NEXT_PUBLIC_APP_URL` | `https://evolution-to-do.vercel.app` | `https://evolution-todo-v1.vercel.app` |
| `DATABASE_URL` | Same Neon URL | Same Neon URL |
| `BETTER_AUTH_SECRET` | Same secret | Same secret |
| `GOOGLE_CLIENT_ID` | Same client ID | Same client ID |
| `NEXT_PUBLIC_API_URL` | Same Railway URL | Same Railway URL |

### Code Changes Required

1. **Better Auth trustedOrigins** - Add all deployment URLs:
   ```typescript
   trustedOrigins: [
     env.BETTER_AUTH_URL,
     "https://evolution-to-do.vercel.app",
     "https://evolution-todo-v1.vercel.app",
   ]
   ```

2. **Backend CORS origins** - Add all frontend URLs:
   ```python
   origins.extend([
     "https://evolution-to-do.vercel.app",
     "https://evolution-todo-v1.vercel.app",
   ])
   ```

3. **Google OAuth** - Add redirect URIs for each deployment:
   ```
   https://evolution-to-do.vercel.app/api/auth/callback/google
   https://evolution-todo-v1.vercel.app/api/auth/callback/google
   ```

## Consequences

### Positive
- Each version has a stable, memorable URL
- Versions are completely independent
- Can deploy updates to one without affecting other
- Clear separation of concerns

### Negative
- Must maintain environment variables in multiple places
- Google OAuth requires multiple redirect URIs
- Manual CLI deployment for secondary projects (no auto-deploy)
- Backend CORS list grows with each deployment

### Neutral
- Both versions share the same database (by design)
- Both versions share the same backend API

## Alternatives Considered

### 1. Vercel Preview Deployments with Aliases
**Rejected because**: Each `vercel` CLI deployment generates a new URL. Aliases must be re-applied after each deploy, and the underlying URL changes break OAuth if not updated.

### 2. Vercel Deployment Protection Bypass
**Rejected because**: Preview deployments with deployment protection require Vercel authentication, adding friction for demos.

### 3. Single Project with Multiple Branches
**Rejected because**: GitHub integration only auto-deploys one branch to production. Other branches get preview URLs that aren't stable.

## References
- [Vercel Deployment Documentation](https://vercel.com/docs/deployments)
- [Better Auth trustedOrigins](https://www.better-auth.com/docs/configuration)
- ADR-001: Authentication Stack (Better Auth)
