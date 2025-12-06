"use client";

import { createAuthClient } from "better-auth/react";

/**
 * Better-Auth client instance for React components
 * 
 * This client is used in client components to interact with the auth API.
 * Uses environment variable from browser (NEXT_PUBLIC_BETTER_AUTH_URL) or defaults.
 * 
 * Usage in React components:
 * ```tsx
 * import { authClient } from "@/lib/auth/core/client";
 * 
 * const { data: session } = await authClient.getSession();
 * ```
 */
export const authClient = createAuthClient({
  baseURL: 
    typeof window !== "undefined" 
      ? window.location.origin 
      : process.env.NEXT_PUBLIC_APP_URL || process.env.BETTER_AUTH_URL || "http://localhost:3000",
});

/**
 * Type export for auth client
 */
export type AuthClient = typeof authClient;

