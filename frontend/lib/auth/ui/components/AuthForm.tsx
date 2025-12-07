"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { cn } from "@/lib/utils";

export type AuthMode = "login" | "register";

export interface AuthFormProps {
  mode?: AuthMode;
  onModeChange?: (mode: AuthMode) => void;
  onSubmit?: (data: { email: string; password: string }) => Promise<void>;
  isLoading?: boolean;
  error?: string | null;
  className?: string;
}

/**
 * AuthForm Component
 * 
 * Reusable authentication form component supporting both login and registration.
 * Features:
 * - Email and password fields
 * - Mode switching (login/register)
 * - Loading states
 * - Error handling
 * - Futuristic design with brand colors
 * 
 * @example
 * ```tsx
 * <AuthForm
 *   mode="login"
 *   onSubmit={async (data) => {
 *     await signIn(data.email, data.password);
 *   }}
 * />
 * ```
 */
export function AuthForm({
  mode = "login",
  onModeChange,
  onSubmit,
  isLoading = false,
  error = null,
  className,
}: AuthFormProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [localError, setLocalError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLocalError(null);

    // Basic validation
    if (!email || !email.includes("@")) {
      setLocalError("Please enter a valid email address");
      return;
    }

    if (!password || password.length < 6) {
      setLocalError("Password must be at least 6 characters");
      return;
    }

    try {
      await onSubmit?.({ email, password });
    } catch (err) {
      setLocalError(err instanceof Error ? err.message : "An error occurred");
    }
  };

  const displayError = error || localError;
  const isLogin = mode === "login";

  return (
    <Card className={cn("w-full max-w-md border-accent/20 shadow-lg shadow-accent/5", className)}>
      <CardHeader className="space-y-1">
        <CardTitle className="text-2xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
          {isLogin ? "Welcome Back" : "Create Account"}
        </CardTitle>
        <CardDescription className="text-muted-foreground">
          {isLogin
            ? "Sign in to your account to continue"
            : "Enter your details to create a new account"}
        </CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          {displayError && (
            <div className="rounded-md bg-destructive/10 border border-destructive/20 p-3 text-sm text-destructive">
              {displayError}
            </div>
          )}

          <div className="space-y-2">
            <Label htmlFor="email" className="text-foreground">
              Email
            </Label>
            <Input
              id="email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={isLoading}
              required
              className="border-input focus-visible:ring-accent/50"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="password" className="text-foreground">
              Password
            </Label>
            <Input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={isLoading}
              required
              minLength={6}
              className="border-input focus-visible:ring-accent/50"
            />
          </div>
        </CardContent>

        <CardFooter className="flex flex-col space-y-4">
          <Button
            type="submit"
            disabled={isLoading}
            className="w-full bg-gradient-to-r from-primary to-primary/80 hover:from-primary/90 hover:to-primary/70 text-primary-foreground shadow-lg shadow-primary/20"
          >
            {isLoading ? (
              <span className="flex items-center gap-2">
                <span className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
                {isLogin ? "Signing in..." : "Creating account..."}
              </span>
            ) : (
              isLogin ? "Sign In" : "Create Account"
            )}
          </Button>

          {onModeChange && (
            <div className="text-center text-sm text-muted-foreground">
              {isLogin ? "Don't have an account? " : "Already have an account? "}
              <button
                type="button"
                onClick={() => onModeChange?.(isLogin ? "register" : "login")}
                className="text-accent hover:text-accent/80 underline underline-offset-4 transition-colors"
                disabled={isLoading}
              >
                {isLogin ? "Sign up" : "Sign in"}
              </button>
            </div>
          )}
        </CardFooter>
      </form>
    </Card>
  );
}




