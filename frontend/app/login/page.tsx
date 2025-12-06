import { LoginPage } from "@/lib/auth/ui/pages/LoginPage";

/**
 * Login Page Route
 * 
 * Public route for user authentication.
 * Handles both login and registration via the LoginPage component.
 * 
 * Route: /login
 * 
 * Marked as dynamic to prevent static generation issues with client components
 */
export const dynamic = "force-dynamic";

export default function LoginRoute() {
  return <LoginPage />;
}

