/**
 * Tests for environment variable validation
 * 
 * Tests the env.ts module to ensure proper validation
 * of required environment variables.
 */

describe("Environment Variable Validation", () => {
  const originalEnv = process.env;

  beforeEach(() => {
    // Reset modules to clear cached imports
    jest.resetModules();
    process.env = { ...originalEnv };
  });

  afterEach(() => {
    process.env = originalEnv;
  });

  describe("env validation", () => {
    it("should throw error when DATABASE_URL is missing", () => {
      delete process.env.DATABASE_URL;
      expect(() => {
        require("@/lib/auth/config/env");
      }).toThrow();
    });

    it("should throw error when DATABASE_URL is invalid", () => {
      process.env.DATABASE_URL = "not-a-valid-url";
      expect(() => {
        require("@/lib/auth/config/env");
      }).toThrow();
    });

    it("should throw error when GOOGLE_CLIENT_ID is missing", () => {
      process.env.DATABASE_URL = "postgresql://user:pass@host/db";
      delete process.env.GOOGLE_CLIENT_ID;
      expect(() => {
        require("@/lib/auth/config/env");
      }).toThrow();
    });

    it("should throw error when GOOGLE_CLIENT_SECRET is missing", () => {
      process.env.DATABASE_URL = "postgresql://user:pass@host/db";
      process.env.GOOGLE_CLIENT_ID = "test-client-id";
      delete process.env.GOOGLE_CLIENT_SECRET;
      expect(() => {
        require("@/lib/auth/config/env");
      }).toThrow();
    });

    it("should throw error when BETTER_AUTH_SECRET is too short", () => {
      process.env.DATABASE_URL = "postgresql://user:pass@host/db";
      process.env.GOOGLE_CLIENT_ID = "test-client-id";
      process.env.GOOGLE_CLIENT_SECRET = "test-secret";
      process.env.BETTER_AUTH_SECRET = "short"; // Less than 32 chars
      expect(() => {
        require("@/lib/auth/config/env");
      }).toThrow();
    });

    it("should accept valid environment variables", () => {
      process.env.DATABASE_URL = "postgresql://user:pass@host/db";
      process.env.GOOGLE_CLIENT_ID = "test-client-id";
      process.env.GOOGLE_CLIENT_SECRET = "test-secret";
      process.env.BETTER_AUTH_SECRET = "a".repeat(32); // At least 32 chars
      
      // Should not throw
      expect(() => {
        const { env } = require("@/lib/auth/config/env");
        expect(env.DATABASE_URL).toBe("postgresql://user:pass@host/db");
        expect(env.GOOGLE_CLIENT_ID).toBe("test-client-id");
      }).not.toThrow();
    });

    it("should use default BETTER_AUTH_URL when not provided", () => {
      process.env.DATABASE_URL = "postgresql://user:pass@host/db";
      process.env.GOOGLE_CLIENT_ID = "test-client-id";
      process.env.GOOGLE_CLIENT_SECRET = "test-secret";
      process.env.BETTER_AUTH_SECRET = "a".repeat(32);
      delete process.env.BETTER_AUTH_URL;
      delete process.env.NEXT_PUBLIC_APP_URL;

      const { env } = require("@/lib/auth/config/env");
      expect(env.BETTER_AUTH_URL).toBe("http://localhost:3000");
    });
  });
});




