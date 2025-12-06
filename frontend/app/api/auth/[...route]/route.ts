import { toNextJsHandler } from "better-auth/next-js";

/**
 * Better-Auth API route handler
 * 
 * This catch-all route handles all authentication endpoints:
 * - /api/auth/sign-in
 * - /api/auth/sign-up
 * - /api/auth/sign-out
 * - /api/auth/session
 * - /api/auth/callback/google
 * - And all other Better-Auth endpoints
 * 
 * The route pattern [...route] catches all paths under /api/auth/*
 * 
 * Dynamic import prevents build-time evaluation of auth config
 */
export const dynamic = "force-dynamic";

async function getAuthHandler() {
  const { auth } = await import("@/lib/auth/core/server");
  return toNextJsHandler(auth.handler);
}

export async function GET(request: Request) {
  const handler = await getAuthHandler();
  return handler.GET(request);
}

export async function POST(request: Request) {
  const handler = await getAuthHandler();
  return handler.POST(request);
}

