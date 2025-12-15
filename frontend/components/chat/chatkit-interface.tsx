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
  MessageInput,
  TypingIndicator,
  ConversationHeader,
  Avatar,
} from "@chatscope/chat-ui-kit-react";
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
import { getAuthToken } from "@/lib/auth-token";
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

  const getConversationTitle = (conv: ConversationSummary) => {
    return conv.title || `Chat ${formatTime(conv.created_at)}`;
  };

  return (
    <div style={{ height: "600px", maxHeight: "80vh" }}>
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
            {messages.map((msg, index) => (
              <Message
                key={msg.id}
                model={{
                  message: msg.content,
                  sender: msg.role === "user" ? "You" : "Assistant",
                  direction: msg.role === "user" ? "outgoing" : "incoming",
                  position: "single",
                  sentTime: formatTime(msg.created_at),
                }}
              >
                {msg.role === "assistant" && (
                  <Avatar name="AI" />
                )}
              </Message>
            ))}
          </MessageList>

          <MessageInput
            placeholder="Ask me to manage your tasks..."
            onSend={sendMessage}
            disabled={isLoading}
            attachButton={false}
          />
        </ChatContainer>
      </MainContainer>
    </div>
  );
}
