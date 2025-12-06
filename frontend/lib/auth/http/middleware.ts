import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { authRoutes, protectedRoutes } from "../config/routes";

/**
 * Check if user has a valid session cookie
 * 
 * For Edge Runtime compatibility, we check for the session cookie.
 * Full session verification happens at the page/component level.
 * 
 * Better-Auth uses JWT sessions stored in cookies.
 * Cookie name pattern: better-auth.session_token
 */
export function hasSessionCookie(request: NextRequest): boolean {
  // Check for Better-Auth session cookie
  // Better-Auth stores JWT session in cookies
  const sessionCookie = request.cookies.get("better-auth.session_token");
  return !!sessionCookie;
}

/**
 * Check if a route requires authentication
 */
export function isProtectedRoute(pathname: string): boolean {
  return protectedRoutes.some((route) => pathname.startsWith(route));
}

/**
 * Check if a route is a public auth route (login, register, etc.)
 */
export function isPublicAuthRoute(pathname: string): boolean {
  return (
    pathname === authRoutes.login ||
    pathname === authRoutes.register ||
    pathname.startsWith("/api/auth/")
  );
}

/**
 * Auth middleware helper
 * 
 * Use this in Next.js middleware.ts to protect routes
 * 
 * @example
 * ```ts
 * // middleware.ts
 * import { authMiddleware } from "@/lib/auth/http/middleware";
 * 
 * export default authMiddleware;
 * ```
 */
export async function authMiddleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Allow public auth routes
  if (isPublicAuthRoute(pathname)) {
    return NextResponse.next();
  }

  // Check if route is protected
  if (isProtectedRoute(pathname)) {
    // Check for session cookie (Edge Runtime compatible)
    // Full session verification happens in server components
    if (!hasSessionCookie(request)) {
      // Redirect to login with return URL
      const loginUrl = new URL(authRoutes.login, request.url);
      loginUrl.searchParams.set("redirect", pathname);
      return NextResponse.redirect(loginUrl);
    }
  }

  return NextResponse.next();
}

