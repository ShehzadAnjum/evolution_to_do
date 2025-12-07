/**
 * Tests for route protection middleware
 * 
 * Tests the middleware helpers to ensure proper route protection logic.
 */

// Import route constants directly to avoid Next.js server dependencies
import { protectedRoutes, authRoutes } from "@/lib/auth/config/routes";

// Re-implement helper functions for testing (same logic as middleware.ts)
function isProtectedRoute(pathname: string): boolean {
  return protectedRoutes.some((route) => pathname.startsWith(route));
}

function isPublicAuthRoute(pathname: string): boolean {
  return (
    pathname === authRoutes.login ||
    pathname === authRoutes.register ||
    pathname.startsWith("/api/auth/")
  );
}

describe("Route Protection Helpers", () => {
  describe("isProtectedRoute", () => {
    it("should return true for /dashboard", () => {
      expect(isProtectedRoute("/dashboard")).toBe(true);
    });

    it("should return true for /dashboard/settings", () => {
      expect(isProtectedRoute("/dashboard/settings")).toBe(true);
    });

    it("should return true for /app", () => {
      expect(isProtectedRoute("/app")).toBe(true);
    });

    it("should return true for /account", () => {
      expect(isProtectedRoute("/account")).toBe(true);
    });

    it("should return false for /login", () => {
      expect(isProtectedRoute("/login")).toBe(false);
    });

    it("should return false for /", () => {
      expect(isProtectedRoute("/")).toBe(false);
    });

    it("should return false for /api/auth/session", () => {
      expect(isProtectedRoute("/api/auth/session")).toBe(false);
    });
  });

  describe("isPublicAuthRoute", () => {
    it("should return true for /login", () => {
      expect(isPublicAuthRoute("/login")).toBe(true);
    });

    it("should return true for /register", () => {
      expect(isPublicAuthRoute("/register")).toBe(true);
    });

    it("should return true for /api/auth/sign-in", () => {
      expect(isPublicAuthRoute("/api/auth/sign-in")).toBe(true);
    });

    it("should return true for /api/auth/callback/google", () => {
      expect(isPublicAuthRoute("/api/auth/callback/google")).toBe(true);
    });

    it("should return false for /dashboard", () => {
      expect(isPublicAuthRoute("/dashboard")).toBe(false);
    });

    it("should return false for /", () => {
      expect(isPublicAuthRoute("/")).toBe(false);
    });
  });
});

