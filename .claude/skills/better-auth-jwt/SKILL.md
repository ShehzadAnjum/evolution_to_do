---
name: better-auth-jwt
description: Better Auth integration patterns for Next.js and FastAPI. Use when implementing authentication, JWT verification, OAuth providers, or protected routes.
---

# Better Auth JWT

## Next.js Setup

```typescript
// lib/auth/core/server.ts
import { betterAuth } from "better-auth";
import { Pool } from "@neondatabase/serverless";

export const auth = betterAuth({
  database: new Pool({ connectionString: process.env.DATABASE_URL }),
  emailAndPassword: { enabled: true },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    },
  },
  session: {
    cookieCache: { enabled: true, maxAge: 60 * 5 },
  },
  advanced: {
    useSecureCookies: process.env.BETTER_AUTH_URL?.startsWith("https://") ?? false,
  },
});
```

## FastAPI JWT Verification

```python
from jose import jwt, JWTError
from fastapi import Depends, HTTPException

async def get_current_user_id(authorization: str = Header(...)) -> str:
    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

## Protected API Route

```typescript
// app/api/auth/[...all]/route.ts
import { auth } from "@/lib/auth/core/server";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
```

## Client-Side Auth

```typescript
import { createAuthClient } from "better-auth/react";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_APP_URL,
});

// Usage
const { data: session } = authClient.useSession();
await authClient.signIn.email({ email, password });
await authClient.signOut();
```

## Common Issues

| Issue | Solution |
|-------|----------|
| Cookies not set | Check `useSecureCookies` matches URL protocol |
| CORS errors | Add frontend URL to backend CORS |
| Session undefined | Ensure auth API route exists at `/api/auth/[...all]` |
