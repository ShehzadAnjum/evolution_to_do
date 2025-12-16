"use client";

import { useState, useEffect, useCallback } from "react";
import {
  MainContainer,
  Sidebar,
  ConversationList,
  Conversation,
  ChatContainer,
  MessageList,
  Message,
  TypingIndicator,
  ConversationHeader,
  Avatar,
} from "@chatscope/chat-ui-kit-react";
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import { getAuthToken } from "@/lib/auth-token";
import { MessageInput } from "./message-input";
import type {
  ChatMessage,
  ChatResponse,
  ConversationSummary,
  ConversationListResponse,
  ConversationDetailResponse,
} from "@/lib/chat/types";

interface ChatKitInterfaceProps {
  initialConversationId?: string;
}

export function ChatKitInterface({ initialConversationId }: ChatKitInterfaceProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversations, setConversations] = useState<ConversationSummary[]>([]);
  const [activeConversationId, setActiveConversationId] = useState<string | undefined>(
    initialConversationId
  );
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingConversations, setIsLoadingConversations] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sidebarVisible, setSidebarVisible] = useState(true);

  // Load conversations on mount
  useEffect(() => {
    loadConversations();
  }, []);

  // Load messages when active conversation changes
  useEffect(() => {
    if (activeConversationId) {
      loadConversationMessages(activeConversationId);
    } else {
      setMessages([]);
    }
  }, [activeConversationId]);

  const loadConversations = async () => {
    try {
      setIsLoadingConversations(true);
      const token = await getAuthToken();
      if (!token) return;

      const response = await fetch("/api/chat/conversations", {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (response.ok) {
        const data: ConversationListResponse = await response.json();
        setConversations(data.conversations || []);
      }
    } catch (err) {
      console.error("Failed to load conversations:", err);
    } finally {
      setIsLoadingConversations(false);
    }
  };

  const loadConversationMessages = async (conversationId: string) => {
    try {
      setIsLoading(true);
      const token = await getAuthToken();
      if (!token) return;

      const response = await fetch(`/api/chat/conversations/${conversationId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (response.ok) {
        const data: ConversationDetailResponse = await response.json();
        setMessages(data.messages || []);
      }
    } catch (err) {
      console.error("Failed to load messages:", err);
    } finally {
      setIsLoading(false);
    }
  };

  const sendMessage = useCallback(
    async (text: string) => {
      if (!text.trim()) return;

      // Add user message to UI immediately
      const userMessage: ChatMessage = {
        id: `temp-${Date.now()}`,
        role: "user",
        content: text,
        created_at: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, userMessage]);
      setIsLoading(true);
      setError(null);

      try {
        const token = await getAuthToken();
        if (!token) {
          throw new Error("Please log in to use the chat assistant.");
        }

        const response = await fetch("/api/chat", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            message: text,
            conversation_id: activeConversationId,
          }),
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.message || `Error: ${response.statusText}`);
        }

        const data: ChatResponse = await response.json();

        // Update conversation ID if this is a new conversation
        if (!activeConversationId && data.conversation_id) {
          setActiveConversationId(data.conversation_id);
          // Refresh conversation list
          loadConversations();
        }

        // Add assistant message
        const assistantMessage: ChatMessage = {
          id: `msg-${Date.now()}`,
          role: "assistant",
          content: data.message,
          tool_calls: data.tool_results?.map((tr, i) => ({
            id: `tc-${i}`,
            name: tr.tool,
            arguments: tr.result || {},
          })),
          created_at: new Date().toISOString(),
          response_language: data.response_language,
        };
        setMessages((prev) => [...prev, assistantMessage]);
      } catch (err) {
        const errorMessage =
          err instanceof Error ? err.message : "Failed to send message";
        setError(errorMessage);
        // Remove the optimistic user message on error
        setMessages((prev) => prev.slice(0, -1));
      } finally {
        setIsLoading(false);
      }
    },
    [activeConversationId]
  );

  const startNewConversation = () => {
    setActiveConversationId(undefined);
    setMessages([]);
  };

  const formatTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  };

  const formatDateTime = (dateString: string) => {
    const date = new Date(dateString);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    const isToday = date.toDateString() === today.toDateString();
    const isYesterday = date.toDateString() === yesterday.toDateString();

    if (isToday) {
      return `Today ${formatTime(dateString)}`;
    } else if (isYesterday) {
      return `Yesterday ${formatTime(dateString)}`;
    } else {
      return date.toLocaleDateString([], {
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit"
      });
    }
  };

  const getConversationTitle = (conv: ConversationSummary) => {
    return conv.title || `Chat ${formatDateTime(conv.updated_at || conv.created_at)}`;
  };

  // Dark mode CSS for ChatKit
  const darkModeStyles = `
    /* Dark mode overrides for ChatKit */
    .dark .chatkit-dark-mode .cs-main-container,
    .dark .chatkit-dark-mode .cs-chat-container,
    .dark .chatkit-dark-mode .cs-message-list,
    .dark .chatkit-dark-mode .cs-sidebar,
    .dark .chatkit-dark-mode .cs-conversation-list,
    .dark .chatkit-dark-mode .cs-conversation-header {
      background-color: hsl(var(--background)) !important;
    }
    .dark .chatkit-dark-mode .cs-conversation {
      background-color: hsl(var(--card)) !important;
    }
    .dark .chatkit-dark-mode .cs-conversation:hover,
    .dark .chatkit-dark-mode .cs-conversation--active {
      background-color: hsl(var(--secondary)) !important;
    }
    .dark .chatkit-dark-mode .cs-conversation__name,
    .dark .chatkit-dark-mode .cs-conversation__info,
    .dark .chatkit-dark-mode .cs-conversation-header__user-name,
    .dark .chatkit-dark-mode .cs-conversation-header__info {
      color: hsl(var(--foreground)) !important;
    }
    .dark .chatkit-dark-mode .cs-message__content {
      background-color: hsl(var(--secondary)) !important;
      color: hsl(var(--foreground)) !important;
    }
    .dark .chatkit-dark-mode .cs-message--outgoing .cs-message__content {
      background-color: hsl(var(--primary)) !important;
      color: hsl(var(--primary-foreground)) !important;
    }
    .dark .chatkit-dark-mode .cs-typing-indicator__dot {
      background-color: hsl(var(--muted-foreground)) !important;
    }
    .dark .chatkit-dark-mode .cs-typing-indicator__text {
      color: hsl(var(--muted-foreground)) !important;
    }
    /* Message header (sender name) */
    .chatkit-dark-mode .cs-message__sender-name {
      font-size: 11px !important;
      margin-bottom: 2px !important;
    }
    .dark .chatkit-dark-mode .cs-message__sender-name {
      color: hsl(var(--muted-foreground)) !important;
    }
    /* Message sent time */
    .chatkit-dark-mode .cs-message__sent-time {
      font-size: 10px !important;
      opacity: 0.7;
    }
    .dark .chatkit-dark-mode .cs-message__sent-time {
      color: hsl(var(--muted-foreground)) !important;
    }
    /* Sidebar button styling */
    .dark .chatkit-dark-mode button {
      background-color: hsl(var(--primary)) !important;
    }
  `;

  return (
    <div className="chatkit-dark-mode flex flex-col" style={{ height: "600px", maxHeight: "80vh" }}>
      <style dangerouslySetInnerHTML={{ __html: darkModeStyles }} />
      <div className="flex-1 overflow-hidden">
        <MainContainer>
        {/* Sidebar with conversation list */}
        <Sidebar position="left" scrollable>
          <div style={{ padding: "10px" }}>
            <button
              onClick={startNewConversation}
              style={{
                width: "100%",
                padding: "10px",
                marginBottom: "10px",
                backgroundColor: "var(--primary)",
                color: "white",
                border: "none",
                borderRadius: "6px",
                cursor: "pointer",
                fontWeight: 500,
              }}
            >
              + New Chat
            </button>
          </div>
          <ConversationList loading={isLoadingConversations}>
            {conversations.map((conv) => (
              <Conversation
                key={conv.id}
                name={getConversationTitle(conv)}
                info={`${conv.message_count || 0} messages`}
                active={conv.id === activeConversationId}
                onClick={() => setActiveConversationId(conv.id)}
              >
                <Avatar name={getConversationTitle(conv).charAt(0)} />
              </Conversation>
            ))}
          </ConversationList>
        </Sidebar>

        {/* Main chat area */}
        <ChatContainer>
          <ConversationHeader>
            <ConversationHeader.Content
              userName="Task Assistant"
              info={activeConversationId ? "Chat with AI" : "Start a new conversation"}
            />
          </ConversationHeader>

          {/* Error banner */}
          {error && (
            <div
              style={{
                backgroundColor: "#fee2e2",
                borderBottom: "1px solid #fecaca",
                padding: "8px 16px",
                color: "#dc2626",
                fontSize: "14px",
              }}
            >
              {error}
              <button
                onClick={() => setError(null)}
                style={{
                  marginLeft: "8px",
                  textDecoration: "underline",
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                  color: "inherit",
                }}
              >
                Dismiss
              </button>
            </div>
          )}

          <MessageList
            typingIndicator={
              isLoading ? <TypingIndicator content="AI is thinking..." /> : null
            }
          >
            {messages.length === 0 && !isLoading && (
              <Message
                model={{
                  message:
                    "Hello! I'm your task assistant. Ask me to add, list, complete, or delete tasks. I also speak Urdu! آپ اردو میں بھی بات کر سکتے ہیں۔",
                  sender: "Assistant",
                  direction: "incoming",
                  position: "single",
                }}
              />
            )}
            {messages
              // Filter out tool response messages (they have tool_call_id)
              // and messages that look like raw JSON tool results
              .filter((msg) => {
                // Skip tool response messages
                if (msg.tool_call_id) return false;
                // Skip messages that are raw JSON tool results
                if (msg.content?.startsWith('{"success"')) return false;
                if (msg.content?.startsWith('{"tasks"')) return false;
                return true;
              })
              .map((msg) => (
              <Message
                key={msg.id}
                model={{
                  message: msg.content,
                  sender: msg.role === "user" ? "You" : "AI",
                  direction: msg.role === "user" ? "outgoing" : "incoming",
                  position: "single",
                  sentTime: formatDateTime(msg.created_at),
                }}
              >
                {msg.role === "assistant" && (
                  <Avatar name="AI" />
                )}
              </Message>
            ))}
          </MessageList>
        </ChatContainer>
        </MainContainer>
      </div>

      {/* Custom input with voice support */}
      <MessageInput
        onSend={sendMessage}
        disabled={isLoading}
        placeholder="Ask me to manage your tasks..."
      />
    </div>
  );
}
