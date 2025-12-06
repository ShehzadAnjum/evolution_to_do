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
  emailAndPassword: {
    enabled: true, // Enable email/password authentication
  },
  // Disable origin check for development
  originCheck: false,
};

// Only add Google OAuth if credentials are provided
if (hasGoogleCredentials) {
  authConfig.socialProviders = {
    google: {
      clientId: env.GOOGLE_CLIENT_ID!,
      clientSecret: env.GOOGLE_CLIENT_SECRET!,
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

