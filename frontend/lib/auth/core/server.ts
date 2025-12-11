import { betterAuth } from "better-auth";
import { env } from "../config/env";
import { providers } from "../config/providers";
import { db } from "../adapters/db-adapter";

/**
 * Better-Auth server instance
 *
 * This is the core authentication server configuration.
 * Configured with:
 * - Neon Postgres database (via Pool - Better-Auth creates Kysely internally)
 * - JWT session strategy
 * - Google OAuth provider (if credentials provided)
 * - Environment-based configuration
 *
 * Uses environment variables from the current project.
 */
// Build auth config - conditionally add Google OAuth
const hasGoogleCredentials = env.GOOGLE_CLIENT_ID &&
                             env.GOOGLE_CLIENT_ID.length > 0 &&
                             env.GOOGLE_CLIENT_SECRET &&
                             env.GOOGLE_CLIENT_SECRET.length > 0;

const authConfig: Parameters<typeof betterAuth>[0] = {
  baseURL: env.BETTER_AUTH_URL,
  secret: env.BETTER_AUTH_SECRET,
  database: db, // Neon Pool - Better-Auth detects PostgreSQL and creates adapter internally
  basePath: "/api/auth", // Explicit base path (matches API route)
  emailAndPassword: {
    enabled: true, // Enable email/password authentication
  },
  // Trusted origins for CORS and preview deployments
  trustedOrigins: [
    env.BETTER_AUTH_URL,
    "https://evolution-to-do.vercel.app",
    "https://frontend-3wxhtu1pv-shehzadanjums-projects.vercel.app", // iteration-1 preview
  ].filter(Boolean) as string[],
  // Production OAuth configuration for Vercel
  // Note: Better Auth v1.4.5 handles cookie security automatically based on NODE_ENV
  // In production (HTTPS), cookies are automatically secure and httpOnly
  advanced: {
    // Enable secure cookies in production
    useSecureCookies: process.env.NODE_ENV === "production",
  },
};

// Only add Google OAuth if credentials are provided
if (hasGoogleCredentials) {
  authConfig.socialProviders = {
    google: {
      clientId: env.GOOGLE_CLIENT_ID!,
      clientSecret: env.GOOGLE_CLIENT_SECRET!,
      // Explicit callback URL for Vercel (avoids auto-detection issues)
      redirectURI: `${env.BETTER_AUTH_URL}/api/auth/callback/google`,
      // Force Google to show account selection screen every time
      // This ensures users can choose a different account after logout
      // According to Better Auth docs, prompt can be set directly on the provider
      prompt: "select_account", // Always show account picker
      // Map Google profile to user fields
      mapProfileToUser: (profile: any) => {
        return {
          name: profile.name || profile.email?.split("@")[0] || undefined,
          email: profile.email,
          image: profile.picture || undefined,
        };
      },
    },
  };
}

export const auth = betterAuth(authConfig);

/**
 * Type export for auth instance
 */
export type Auth = typeof auth;

