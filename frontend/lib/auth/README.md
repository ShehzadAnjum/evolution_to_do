# Better-Auth Module

A reusable authentication module for Next.js applications using Better-Auth, Neon Postgres, and JWT sessions.

## Features

- ✅ Email/password authentication (sign-up, sign-in)
- ✅ Google OAuth integration
- ✅ JWT session management
- ✅ Route protection middleware
- ✅ Server and client helpers
- ✅ Type-safe with TypeScript
- ✅ Dark theme UI with Tailwind CSS

## Quick Start

### Installation

The module is already integrated into this Next.js app. To use it in another project, copy the `lib/auth` directory.

### Environment Variables

Create `.env.local` with:

```env
DATABASE_URL=postgresql://user:pass@host/db
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
BETTER_AUTH_SECRET=your_32_character_secret
BETTER_AUTH_URL=http://localhost:3000
```

### Usage

#### Server Component

```tsx
import { getCurrentUser } from "@/lib/auth";
import { redirect } from "next/navigation";

export default async function Page() {
  const user = await getCurrentUser();
  if (!user) redirect("/login");
  return <div>Welcome {user.email}</div>;
}
```

#### Client Component

```tsx
"use client";
import { authClient } from "@/lib/auth";

export function UserProfile() {
  const { data: session } = await authClient.getSession();
  return <div>{session?.user?.email}</div>;
}
```

#### Login Page

```tsx
import { LoginPage } from "@/lib/auth";

export default function LoginRoute() {
  return <LoginPage />;
}
```

## API Reference

### Server Helpers

- `getCurrentUser()` - Get current authenticated user (returns `null` if not authenticated)
- `requireAuth()` - Get current user or redirect to login
- `authMiddleware(request)` - Middleware helper for route protection

### Client Helpers

- `authClient.signIn.email({ email, password })` - Sign in with email/password
- `authClient.signUp.email({ email, password, name })` - Sign up with email/password
- `authClient.signIn.social({ provider: "google" })` - Sign in with Google OAuth
- `authClient.signOut()` - Sign out current user
- `authClient.getSession()` - Get current session

### UI Components

- `<LoginPage />` - Complete login/register page
- `<AuthForm mode="login" | "register" />` - Email/password form
- `<SocialButtons />` - Social authentication buttons

## Route Protection

### Middleware (Automatic)

Protected routes are automatically protected via `middleware.ts`:
- `/dashboard/*`
- `/app/*`
- `/account/*`

### Manual Protection

```tsx
import { requireAuth } from "@/lib/auth";

export default async function ProtectedPage() {
  const user = await requireAuth(); // Redirects if not authenticated
  return <div>Protected content</div>;
}
```

## Testing

Run tests:

```bash
npm test
```

Test coverage includes:
- Environment variable validation
- Route protection helpers
- Route constants

## Architecture

```
lib/auth/
├── index.ts              # Main entry point
├── adapters/            # Database adapters
├── config/              # Configuration
├── core/                # Better-Auth instances
├── http/                # Middleware & helpers
└── ui/                  # React components
```

## License

Part of the better-auth-app project.




