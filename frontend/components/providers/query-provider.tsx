"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState, useEffect } from "react";

// Create a client with good defaults for chat caching
function makeQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: {
        // Show stale data immediately, refetch in background
        staleTime: 1000 * 60 * 5, // 5 minutes before data is considered stale
        gcTime: 1000 * 60 * 30, // 30 minutes cache retention (formerly cacheTime)
        refetchOnWindowFocus: false, // Don't refetch on every tab switch
        refetchOnMount: true, // Refetch when component mounts
        retry: 1, // Only retry once on failure
      },
    },
  });
}

let browserQueryClient: QueryClient | undefined = undefined;

function getQueryClient() {
  if (typeof window === "undefined") {
    // Server: always make a new query client
    return makeQueryClient();
  } else {
    // Browser: make a new query client if we don't already have one
    if (!browserQueryClient) browserQueryClient = makeQueryClient();
    return browserQueryClient;
  }
}

// LocalStorage persistence helpers
const CACHE_KEY = "evolution-todo-chat-cache";

function persistCache(client: QueryClient) {
  try {
    const cache = client.getQueryCache().getAll();
    const dataToStore = cache
      .filter(query => query.state.data !== undefined)
      .map(query => ({
        queryKey: query.queryKey,
        data: query.state.data,
        dataUpdatedAt: query.state.dataUpdatedAt,
      }));
    localStorage.setItem(CACHE_KEY, JSON.stringify(dataToStore));
  } catch (e) {
    console.warn("Failed to persist query cache:", e);
  }
}

function restoreCache(client: QueryClient) {
  try {
    const cached = localStorage.getItem(CACHE_KEY);
    if (cached) {
      const data = JSON.parse(cached);
      data.forEach((item: { queryKey: unknown[]; data: unknown; dataUpdatedAt: number }) => {
        // Only restore if cache is less than 30 minutes old
        const age = Date.now() - item.dataUpdatedAt;
        if (age < 1000 * 60 * 30) {
          client.setQueryData(item.queryKey, item.data);
        }
      });
    }
  } catch (e) {
    console.warn("Failed to restore query cache:", e);
  }
}

export function QueryProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(getQueryClient);

  // Restore cache from localStorage on mount
  useEffect(() => {
    restoreCache(queryClient);

    // Persist cache periodically and on page unload
    const interval = setInterval(() => persistCache(queryClient), 30000); // Every 30s

    const handleBeforeUnload = () => persistCache(queryClient);
    window.addEventListener("beforeunload", handleBeforeUnload);

    return () => {
      clearInterval(interval);
      window.removeEventListener("beforeunload", handleBeforeUnload);
      persistCache(queryClient); // Persist on unmount too
    };
  }, [queryClient]);

  return (
    <QueryClientProvider client={queryClient}>
      {children}
    </QueryClientProvider>
  );
}
