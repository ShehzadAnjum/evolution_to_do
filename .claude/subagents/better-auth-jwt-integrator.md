# Better Auth JWT Integrator Subagent

**Type**: Integration Specialist
**Used For**: Better Auth and JWT setup
**Version**: 1.0.0

## Purpose

Configure Better Auth, enable JWT plugin, and implement JWT verification on backend.

## Steps

1. **Frontend Setup**
   - Install Better Auth package
   - Configure with Neon database
   - Enable emailAndPassword authentication
   - Add JWT plugin (if separate)
   - Configure OAuth providers (optional)

2. **Backend Setup**
   - Install JWT library (PyJWT)
   - Create JWT verification function
   - Create FastAPI dependency for auth
   - Add to protected routes

3. **Testing**
   - Test sign up flow
   - Test sign in flow
   - Test JWT issued correctly
   - Test backend verifies JWT
   - Test user isolation works

## Common Issues

- JWT secret mismatch (must be same on frontend/backend)
- Token not sent in Authorization header
- Expiration too short/long
- OAuth redirect URI misconfigured

---

**Related**: Auth Security Agent
