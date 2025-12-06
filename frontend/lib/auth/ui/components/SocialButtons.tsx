"use client";

import { Button } from "@/components/ui/button";
import { authClient } from "../../core/client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export interface SocialButtonsProps {
  className?: string;
  onSuccess?: () => void;
  onError?: (error: string) => void;
}

/**
 * SocialButtons Component
 * 
 * Provides social authentication buttons (Google OAuth, etc.)
 * Features:
 * - Google OAuth sign-in
 * - Loading states
 * - Error handling
 * - Futuristic design with brand colors
 * 
 * @example
 * ```tsx
 * <SocialButtons
 *   onSuccess={() => router.push('/dashboard')}
 *   onError={(error) => setError(error)}
 * />
 * ```
 */
export function SocialButtons({ className, onSuccess, onError }: SocialButtonsProps) {
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleGoogleSignIn = async () => {
    setIsLoading(true);
    try {
      // Better-Auth social sign-in redirects to OAuth provider
      // The redirect URL is handled by Better-Auth automatically
      const result = await authClient.signIn.social({
        provider: "google",
        callbackURL: "/dashboard",
      });

      // If there's an error, handle it
      if (result?.error) {
        onError?.(result.error.message || "Failed to sign in with Google");
        setIsLoading(false);
        return;
      }

      // If successful, Better-Auth will redirect automatically
      // The callback will handle the redirect to /dashboard
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "An unexpected error occurred";
      onError?.(errorMessage);
      setIsLoading(false);
    }
    // Note: Don't set loading to false on success - redirect will happen
  };

  return (
    <div className={className}>
      <div className="relative">
        <div className="absolute inset-0 flex items-center">
          <span className="w-full border-t border-border" />
        </div>
        <div className="relative flex justify-center text-xs uppercase">
          <span className="bg-card px-2 text-muted-foreground">Or continue with</span>
        </div>
      </div>

      <Button
        type="button"
        variant="outline"
        onClick={handleGoogleSignIn}
        disabled={isLoading}
        className="w-full mt-4 border-accent/20 hover:border-accent/40 hover:bg-accent/5 transition-all"
      >
        {isLoading ? (
          <span className="flex items-center gap-2">
            <span className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
            Connecting...
          </span>
        ) : (
          <span className="flex items-center gap-2">
            <svg className="h-5 w-5" viewBox="0 0 24 24">
              <path
                fill="currentColor"
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
              />
              <path
                fill="currentColor"
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
              />
              <path
                fill="currentColor"
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
              />
              <path
                fill="currentColor"
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
              />
            </svg>
            Continue with Google
          </span>
        )}
      </Button>
    </div>
  );
}

