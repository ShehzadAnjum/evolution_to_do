/**
 * Preview URL Detection for Vercel
 *
 * Detects Vercel preview deployments and returns the correct base URL
 * for Better Auth configuration.
 */

/**
 * Get the correct base URL for Better Auth
 *
 * In production: Uses BETTER_AUTH_URL
 * In preview: Uses the preview deployment URL from Vercel headers
 */
export function getAuthBaseURL(request?: Request): string {
  // Always use BETTER_AUTH_URL if explicitly set
  if (process.env.BETTER_AUTH_URL) {
    return process.env.BETTER_AUTH_URL;
  }

  // In preview deployments, use the Vercel deployment URL
  if (process.env.VERCEL_URL) {
    return `https://${process.env.VERCEL_URL}`;
  }

  // Fallback to NEXT_PUBLIC_APP_URL or localhost
  return process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000";
}

/**
 * Check if current deployment is a Vercel preview
 */
export function isVercelPreview(): boolean {
  return (
    process.env.VERCEL === "1" &&
    process.env.VERCEL_ENV === "preview"
  );
}

/**
 * Get trusted origins including preview URLs
 */
export function getTrustedOrigins(): string[] {
  const origins: string[] = [];

  // Add production URL
  if (process.env.BETTER_AUTH_URL) {
    origins.push(process.env.BETTER_AUTH_URL);
  }

  // Add preview URL if in preview environment
  if (isVercelPreview() && process.env.VERCEL_URL) {
    origins.push(`https://${process.env.VERCEL_URL}`);
  }

  // Add wildcard for all Vercel deployments
  origins.push("https://*.vercel.app");

  // Add localhost for development
  if (process.env.NODE_ENV === "development") {
    origins.push("http://localhost:3000");
    origins.push("http://localhost:3001");
  }

  return origins;
}
