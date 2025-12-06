/**
 * Better-Auth Module - Main Entry Point
 * 
 * This is the single public entry point for the authentication module.
 * The rest of the app should import only from this file, never from deep files.
 * 
 * This module provides:
 * - Server-side authentication helpers
 * - Client-side authentication helpers
 * - UI components
 * - Route protection utilities
 * 
 * @example
 * ```tsx
 * // Server Component
 * import { getCurrentUser } from "@/lib/auth";
 * 
 * export default async function Page() {
 *   const user = await getCurrentUser();
 *   return <div>Hello {user?.email}</div>;
 * }
 * ```
 * 
 * @example
 * ```tsx
 * // Client Component
 * import { authClient } from "@/lib/auth";
 * 
 * const { data: session } = await authClient.getSession();
 * ```
 */

// Server-side exports
export { auth } from "./core/server";
export type { Auth } from "./core/server";
export { getCurrentUser, requireAuth } from "./http/helpers";
export { authMiddleware, isProtectedRoute, isPublicAuthRoute } from "./http/middleware";

// Client-side exports
export { authClient } from "./core/client";
export type { AuthClient } from "./core/client";

// UI Components
export { AuthForm } from "./ui/components/AuthForm";
export type { AuthMode, AuthFormProps } from "./ui/components/AuthForm";
export { SocialButtons } from "./ui/components/SocialButtons";
export type { SocialButtonsProps } from "./ui/components/SocialButtons";
export { LoginPage } from "./ui/pages/LoginPage";

// Configuration exports
export { authRoutes, protectedRoutes } from "./config/routes";
export { env } from "./config/env";
export type { AuthEnv } from "./config/env";




