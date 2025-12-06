"use client";

/**
 * Get JWT token from Better Auth session
 *
 * Better Auth stores JWT tokens in httpOnly cookies, which can't be
 * accessed from client-side JavaScript. This helper calls a server-side
 * API route that extracts the token from the session cookie.
 *
 * @returns JWT token string or null if not authenticated
 */
export async function getAuthToken(): Promise<string | null> {
  try {
    // Call server-side API route to get token from httpOnly cookie
    const response = await fetch("/api/auth/token", {
      method: "GET",
      credentials: "include", // Include cookies in request
    });

    if (!response.ok) {
      if (response.status === 401) {
        // Not authenticated
        return null;
      }
      throw new Error(`Failed to get token: ${response.statusText}`);
    }

    const data = await response.json();
    return data.token || null;
  } catch (error) {
    console.error("Error getting auth token:", error);
    return null;
  }
}
