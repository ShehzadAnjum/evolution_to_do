"use client";

import { useState, useCallback, useRef } from "react";
import { MessageList } from "./message-list";
import { MessageInput } from "./message-input";
import { getAuthToken } from "@/lib/auth-token";
import { speak, mapLanguageForTTS } from "@/lib/voice/api";
import type { ChatMessage, ChatResponse } from "@/lib/chat/types";

interface ChatPanelProps {
  isOpen: boolean;
  onClose: () => void;
  onTasksChanged?: () => void;
}

export function ChatPanel({ isOpen, onClose, onTasksChanged }: ChatPanelProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [voiceEnabled, setVoiceEnabled] = useState(true);
  const [isSpeaking, setIsSpeaking] = useState(false);

  // Track if we should speak (to avoid speaking on page load)
  const shouldSpeakRef = useRef(false);

  const sendMessage = useCallback(
    async (content: string) => {
      if (!content.trim()) return;

      // Mark that we should speak the response
      shouldSpeakRef.current = true;

      const userMessage: ChatMessage = {
        id: `temp-${Date.now()}`,
        role: "user",
        content,
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
            message: content,
            conversation_id: conversationId,
          }),
        });

        if (!response.ok) {
          const errorData = await response.json().catch(() => ({}));
          throw new Error(errorData.message || `Error: ${response.statusText}`);
        }

        const data: ChatResponse = await response.json();

        if (!conversationId && data.conversation_id) {
          setConversationId(data.conversation_id);
        }

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
          input_language: data.input_language,
          response_language: data.response_language,
        };

        setMessages((prev) => [...prev, assistantMessage]);

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
          const taskTools = ["add_task", "update_task", "delete_task", "complete_task", "clear_completed_tasks"];
          const hasTaskChange = data.tool_results.some((tr) => taskTools.includes(tr.tool));
          if (hasTaskChange) {
            onTasksChanged();
          }
        }
      } catch (err) {
        let errorMessage = err instanceof Error ? err.message : "Failed to send message";
        // Handle common backend errors
        if (errorMessage.includes("Method Not Allowed") || errorMessage.includes("405")) {
          errorMessage = "Chat service is currently unavailable. Please try again later.";
        } else if (errorMessage.includes("Failed to fetch") || errorMessage.includes("NetworkError")) {
          errorMessage = "Cannot connect to chat service. Please check your connection.";
        }
        setError(errorMessage);
        setMessages((prev) => prev.slice(0, -1));
      } finally {
        setIsLoading(false);
      }
    },
    [conversationId, voiceEnabled, onTasksChanged]
  );

  const clearChat = () => {
    setMessages([]);
    setConversationId(undefined);
    setError(null);
    shouldSpeakRef.current = false;
  };

  const toggleVoice = () => {
    setVoiceEnabled((prev) => !prev);
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

      {/* Panel */}
      <div
        className={`
          fixed top-0 right-0 h-full w-full sm:w-96 lg:w-[420px]
          bg-background border-l border-border
          transform transition-transform duration-300 ease-in-out
          z-50 flex flex-col
          ${isOpen ? "translate-x-0" : "translate-x-full"}
        `}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-4 h-16 border-b border-border bg-card">
          <div className="flex items-center gap-2">
            <span className="text-xl">🤖</span>
            <h2 className="font-semibold text-foreground">AI Assistant</h2>
            {isSpeaking && (
              <span className="text-xs text-green-500 animate-pulse">🔊</span>
            )}
          </div>
          <div className="flex items-center gap-1">
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
              onClick={clearChat}
              className="flex items-center gap-1 px-2 py-1 text-xs hover:bg-secondary rounded-lg text-muted-foreground hover:text-foreground transition-colors"
              title="Clear all chat messages"
            >
              🗑️ <span>Clear</span>
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
          <div className="bg-destructive/10 border-b border-destructive/20 px-4 py-2 text-sm text-destructive">
            {error}
            <button
              onClick={() => setError(null)}
              className="ml-2 underline hover:no-underline"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Messages area - scrollable */}
        <div className="flex-1 overflow-y-auto min-h-0">
          <MessageList messages={messages} isLoading={isLoading} />
        </div>

        {/* Welcome message when empty */}
        {messages.length === 0 && (
          <div className="absolute inset-0 top-16 flex items-center justify-center p-8 pointer-events-none">
            <div className="text-center text-muted-foreground">
              <div className="text-4xl mb-4">💬</div>
              <p className="text-sm">
                Ask me to manage your tasks!
              </p>
              <p className="text-xs mt-2 opacity-70">
                Try: &quot;Add a task to buy groceries&quot; or &quot;Show my tasks for today&quot;
              </p>
              <p className="text-xs mt-2 opacity-50">
                🎤 Voice input supported | 🔊 Auto-play enabled
              </p>
            </div>
          </div>
        )}

        {/* Input area */}
        <MessageInput
          onSend={sendMessage}
          disabled={isLoading}
          placeholder="Ask me to manage your tasks..."
        />
      </div>
    </>
  );
}
