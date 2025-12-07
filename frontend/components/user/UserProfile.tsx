"use client";

import { useState, useEffect } from "react";
import { authClient } from "@/lib/auth/core/client";
import type { User } from "@/lib/types";

export function UserProfile() {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    try {
      const session = await authClient.getSession();
      if (session?.data?.user) {
        setUser({
          id: session.data.user.id,
          email: session.data.user.email || "",
          name: session.data.user.name || undefined,
          image: session.data.user.image || undefined,
        });
      }
    } catch (error) {
      console.error("Error loading user:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleLogout = async () => {
    setIsLoggingOut(true);
    try {
      // Sign out from Better Auth
      await authClient.signOut();

      // Clear any local state
      setUser(null);

      // Force a hard redirect to login page to clear any cached state
      // Using window.location ensures a full page reload and clears all cookies/cache
      window.location.href = "/login";
    } catch (error) {
      console.error("Error signing out:", error);
      // Even if signOut fails, redirect to login
      window.location.href = "/login";
    } finally {
      setIsLoggingOut(false);
    }
  };

  if (isLoading) {
    return (
      <div className="flex items-center gap-2">
        <div className="h-8 w-8 rounded-full bg-gray-300 animate-pulse" />
        <div className="h-4 w-20 bg-gray-300 animate-pulse rounded" />
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="flex items-center gap-3">
      {/* User Avatar */}
      {user.image ? (
        <img
          src={user.image}
          alt={user.name || user.email}
          className="h-8 w-8 rounded-full border-2 border-gray-400"
        />
      ) : (
        <div className="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center text-white font-semibold text-sm border-2 border-gray-400">
          {(user.name || user.email || "U").charAt(0).toUpperCase()}
        </div>
      )}

      {/* User Name/Email */}
      <div className="flex flex-col">
        <span className="text-sm font-semibold text-gray-900">
          {user.name || user.email.split("@")[0]}
        </span>
        <span className="text-xs text-gray-600">{user.email}</span>
      </div>

      {/* Logout Button */}
      <button
        onClick={handleLogout}
        disabled={isLoggingOut}
        className="px-3 py-1 text-sm font-semibold text-red-700 hover:text-red-900 hover:bg-red-50 rounded border border-red-300 disabled:opacity-50"
      >
        {isLoggingOut ? "Logging out..." : "Logout"}
      </button>
    </div>
  );
}
