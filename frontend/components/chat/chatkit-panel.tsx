"use client";

import { useState, useCallback, useEffect, useRef, useImperativeHandle, forwardRef } from "react";
import { useQueryClient } from "@tanstack/react-query";
import { getAuthToken } from "@/lib/auth-token";
import { speak, mapLanguageForTTS } from "@/lib/voice/api";
import { MessageInput, MessageInputRef } from "./message-input";
import {
  useConversations,
  useConversationMessages,
  useDeleteMessage,
  usePrefetchConversation,
  chatKeys,
} from "@/lib/chat/use-chat-queries";
import type {
  ChatMessage,
  ChatResponse,
} from "@/lib/chat/types";

interface ChatKitPanelProps {
  isOpen: boolean;
  onClose: () => void;
  onTasksChanged?: () => void;
  preloadOnMount?: boolean;
  onLoadingChange?: (isLoading: boolean) => void;
}

// Export a ref type for external preloading
export interface ChatKitPanelRef {
  preload: () => void;
}

export const ChatKitPanel = forwardRef<ChatKitPanelRef, ChatKitPanelProps>(
  function ChatKitPanel({ isOpen, onClose, onTasksChanged, preloadOnMount = false, onLoadingChange }, ref) {
  const queryClient = useQueryClient();

  // React Query hooks for data fetching with caching
  const {
    data: conversations = [],
    isLoading: isLoadingConversations,
    refetch: refetchConversations,
  } = useConversations();

  // UI state - which conversations are expanded (IDs only)
  const [expandedIds, setExpandedIds] = useState<Set<string>>(new Set());
  const [activeConversationId, setActiveConversationId] = useState<string | undefined>();

  // Local message overrides (for optimistic updates and temp messages)
  const [localMessages, setLocalMessages] = useState<Record<string, ChatMessage[]>>({});

  // Other state
  const [isLoading, setIsLoading] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [deleteConfirm, setDeleteConfirm] = useState<{ conversationId: string; messageId: string; content: string } | null>(null);

  // Refs
  const messageInputRef = useRef<MessageInputRef>(null);
  const shouldSpeakRef = useRef(false);
  const hasAutoExpandedRef = useRef(false);

  // Prefetch hook for eager loading
  const prefetchConversation = usePrefetchConversation();

  // Delete mutation
  const deleteMessageMutation = useDeleteMessage();

  // Expose preload method to parent
  useImperativeHandle(ref, () => ({
    preload: () => {
      refetchConversations();
    }
  }));

  // Notify parent about loading state changes
  useEffect(() => {
    if (onLoadingChange) {
      onLoadingChange(isLoadingConversations);
    }
  }, [isLoadingConversations, onLoadingChange]);

  // Auto-expand most recent conversation when conversations load
  useEffect(() => {
    if (!hasAutoExpandedRef.current && conversations.length > 0 && !isLoadingConversations) {
      const mostRecent = conversations[0];
      setActiveConversationId(mostRecent.id);
      setExpandedIds(new Set([mostRecent.id]));
      // Prefetch the messages
      prefetchConversation(mostRecent.id);
      hasAutoExpandedRef.current = true;
    }
  }, [conversations, isLoadingConversations, prefetchConversation]);

  // Toggle conversation expansion
  const toggleConversation = (conversationId: string) => {
    setExpandedIds(prev => {
      const newSet = new Set(prev);
      if (newSet.has(conversationId)) {
        newSet.delete(conversationId);
        if (activeConversationId === conversationId) {
          setActiveConversationId(undefined);
        }
      } else {
        newSet.add(conversationId);
        setActiveConversationId(conversationId);
        // Prefetch when expanding
        prefetchConversation(conversationId);
      }
      return newSet;
    });
  };

  const sendMessage = useCallback(
    async (text: string) => {
      if (!text.trim()) return;

      shouldSpeakRef.current = true;
      setIsLoading(true);
      setError(null);

      // Create optimistic user message immediately
      const tempUserMessageId = `temp-user-${Date.now()}`;
      const userMessage: ChatMessage = {
        id: tempUserMessageId,
        role: "user",
        content: text,
        created_at: new Date().toISOString(),
      };

      // Add user message immediately to show it right away
      if (activeConversationId) {
        setLocalMessages(prev => ({
          ...prev,
          [activeConversationId]: [...(prev[activeConversationId] || []), userMessage]
        }));
      }

      try {
        const token = await getAuthToken();
        if (!token) {
          throw new Error("Please log in to use the chat assistant.");
        }

        // Collect context messages from all expanded conversations
        const contextMessages: { role: string; content: string }[] = [];
        for (const convId of expandedIds) {
          const cachedMessages = queryClient.getQueryData<ChatMessage[]>(chatKeys.conversation(convId));
          const local = localMessages[convId] || [];
          const allMsgs = [...(cachedMessages || []), ...local];
          allMsgs.forEach((msg) => {
            if (msg.role === "user" || msg.role === "assistant") {
              contextMessages.push({
                role: msg.role,
                content: msg.content,
              });
            }
          });
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
            context_messages: contextMessages.length > 0 ? contextMessages : undefined,
          }),
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.message || `Error: ${response.statusText}`);
        }

        const data: ChatResponse = await response.json();

        // If new conversation, reload list and expand it
        if (!activeConversationId && data.conversation_id) {
          setActiveConversationId(data.conversation_id);
          await refetchConversations();
          setExpandedIds(prev => new Set([...prev, data.conversation_id!]));
          // Invalidate to load the new conversation messages
          queryClient.invalidateQueries({ queryKey: chatKeys.conversation(data.conversation_id) });
        } else if (activeConversationId) {
          // Add assistant response to local state
          const assistantMessage: ChatMessage = {
            id: `temp-ai-${Date.now()}`,
            role: "assistant",
            content: data.message,
            created_at: new Date().toISOString(),
          };

          setLocalMessages(prev => ({
            ...prev,
            [activeConversationId]: [...(prev[activeConversationId] || []), assistantMessage]
          }));
        }

        // Auto-play TTS if enabled
        if (voiceEnabled && shouldSpeakRef.current && data.message) {
          const ttsLanguage = mapLanguageForTTS(data.response_language);
          setIsSpeaking(true);
          try {
            await speak(data.message, ttsLanguage);
          } catch (ttsError) {
            console.warn("TTS playback failed:", ttsError);
          } finally {
            setIsSpeaking(false);
          }
        }

        // Refresh task list if any task-related tool was called
        if (data.tool_results && data.tool_results.length > 0 && onTasksChanged) {
          const taskTools = ["add_task", "update_task", "delete_task", "complete_task", "clear_completed_tasks", "schedule_device", "control_device"];
          const hasTaskChange = data.tool_results.some((tr) => taskTools.includes(tr.tool));
          if (hasTaskChange) {
            onTasksChanged();
          }
        }
      } catch (err) {
        let errorMessage = err instanceof Error ? err.message : "Failed to send message";
        if (errorMessage.includes("Method Not Allowed") || errorMessage.includes("405")) {
          errorMessage = "Chat service is currently unavailable. Please try again later.";
        } else if (errorMessage.includes("Failed to fetch") || errorMessage.includes("NetworkError")) {
          errorMessage = "Cannot connect to chat service. Please check your connection.";
        }
        setError(errorMessage);
        // Remove optimistic user message on error
        if (activeConversationId) {
          setLocalMessages(prev => ({
            ...prev,
            [activeConversationId]: (prev[activeConversationId] || []).filter(m => m.id !== tempUserMessageId)
          }));
        }
      } finally {
        setIsLoading(false);
      }
    },
    [activeConversationId, expandedIds, voiceEnabled, onTasksChanged, queryClient, localMessages, refetchConversations]
  );

  const startNewConversation = () => {
    setActiveConversationId(undefined);
    setError(null);
    shouldSpeakRef.current = false;
  };

  const toggleVoice = () => {
    setVoiceEnabled((prev) => !prev);
  };

  // Copy message to clipboard and input box
  const handleCopyMessage = async (content: string) => {
    try {
      await navigator.clipboard.writeText(content);
      if (messageInputRef.current) {
        messageInputRef.current.setValue(content);
      }
    } catch (err) {
      console.error("Failed to copy:", err);
    }
  };

  // Delete message with confirmation
  const handleDeleteMessage = async () => {
    if (!deleteConfirm) return;

    const { conversationId, messageId } = deleteConfirm;
    const isTempMessage = messageId.startsWith("temp-");

    setIsDeleting(true);

    if (isTempMessage) {
      // Just remove from local state
      setLocalMessages(prev => ({
        ...prev,
        [conversationId]: (prev[conversationId] || []).filter(m => m.id !== messageId)
      }));
      setDeleteConfirm(null);
      setIsDeleting(false);
      return;
    }

    // Real message - delete via mutation (updates cache automatically)
    try {
      await deleteMessageMutation.mutateAsync({ conversationId, messageId });
      setDeleteConfirm(null);
    } catch (err) {
      console.error("Failed to delete message:", err);
    } finally {
      setIsDeleting(false);
    }
  };

  const formatDateTime = (dateString: string) => {
    const date = new Date(dateString);
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    const isToday = date.toDateString() === today.toDateString();
    const isYesterday = date.toDateString() === yesterday.toDateString();
    const time = date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });

    if (isToday) {
      return `Today ${time}`;
    } else if (isYesterday) {
      return `Yesterday ${time}`;
    } else {
      return date.toLocaleDateString([], {
        month: "short",
        day: "numeric",
        year: date.getFullYear() !== today.getFullYear() ? "numeric" : undefined,
      }) + ` ${time}`;
    }
  };

  const formatMessageTime = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  };

  return (
    <>
      {/* Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black/30 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      {/* Panel - 1.5x wider for better readability */}
      <div
        className={`
          fixed top-0 right-0 h-full w-full sm:w-[576px] lg:w-[630px]
          bg-background border-l border-border
          transform transition-transform duration-300 ease-in-out
          z-50 flex flex-col
          ${isOpen ? "translate-x-0" : "translate-x-full"}
        `}
      >
        {/* Header */}
        <div className="flex-none flex items-center justify-between px-4 h-14 border-b border-border bg-card">
          <div className="flex items-center gap-2">
            <span className="text-xl">🤖</span>
            <h2 className="font-semibold text-foreground">AI Assistant</h2>
            {isSpeaking && (
              <span className="text-xs text-green-500 animate-pulse">🔊</span>
            )}
          </div>
          <div className="flex items-center gap-1">
            <span className="text-xs text-muted-foreground">
              {conversations.length} chats
            </span>
            {/* Voice toggle */}
            <button
              onClick={toggleVoice}
              className={`flex items-center gap-1 px-2 py-1 text-xs rounded-lg transition-colors ${
                voiceEnabled
                  ? "bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400"
                  : "bg-secondary text-muted-foreground hover:text-foreground"
              }`}
              title={voiceEnabled ? "Voice enabled - click to mute" : "Voice muted - click to enable"}
            >
              {voiceEnabled ? "🔊" : "🔇"}
            </button>
            <button
              onClick={startNewConversation}
              className="flex items-center gap-1 px-2 py-1 text-xs hover:bg-secondary rounded-lg text-muted-foreground hover:text-foreground transition-colors"
              title="Start new conversation"
            >
              ✨ New
            </button>
            <button
              onClick={onClose}
              className="p-2 hover:bg-secondary rounded-lg text-muted-foreground hover:text-foreground transition-colors"
              title="Close"
            >
              ✕
            </button>
          </div>
        </div>

        {/* Error banner */}
        {error && (
          <div className="flex-none bg-destructive/10 border-b border-destructive/20 px-4 py-2 text-sm text-destructive">
            {error}
            <button
              onClick={() => setError(null)}
              className="ml-2 underline hover:no-underline"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Conversation List - Scrollable (newest at bottom, closest to input) */}
        <div className="flex-1 overflow-y-auto flex flex-col-reverse">
          {isLoadingConversations && conversations.length === 0 ? (
            <div className="flex items-center justify-center h-32">
              <div className="animate-spin text-2xl">⏳</div>
            </div>
          ) : conversations.length === 0 ? (
            <div className="text-center p-8 text-muted-foreground">
              <div className="text-4xl mb-4">💬</div>
              <p className="text-sm">No conversations yet.</p>
              <p className="text-xs mt-2">Send a message to start chatting!</p>
            </div>
          ) : (
            <div className="divide-y divide-border">
              {/* Reverse order: oldest at top, newest at bottom (close to input) */}
              {[...conversations].reverse().map((conv) => {
                const isExpanded = expandedIds.has(conv.id);
                const isActive = activeConversationId === conv.id;

                return (
                  <div key={conv.id} className={isActive ? "bg-secondary/50" : ""}>
                    {/* Session Header - Clickable */}
                    <button
                      onClick={() => toggleConversation(conv.id)}
                      className={`w-full px-4 py-3 flex items-center justify-between hover:bg-secondary/50 transition-colors text-left ${
                        isExpanded ? "bg-secondary/30" : ""
                      }`}
                    >
                      <div className="flex items-center gap-2 min-w-0">
                        <span className={`transition-transform ${isExpanded ? "rotate-90" : ""}`}>
                          ▶
                        </span>
                        <div className="min-w-0">
                          <div className="font-medium text-sm text-foreground truncate">
                            {formatDateTime(conv.updated_at || conv.created_at)}
                          </div>
                          {conv.title && (
                            <div className="text-xs text-muted-foreground truncate">
                              {conv.title}
                            </div>
                          )}
                        </div>
                      </div>
                      <span className="text-xs text-muted-foreground flex-none ml-2">
                        {conv.message_count || 0} msgs
                      </span>
                    </button>

                    {/* Expanded Messages */}
                    {isExpanded && (
                      <ConversationMessages
                        conversationId={conv.id}
                        localMessages={localMessages[conv.id] || []}
                        onCopy={handleCopyMessage}
                        onDelete={(messageId, content) => setDeleteConfirm({ conversationId: conv.id, messageId, content })}
                        formatMessageTime={formatMessageTime}
                      />
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="flex-none border-t border-border">
          <MessageInput
            ref={messageInputRef}
            onSend={sendMessage}
            disabled={isLoading}
            placeholder={activeConversationId ? "Continue conversation..." : "Start a new conversation..."}
          />
        </div>

        {/* Delete Confirmation Dialog */}
        {deleteConfirm && (
          <div className="fixed inset-0 bg-black/50 z-[60] flex items-center justify-center p-4">
            <div className="bg-card rounded-lg shadow-xl max-w-sm w-full p-4 border border-border">
              {isDeleting ? (
                // Deleting state
                <div className="text-center py-4">
                  <div className="animate-spin text-3xl mb-3">⏳</div>
                  <p className="text-sm font-medium text-foreground">Deleting message...</p>
                  <p className="text-xs text-muted-foreground mt-1">Please wait</p>
                </div>
              ) : (
                // Confirmation state
                <>
                  <h3 className="font-semibold text-foreground mb-2">Delete Message?</h3>
                  <p className="text-sm text-muted-foreground mb-1">
                    Are you sure you want to delete this message?
                  </p>
                  <p className="text-sm text-foreground bg-secondary/50 rounded p-2 mb-4 italic">
                    &ldquo;{deleteConfirm.content}&rdquo;
                  </p>
                  <div className="flex justify-end gap-2">
                    <button
                      onClick={() => setDeleteConfirm(null)}
                      className="px-3 py-1.5 text-sm rounded-md border border-border hover:bg-secondary transition-colors"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={handleDeleteMessage}
                      className="px-3 py-1.5 text-sm rounded-md bg-destructive text-destructive-foreground hover:bg-destructive/90 transition-colors"
                    >
                      Delete
                    </button>
                  </div>
                </>
              )}
            </div>
          </div>
        )}
      </div>
    </>
  );
});

// Separate component for conversation messages (uses its own query)
interface ConversationMessagesProps {
  conversationId: string;
  localMessages: ChatMessage[];
  onCopy: (content: string) => void;
  onDelete: (messageId: string, content: string) => void;
  formatMessageTime: (dateString: string) => string;
}

function ConversationMessages({
  conversationId,
  localMessages,
  onCopy,
  onDelete,
  formatMessageTime,
}: ConversationMessagesProps) {
  const { data: messages = [], isLoading } = useConversationMessages(conversationId);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Combine cached messages with local optimistic messages
  const allMessages = [...messages, ...localMessages];

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [allMessages.length]);

  if (isLoading) {
    return (
      <div className="bg-card border-t border-border p-4 text-center">
        <span className="animate-spin inline-block">⏳</span>
      </div>
    );
  }

  if (allMessages.length === 0) {
    return (
      <div className="bg-card border-t border-border p-4 text-center text-sm text-muted-foreground">
        No messages
      </div>
    );
  }

  return (
    <div className="bg-card border-t border-border">
      <div className="max-h-80 overflow-y-auto">
        {allMessages.map((msg) => (
          <div
            key={msg.id}
            className={`px-4 py-2 group relative ${
              msg.role === "user" ? "bg-primary/10" : "bg-secondary/30"
            }`}
          >
            <div className="flex items-center justify-between mb-1">
              <div className="flex items-center gap-2">
                <span className="text-xs font-medium">
                  {msg.role === "user" ? "You" : "🤖 AI"}
                </span>
                <span className="text-xs text-muted-foreground">
                  {formatMessageTime(msg.created_at)}
                </span>
              </div>
              {/* Action buttons - visible on hover */}
              <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                {/* Copy button - only for user messages */}
                {msg.role === "user" && (
                  <button
                    onClick={() => onCopy(msg.content)}
                    className="p-1 hover:bg-secondary rounded text-muted-foreground hover:text-foreground transition-colors"
                    title="Copy to clipboard and input"
                  >
                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                    </svg>
                  </button>
                )}
                {/* Delete button - for all messages */}
                <button
                  onClick={() => onDelete(msg.id, msg.content.slice(0, 50) + (msg.content.length > 50 ? "..." : ""))}
                  className="p-1 hover:bg-destructive/20 rounded text-muted-foreground hover:text-destructive transition-colors"
                  title="Delete message"
                >
                  <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                </button>
              </div>
            </div>
            <div className="text-sm text-foreground whitespace-pre-wrap">
              {msg.content}
            </div>
          </div>
        ))}
        {/* Scroll target */}
        <div ref={messagesEndRef} />
      </div>
    </div>
  );
}
