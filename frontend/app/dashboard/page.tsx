import { redirect } from "next/navigation";

/**
 * Protected Dashboard Page
 * 
 * Example of a protected route that requires authentication.
 * Uses requireAuth() helper to ensure user is authenticated.
 * 
 * Route: /dashboard
 */
export default async function DashboardPage() {
  // Redirect to tasks page (main application)
  redirect("/tasks");
}

