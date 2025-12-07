# Frontend Context: Evolution of Todo (Phase II)

**Stack**: Next.js 14 | React | TypeScript | Better Auth | Tailwind CSS
**Last Updated**: 2025-12-06
**Status**: Auth module integrated, task management pending

---

## Quick Reference

```bash
cd frontend

# Development
npm install              # Install dependencies (already done)
npm run dev              # Start dev server (localhost:3000)
npm run build            # Production build
npm run lint             # Run ESLint
npm run test             # Run Jest tests

# Before running, create .env.local:
cp .env.example .env.local
# Then edit .env.local with your credentials
```

---

## Directory Structure

```
frontend/
├── app/                         # Next.js App Router
│   ├── layout.tsx               # Root layout
│   ├── page.tsx                 # Home page
│   ├── globals.css              # Global styles
│   ├── api/
│   │   └── auth/[...route]/     # Better Auth API route
│   ├── login/
│   │   └── page.tsx             # Login/signup page
│   └── dashboard/
│       └── page.tsx             # Protected dashboard (add tasks here)
│
├── components/
│   └── ui/                      # shadcn/ui components
│
├── lib/
│   ├── utils.ts                 # Utility functions
│   └── auth/                    # Better Auth module
│       ├── index.ts             # Main entry point
│       ├── core/
│       │   ├── server.ts        # Server-side auth
│       │   └── client.ts        # Client-side auth
│       ├── config/
│       │   ├── env.ts           # Environment validation
│       │   ├── providers.ts     # OAuth providers
│       │   └── routes.ts        # Route constants
│       ├── adapters/
│       │   └── db-adapter.ts    # Neon PostgreSQL adapter
│       ├── http/
│       │   ├── middleware.ts    # Auth middleware
│       │   └── helpers.ts       # Server helpers
│       └── ui/
│           └── ...              # Auth UI components
│
├── middleware.ts                # Next.js middleware (route protection)
├── tests/                       # Jest tests
├── package.json
├── tailwind.config.ts
└── tsconfig.json
```

---

## Auth Module (Pre-built)

The authentication module is **complete and production-ready**:

### Features
- Email/password sign-up and sign-in
- Google OAuth (optional)
- JWT session management
- Route protection via middleware
- Neon PostgreSQL storage

### Usage

```typescript
// Server-side: Get current user
import { getCurrentUser, requireAuth } from '@/lib/auth';

export default async function ProtectedPage() {
  const user = await requireAuth(); // Redirects if not authenticated
  return <div>Hello, {user.email}</div>;
}

// Client-side: Sign out
import { signOut } from '@/lib/auth';

<button onClick={() => signOut()}>Sign Out</button>
```

### Routes
- `/login` - Login/signup page
- `/dashboard` - Protected dashboard
- `/api/auth/[...route]` - Auth API endpoints

---

## Environment Variables

```bash
# .env.local (required)
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
BETTER_AUTH_SECRET=your-32-character-secret-key
BETTER_AUTH_URL=http://localhost:3000

# Optional: Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
```

---

## What Needs to Be Added (Phase II Tasks)

### 1. Task Components
```
components/
└── tasks/
    ├── task-list.tsx        # Display all tasks
    ├── task-item.tsx        # Single task display
    ├── task-form.tsx        # Add/edit task form
    └── task-summary.tsx     # Total/completed counts
```

### 2. Task API Integration
```typescript
// lib/api.ts - Connect to FastAPI backend
const API_URL = process.env.NEXT_PUBLIC_API_URL;

export async function getTasks(token: string) { ... }
export async function createTask(token: string, data: TaskCreate) { ... }
export async function updateTask(token: string, id: string, data: TaskUpdate) { ... }
export async function deleteTask(token: string, id: string) { ... }
export async function toggleComplete(token: string, id: string) { ... }
```

### 3. Dashboard Enhancement
- Add task list component
- Add task form
- Add task CRUD operations
- Show summary stats

---

## TypeScript Types (To Add)

```typescript
// lib/types.ts
export interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string;
  is_complete: boolean;
  created_at: string;
  updated_at: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  is_complete?: boolean;
}
```

---

## Testing

```bash
# Run all tests
npm run test

# Current tests (29 passing):
# - Environment validation (7 tests)
# - Route protection (12 tests)
# - Route constants (10 tests)
```

---

## Current State

### Complete
- Next.js project setup
- Tailwind CSS + shadcn/ui
- Better Auth integration
- Login/signup pages
- Protected dashboard route
- JWT session management
- Neon PostgreSQL connection
- Route protection middleware
- 29 passing tests

### Pending (Phase II)
- Task list components
- Task CRUD operations
- API client for backend
- Task management UI

---

**Parent Context**: See `/CLAUDE.md` for project-wide instructions.
