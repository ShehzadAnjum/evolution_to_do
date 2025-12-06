# ADR-001: Authentication Stack with Better Auth

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together.

- **Status:** Accepted
- **Date:** 2025-12-07
- **Feature:** Phase II - Full-Stack Web Application
- **Context:** Phase II requires multi-user authentication with JWT tokens for API access

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? YES - Authentication is foundational
     2) Alternatives: Multiple viable options considered with tradeoffs? YES - Custom auth, NextAuth, Clerk, Better Auth
     3) Scope: Cross-cutting concern (not an isolated detail)? YES - Affects frontend, backend, database
-->

## Decision

Use Better Auth for authentication stack with the following components:

**Authentication Layer:**
- **Framework:** Better Auth v1.0.16
- **Token Type:** JWT (JSON Web Tokens)
- **Session Management:** HTTP-only cookies (frontend) + JWT validation (backend)
- **User Storage:** Neon PostgreSQL (managed by Better Auth migrations)
- **Password Hashing:** Better Auth built-in (bcrypt)
- **Token Extraction:** Custom server-side route (`/api/auth/token/route.ts`)

**Integration Pattern:**
- Frontend: Better Auth client for signup/signin/signout
- Backend: python-jose for JWT validation via `get_current_user_id()` dependency
- Database: Better Auth CLI migrations for user tables

## Consequences

### Positive

1. **Integrated Experience:** Better Auth handles user management, session management, and token generation out-of-the-box
2. **Security Best Practices:** HTTP-only cookies prevent XSS attacks, bcrypt hashing for passwords
3. **Type Safety:** Full TypeScript support on frontend with Better Auth client
4. **Rapid Development:** Reduced implementation time vs custom auth (saved ~8-12 hours)
5. **Migration Management:** Better Auth CLI handles database schema migrations (`npx @better-auth/cli migrate`)
6. **JWT Flexibility:** JWT tokens work seamlessly with FastAPI backend dependency injection
7. **Multi-Provider Ready:** Better Auth supports OAuth providers (Google, GitHub) for future phases

### Negative

1. **Learning Curve:** Team needed 30 minutes to read Better Auth documentation (30-minute rule)
2. **Framework Coupling:** Tight coupling to Better Auth library (migration to different auth would require refactoring)
3. **Custom Token Extraction:** Needed custom server-side route to extract JWT from HTTP-only cookie for API calls
4. **Database Schema Management:** Better Auth controls user table schema (less flexibility for custom user fields)
5. **Relatively New:** Better Auth is newer than NextAuth (potential for undiscovered edge cases)

## Alternatives Considered

### Alternative A: Custom Authentication Implementation
- **Components:** Custom JWT generation, bcrypt password hashing, manual session management
- **Pros:** Full control, no third-party dependencies, custom schema
- **Cons:**
  - Estimated 8-12 hours additional development time
  - Higher risk of security vulnerabilities (rolling your own auth)
  - No built-in session management
  - Manual token refresh logic
- **Why Rejected:** Violates "Quality Over Speed" principle - custom auth increases risk without proportional value for Phase II

### Alternative B: NextAuth.js
- **Components:** NextAuth v5, adapter for PostgreSQL, JWT strategy
- **Pros:** Mature ecosystem, extensive documentation, large community
- **Cons:**
  - More complex setup for JWT-only authentication
  - Heavier dependency (larger bundle size)
  - Session-first design (we need JWT-first for API)
  - Adapter configuration more complex than Better Auth
- **Why Rejected:** Better Auth offers simpler JWT-first pattern which better aligns with FastAPI backend

### Alternative C: Clerk
- **Components:** Clerk hosted authentication, pre-built components
- **Pros:** Beautiful UI components, hosted service, extensive features
- **Cons:**
  - Third-party hosted service (data privacy concerns)
  - Vendor lock-in (harder to migrate away)
  - Requires Clerk API keys (external dependency)
  - Pricing concerns for production (free tier limits)
- **Why Rejected:** Constitution principle "Repository Cleanliness" - prefer self-hosted solution in Neon database

### Alternative D: Supabase Auth
- **Components:** Supabase Auth + PostgreSQL
- **Pros:** Integrated with PostgreSQL, open-source, JWT support
- **Cons:**
  - Requires Supabase SDK (additional dependency)
  - Designed for Supabase ecosystem (not Neon)
  - Row Level Security patterns don't align with FastAPI backend
- **Why Rejected:** Better Auth integrates more cleanly with existing Neon PostgreSQL + FastAPI stack

## References

- Feature Spec: `specs/phase-2/spec.md` (FR-001 through FR-005)
- Implementation Plan: `specs/phase-2/plan.md` (lines 256-286 - Authentication Flow)
- Related ADRs: ADR-002 (Neon PostgreSQL), ADR-004 (TEXT user_id)
- Better Auth Documentation: https://www.better-auth.com/docs
- Implementation Evidence: `frontend/lib/auth/`, `backend/src/api/deps.py`
