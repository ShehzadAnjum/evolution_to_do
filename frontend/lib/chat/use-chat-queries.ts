"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getAuthToken } from "@/lib/auth-token";
import type {
  ConversationSummary,
  ConversationListResponse,
  ConversationDetailResponse,
  ChatMessage,
} from "./types";

// Query keys for cache management
export const chatKeys = {
  all: ["chat"] as const,
  conversations: () => [...chatKeys.all, "conversations"] as const,
  conversation: (id: string) => [...chatKeys.all, "conversation", id] as const,
};

// Fetch all conversations
async function fetchConversations(): Promise<ConversationSummary[]> {
  const token = await getAuthToken();
  if (!token) throw new Error("Not authenticated");

  const response = await fetch("/api/chat/conversations?limit=100", {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch conversations");
  }

  const data: ConversationListResponse = await response.json();
  return data.conversations || [];
}

// Fetch single conversation messages
async function fetchConversationMessages(conversationId: string): Promise<ChatMessage[]> {
  const token = await getAuthToken();
  if (!token) throw new Error("Not authenticated");

  const response = await fetch(`/api/chat/conversations/${conversationId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!response.ok) {
    throw new Error("Failed to fetch conversation messages");
  }

  const data: ConversationDetailResponse = await response.json();

  // Filter out tool messages
  return (data.messages || []).filter(msg => {
    if (msg.tool_call_id) return false;
    if (msg.content?.startsWith('{"success"')) return false;
    if (msg.content?.startsWith('{"tasks"')) return false;
    return true;
  });
}

// Delete a message
async function deleteMessage(conversationId: string, messageId: string): Promise<void> {
  const token = await getAuthToken();
  if (!token) throw new Error("Not authenticated");

  const response = await fetch(`/api/chat/conversations/${conversationId}/messages/${messageId}`, {
    method: "DELETE",
    headers: { Authorization: `Bearer ${token}` },
  });

  if (!response.ok) {
    throw new Error("Failed to delete message");
  }
}

// Hook: Get all conversations with caching
export function useConversations() {
  return useQuery({
    queryKey: chatKeys.conversations(),
    queryFn: fetchConversations,
    staleTime: 1000 * 60 * 2, // 2 minutes
  });
}

// Hook: Get conversation messages with caching
export function useConversationMessages(conversationId: string | null) {
  return useQuery({
    queryKey: chatKeys.conversation(conversationId || ""),
    queryFn: () => fetchConversationMessages(conversationId!),
    enabled: !!conversationId, // Only fetch if we have an ID
    staleTime: 1000 * 60 * 2, // 2 minutes
  });
}

// Hook: Prefetch conversation messages (for eager loading)
export function usePrefetchConversation() {
  const queryClient = useQueryClient();

  return (conversationId: string) => {
    queryClient.prefetchQuery({
      queryKey: chatKeys.conversation(conversationId),
      queryFn: () => fetchConversationMessages(conversationId),
      staleTime: 1000 * 60 * 2,
    });
  };
}

// Hook: Delete message mutation
export function useDeleteMessage() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ conversationId, messageId }: { conversationId: string; messageId: string }) =>
      deleteMessage(conversationId, messageId),
    onSuccess: (_, { conversationId, messageId }) => {
      // Update cache optimistically
      queryClient.setQueryData<ChatMessage[]>(
        chatKeys.conversation(conversationId),
        (old) => old?.filter(m => m.id !== messageId)
      );
    },
  });
}

// Hook: Add messages to conversation cache (after sending)
export function useAddMessagesToCache() {
  const queryClient = useQueryClient();

  return (conversationId: string, messages: ChatMessage[]) => {
    queryClient.setQueryData<ChatMessage[]>(
      chatKeys.conversation(conversationId),
      (old) => [...(old || []), ...messages]
    );
  };
}

// Hook: Invalidate all chat data (force refetch)
export function useInvalidateChat() {
  const queryClient = useQueryClient();

  return () => {
    queryClient.invalidateQueries({ queryKey: chatKeys.all });
  };
}

// Hook: Refetch conversations
export function useRefetchConversations() {
  const queryClient = useQueryClient();

  return () => {
    queryClient.invalidateQueries({ queryKey: chatKeys.conversations() });
  };
}
