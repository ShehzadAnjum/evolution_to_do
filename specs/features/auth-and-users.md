# Feature: Authentication and Users

**Phases**: II, III, IV, V
**Status**: Implemented (Phase II)
**Version**: 02.002.000

---

## Overview

User authentication and authorization using Better Auth with JWT tokens. Enables multi-user functionality with secure session management and user isolation.

---

## Key Components

### 1. User Registration (Sign Up)
- Email/password registration
- Optional: Google OAuth
- User profile creation
- Automatic sign-in after registration

### 2. User Login (Sign In)
- Email/password authentication
- Google OAuth option
- JWT token issuance
- Session creation

### 3. User Logout (Sign Out)
- Session termination
- Token invalidation
- Redirect to login page

### 4. Session Management
- JWT tokens for stateless auth
- Token validation on every API request
- Token refresh (as needed)
- Session persistence across page reloads

### 5. User Isolation
- All data scoped to user_id
- Backend validates user_id matches token
- Frontend only shows current user's data

---

## Technology Stack

- **Better Auth**: Authentication library (JS/TS)
- **JWT**: JSON Web Tokens for session
- **Neon PostgreSQL**: User data storage
- **Next.js**: Frontend auth flow
- **FastAPI**: Backend JWT verification

---

## Data Model

See `specs/database/schema.md` for user schema (managed by Better Auth).

**User Fields**:
```typescript
{
  id: string,
  email: string (unique),
  name: string | null,
  image: string | null (from OAuth),
  created_at: timestamp,
  updated_at: timestamp
}
```

---

## API Endpoints

All auth endpoints are managed by Better Auth:
- `/api/auth/sign-up` - Register new user
- `/api/auth/sign-in` - Login
- `/api/auth/sign-out` - Logout
- `/api/auth/session` - Get current session
- `/api/auth/callback/google` - OAuth callback

---

## Security Requirements

1. **Password Security**:
   - Minimum 8 characters
   - Hashed with bcrypt
   - Never stored in plaintext

2. **Token Security**:
   - Signed with secret key
   - Short expiration (7 days)
   - Validated on every request

3. **User Isolation**:
   - Backend validates user_id in URL matches token
   - Database queries filtered by user_id
   - No cross-user data access

4. **Environment Security**:
   - Secrets in environment variables
   - HTTPS in production
   - Secure cookies

---

## User Stories

### US-AUTH-1: User Registration
As a new user, I want to create an account so I can use the app.

**Acceptance Criteria**:
- Can sign up with email/password
- Can sign up with Google (optional)
- Receive confirmation after signup
- Auto-login after successful signup

### US-AUTH-2: User Login
As a returning user, I want to log in so I can access my tasks.

**Acceptance Criteria**:
- Can login with email/password
- Can login with Google (if configured)
- Redirect to dashboard after login
- Error message for invalid credentials

### US-AUTH-3: User Logout
As a logged-in user, I want to log out so I can end my session.

**Acceptance Criteria**:
- Logout button accessible
- Redirect to login after logout
- Session terminated
- Cannot access protected pages after logout

### US-AUTH-4: Session Persistence
As a user, I want to stay logged in so I don't have to login repeatedly.

**Acceptance Criteria**:
- Session persists across page reloads
- Session persists across browser closes (optional)
- Token auto-refreshes before expiration

---

## Current Implementation Status

- ✅ Phase II: Complete (Better Auth integrated)
  - Email/password authentication working
  - Google OAuth configured
  - JWT tokens issued
  - User isolation enforced
  - Protected routes working

---

## References

- Better Auth Config: `frontend/lib/auth/core/server.ts`
- Backend JWT Verification: `backend/src/middleware/auth.py` (TBD)
- Auth Spec Document: `docs/BETTER_AUTH_REFERENCE.md`
- Phase II Spec: `specs/phases/phase-2.md`
