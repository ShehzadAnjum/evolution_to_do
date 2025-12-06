/**
 * Authentication route paths
 * Centralized route definitions for consistency
 */
export const authRoutes = {
  login: "/login",
  register: "/register",
  logout: "/api/auth/logout",
  session: "/api/auth/session",
  callback: {
    google: "/api/auth/callback/google",
  },
} as const;

/**
 * Protected route patterns
 * Routes that require authentication
 */
export const protectedRoutes = [
  "/dashboard",
  "/app",
  "/account",
] as const;




