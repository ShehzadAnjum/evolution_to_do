"use client";

import { useState, useEffect } from "react";
import { AuthForm, type AuthMode } from "../components/AuthForm";
import { SocialButtons } from "../components/SocialButtons";
import { authClient } from "../../core/client";
import { useRouter, useSearchParams } from "next/navigation";
import { APP_VERSION } from "@/lib/version";

/**
 * LoginPage Component
 *
 * Complete login/register page with:
 * - Email/password authentication
 * - Mode switching (login ↔ register)
 * - Error handling
 * - Loading states
 * - Futuristic design
 * - Redirect parameter support (from middleware)
 *
 * This component handles the authentication flow and redirects
 * users after successful authentication.
 */
export function LoginPage() {
  const [mode, setMode] = useState<AuthMode>("login");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();
  const searchParams = useSearchParams();

  // Get redirect URL from query params (set by middleware) or default to /tasks
  const redirectTo = searchParams.get("redirect") || "/tasks";

  const handleSubmit = async (data: { email: string; password: string }) => {
    setIsLoading(true);
    setError(null);

    try {
      if (mode === "login") {
        // Sign in
        const result = await authClient.signIn.email({
          email: data.email,
          password: data.password,
        });

        if (result.error) {
          setError(result.error.message || "Failed to sign in");
          return;
        }

        // Redirect on success (use redirect param or default)
        router.push(redirectTo);
        router.refresh();
      } else {
        // Sign up
        const result = await authClient.signUp.email({
          email: data.email,
          password: data.password,
          name: data.email.split("@")[0], // Use email prefix as default name
        });

        if (result.error) {
          setError(result.error.message || "Failed to create account");
          return;
        }

        // After sign up, automatically sign in
        const signInResult = await authClient.signIn.email({
          email: data.email,
          password: data.password,
        });

        if (signInResult.error) {
          setError("Account created but sign in failed. Please try signing in.");
          setMode("login");
          return;
        }

        // Redirect on success (use redirect param or default)
        router.push(redirectTo);
        router.refresh();
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "An unexpected error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-background via-background to-primary/5 p-4">
      <div className="w-full max-w-md">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent">
            Better Auth
          </h1>
          <p className="text-muted-foreground">
            Secure authentication for modern applications
          </p>
        </div>

        <AuthForm
          mode={mode}
          onModeChange={setMode}
          onSubmit={handleSubmit}
          isLoading={isLoading}
          error={error}
        />

        <SocialButtons
          className="mt-6"
          onSuccess={() => {
            setError(null);
            router.push(redirectTo);
            router.refresh();
          }}
          onError={(err) => setError(err)}
        />

        <div className="mt-6 text-center text-xs text-muted-foreground">
          By continuing, you agree to our Terms of Service and Privacy Policy
        </div>
      </div>

      {/* Version display - bottom right */}
      <div className="fixed bottom-4 right-4 text-xs text-muted-foreground/60 font-mono">
        v{APP_VERSION}
      </div>
    </div>
  );
}

