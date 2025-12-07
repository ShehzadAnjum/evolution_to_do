import { env } from "./env";

/**
 * Google OAuth provider configuration
 */
export const googleProvider = {
  clientId: env.GOOGLE_CLIENT_ID,
  clientSecret: env.GOOGLE_CLIENT_SECRET,
} as const;

/**
 * All OAuth providers configuration
 */
export const providers = {
  google: googleProvider,
} as const;

