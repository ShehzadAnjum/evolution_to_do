/**
 * Tests for route constants
 * 
 * Ensures route paths are correctly defined and consistent.
 */

import { authRoutes, protectedRoutes } from "@/lib/auth/config/routes";

describe("Route Constants", () => {
  describe("authRoutes", () => {
    it("should have correct login route", () => {
      expect(authRoutes.login).toBe("/login");
    });

    it("should have correct register route", () => {
      expect(authRoutes.register).toBe("/register");
    });

    it("should have correct logout route", () => {
      expect(authRoutes.logout).toBe("/api/auth/logout");
    });

    it("should have correct session route", () => {
      expect(authRoutes.session).toBe("/api/auth/session");
    });

    it("should have correct Google callback route", () => {
      expect(authRoutes.callback.google).toBe("/api/auth/callback/google");
    });
  });

  describe("protectedRoutes", () => {
    it("should include /dashboard", () => {
      expect(protectedRoutes).toContain("/dashboard");
    });

    it("should include /app", () => {
      expect(protectedRoutes).toContain("/app");
    });

    it("should include /account", () => {
      expect(protectedRoutes).toContain("/account");
    });

    it("should be an array", () => {
      expect(Array.isArray(protectedRoutes)).toBe(true);
    });
  });
});




