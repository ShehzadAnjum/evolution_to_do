import { cookies } from "next/headers";
import { auth } from "../core/server";

/**
 * Get current user from server-side
 * 
 * Use this in Server Components and Server Actions to get the authenticated user.
 * Returns null if user is not authenticated.
 * 
 * @example
 * ```tsx
 * // app/dashboard/page.tsx
 * import { getCurrentUser } from "@/lib/auth/http/helpers";
 * 
 * export default async function DashboardPage() {
 *   const user = await getCurrentUser();
 *   if (!user) {
 *     redirect("/login");
 *   }
 *   return <div>Welcome, {user.email}</div>;
 * }
 * ```
 */
export async function getCurrentUser() {
  try {
    const cookieStore = await cookies();
    const session = await auth.api.getSession({
      headers: new Headers({
        cookie: cookieStore.toString(),
      }),
    });

    // Better-Auth returns { session, user } directly
    return session?.user || null;
  } catch (error) {
    return null;
  }
}

/**
 * Require authentication
 * 
 * Throws an error or redirects if user is not authenticated.
 * Use in Server Components that require authentication.
 * 
 * @example
 * ```tsx
 * import { requireAuth } from "@/lib/auth/http/helpers";
 * import { redirect } from "next/navigation";
 * 
 * export default async function ProtectedPage() {
 *   const user = await requireAuth();
 *   return <div>Welcome, {user.email}</div>;
 * }
 * ```
 */
export async function requireAuth() {
  const user = await getCurrentUser();
  if (!user) {
    const { redirect } = await import("next/navigation");
    redirect("/login");
  }
  return user;
}

