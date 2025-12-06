"use client";

import { Button } from "@/components/ui/button";
import { authClient } from "@/lib/auth/core/client";

/**
 * Sign Out Button Component
 * 
 * Client component for sign-out functionality.
 * Must be a separate file with "use client" directive.
 */
export function SignOutButton() {
  const handleSignOut = async () => {
    try {
      await authClient.signOut();
      window.location.href = "/login";
    } catch (error) {
      console.error("Sign out error:", error);
      // Force redirect even if sign out fails
      window.location.href = "/login";
    }
  };

  return (
    <Button
      onClick={handleSignOut}
      variant="outline"
      className="w-full border-destructive/20 hover:border-destructive/40 hover:bg-destructive/5"
    >
      Sign Out
    </Button>
  );
}




