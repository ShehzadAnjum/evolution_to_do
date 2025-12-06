import { authMiddleware } from "@/lib/auth/http/middleware";
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

/**
 * Next.js Middleware
 * 
 * Protects routes defined in lib/auth/config/routes.ts
 * Unauthenticated users are redirected to /login
 * 
 * Matches:
 * - /dashboard/*
 * - /app/*
 * - /account/*
 */
export async function middleware(request: NextRequest) {
  return authMiddleware(request);
}

/**
 * Middleware configuration
 * 
 * Matches protected route patterns
 */
export const config = {
  matcher: [
    "/dashboard/:path*",
    "/app/:path*",
    "/account/:path*",
  ],
};




