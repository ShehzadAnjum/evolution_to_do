/**
 * Chat API client for Phase III AI Chatbot.
 *
 * This module provides functions for interacting with the chat API endpoints.
 */

import type {
  ChatRequest,
  ChatResponse,
  ConversationDetailResponse,
  ConversationListResponse,
} from "./types";

/**
 * Base URL for the API.
 * In production, this will be the backend URL.
 * In development, we proxy through Next.js API routes.
 */
const API_BASE = "/api/chat";

/**
 * Send a message to the AI assistant.
 *
 * @param request - The chat request with message and optional conversation_id
 * @returns The chat response with AI message and any tool results
 */
export async function sendMessage(request: ChatRequest): Promise<ChatResponse> {
  const response = await fetch(API_BASE, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(request),
    credentials: "include", // Include cookies for auth
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Failed to send message");
  }

  return response.json();
}

/**
 * List user's conversations.
 *
 * @param limit - Maximum number of conversations to return (default: 20)
 * @param offset - Number of conversations to skip (default: 0)
 * @returns List of conversations with total count
 */
export async function listConversations(
  limit: number = 20,
  offset: number = 0
): Promise<ConversationListResponse> {
  const params = new URLSearchParams({
    limit: limit.toString(),
    offset: offset.toString(),
  });

  const response = await fetch(`${API_BASE}/conversations?${params}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Failed to list conversations");
  }

  return response.json();
}

/**
 * Get a specific conversation with its messages.
 *
 * @param conversationId - UUID of the conversation
 * @returns Conversation details with messages
 */
export async function getConversation(
  conversationId: string
): Promise<ConversationDetailResponse> {
  const response = await fetch(`${API_BASE}/conversations/${conversationId}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Failed to get conversation");
  }

  return response.json();
}

/**
 * Delete a conversation.
 *
 * @param conversationId - UUID of the conversation to delete
 * @returns Success response
 */
export async function deleteConversation(
  conversationId: string
): Promise<{ success: boolean; message: string }> {
  const response = await fetch(`${API_BASE}/conversations/${conversationId}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.message || "Failed to delete conversation");
  }

  return response.json();
}
