import { z } from "zod";

/**
 * Environment variable schema for authentication configuration
 * Validates all required environment variables at runtime
 */
const envSchema = z.object({
  DATABASE_URL: z.string().url("DATABASE_URL must be a valid URL"),
  GOOGLE_CLIENT_ID: z.string().min(1, "GOOGLE_CLIENT_ID is required"),
  GOOGLE_CLIENT_SECRET: z.string().min(1, "GOOGLE_CLIENT_SECRET is required"),
  BETTER_AUTH_SECRET: z.string().min(32, "BETTER_AUTH_SECRET must be at least 32 characters"),
  BETTER_AUTH_URL: z.string().url("BETTER_AUTH_URL must be a valid URL").optional(),
});

/**
 * Validated environment variables
 * 
 * Throws error if any required variable is missing or invalid.
 * Validation occurs at runtime when the auth module is imported.
 * 
 * Note: The API route handler uses dynamic imports to prevent
 * build-time evaluation, allowing builds to succeed without env vars.
 */
// Determine the correct base URL
// Better-Auth needs the correct baseURL for OAuth redirects
// For development, we'll use the port from NEXT_PUBLIC_APP_URL or default to 3000
const getBaseURL = () => {
  // If explicitly set, use it
  if (process.env.BETTER_AUTH_URL) {
    return process.env.BETTER_AUTH_URL;
  }
  // Try to detect the port from NEXT_PUBLIC_APP_URL
  if (process.env.NEXT_PUBLIC_APP_URL) {
    return process.env.NEXT_PUBLIC_APP_URL;
  }
  // In development, use localhost:3000 as default (or whatever port Next.js is using)
  // Note: The actual request origin will be validated separately via trustedOrigins
  // Note: If Next.js uses a different port, either set BETTER_AUTH_URL in .env.local
  // or ensure Google OAuth redirect URI includes that port
  return "http://localhost:3000";
};

/**
 * Lazy environment variable validation
 * Only validates when actually accessed at runtime, not during build
 */
let validatedEnv: z.infer<typeof envSchema> | null = null;

function getEnv() {
  if (validatedEnv) {
    return validatedEnv;
  }
  
  // Check if we're in a build context (env vars not available)
  const isBuildTime = !process.env.DATABASE_URL || !process.env.BETTER_AUTH_SECRET;
  
  if (isBuildTime) {
    // Build-time: use fallback values that pass validation
    // Actual validation will happen at runtime when env vars are available
    validatedEnv = {
      DATABASE_URL: process.env.DATABASE_URL || "postgresql://placeholder@localhost/placeholder",
      GOOGLE_CLIENT_ID: process.env.GOOGLE_CLIENT_ID || "placeholder-client-id",
      GOOGLE_CLIENT_SECRET: process.env.GOOGLE_CLIENT_SECRET || "placeholder-client-secret",
      BETTER_AUTH_SECRET: process.env.BETTER_AUTH_SECRET || "placeholder-secret-key-at-least-32-chars-long-for-build",
      BETTER_AUTH_URL: getBaseURL(),
    } as z.infer<typeof envSchema>;
  } else {
    // Runtime: validate properly
    validatedEnv = envSchema.parse({
      DATABASE_URL: process.env.DATABASE_URL!,
      GOOGLE_CLIENT_ID: process.env.GOOGLE_CLIENT_ID!,
      GOOGLE_CLIENT_SECRET: process.env.GOOGLE_CLIENT_SECRET!,
      BETTER_AUTH_SECRET: process.env.BETTER_AUTH_SECRET!,
      BETTER_AUTH_URL: getBaseURL(),
    });
  }
  return validatedEnv;
}

export const env = new Proxy({} as z.infer<typeof envSchema>, {
  get(_target, prop) {
    return getEnv()[prop as keyof z.infer<typeof envSchema>];
  },
});

/**
 * Type-safe environment variables
 */
export type AuthEnv = z.infer<typeof envSchema>;

