"use client";

import { useEffect, useRef } from "react";
import type { ChatMessage, ToolResult } from "@/lib/chat/types";

// Detect if text contains Urdu/Arabic script (needs RTL)
function containsUrduScript(text: string): boolean {
  // Unicode range for Arabic script (includes Urdu)
  const urduRegex = /[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]/;
  return urduRegex.test(text);
}

// Get text direction and font class based on content
function getTextStyles(text: string): { dir: "rtl" | "ltr"; className: string } {
  if (containsUrduScript(text)) {
    // Larger font for Urdu - text-base (16px) instead of text-sm (14px)
    // Also add leading-relaxed for better line spacing in Urdu script
    return { dir: "rtl", className: "font-urdu text-right text-base leading-relaxed" };
  }
  return { dir: "ltr", className: "" };
}

interface MessageListProps {
  messages: ChatMessage[];
  isLoading?: boolean;
}

export function MessageList({ messages, isLoading = false }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.length === 0 ? (
        <div className="text-center text-muted-foreground py-8">
          <p className="text-lg font-medium">Welcome to Task Assistant!</p>
          <p className="text-sm mt-2">English / اردو / Roman Urdu</p>
          <p className="text-sm mt-3 font-medium">Try saying:</p>
          <ul className="text-sm mt-2 space-y-1">
            <li>&quot;Add a task to buy groceries&quot;</li>
            <li>&quot;doodh lena hai&quot; <span className="opacity-60">(buy milk)</span></li>
            <li>&quot;report hogayi&quot; <span className="opacity-60">(report done)</span></li>
            <li>&quot;meri tasks dikhao&quot; <span className="opacity-60">(show my tasks)</span></li>
          </ul>
        </div>
      ) : (
        messages.map((message, index) => {
          // Find the next assistant message to get language info
          const nextMessage = messages[index + 1];
          const showLanguageAfterUser = message.role === "user" && nextMessage?.role === "assistant" && nextMessage.input_language;

          return (
            <div key={message.id}>
              <MessageBubble message={message} />
              {/* Show detected language after user message, before AI reply */}
              {showLanguageAfterUser && (
                <div className="text-xs text-green-600 dark:text-green-400 mt-1 mb-2 text-center">
                  Detected: {nextMessage.input_language === "urdu_script" ? "Urdu Script" :
                             nextMessage.input_language === "roman_urdu" ? "Roman Urdu" : "English"}
                </div>
              )}
            </div>
          );
        })
      )}

      {isLoading && (
        <div className="flex justify-start">
          <div className="bg-muted rounded-lg px-4 py-2">
            <div className="flex space-x-2">
              <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
              <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
              <div className="w-2 h-2 bg-muted-foreground rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
            </div>
          </div>
        </div>
      )}

      <div ref={messagesEndRef} />
    </div>
  );
}

function MessageBubble({ message }: { message: ChatMessage }) {
  const isUser = message.role === "user";
  const isAssistant = message.role === "assistant";
  const textStyles = getTextStyles(message.content || "");

  // Debug: Log message props for assistant messages
  if (isAssistant) {
    console.log("[MessageBubble] Assistant message:", {
      id: message.id,
      input_language: message.input_language,
      response_language: message.response_language,
      hasInputLanguage: !!message.input_language,
    });
  }

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] rounded-lg px-4 py-2 ${
          isUser
            ? "bg-primary text-primary-foreground"
            : "bg-muted text-foreground"
        }`}
      >
        <p
          className={`whitespace-pre-wrap ${textStyles.className || 'text-sm'}`}
          dir={textStyles.dir}
        >
          {message.content}
        </p>


        {/* Show tool calls if any */}
        {isAssistant && message.tool_calls && message.tool_calls.length > 0 && (
          <div className="mt-2 pt-2 border-t border-primary/20 text-xs opacity-70">
            <p className="font-medium">Actions taken:</p>
            <ul className="list-disc list-inside">
              {message.tool_calls.map((tc) => (
                <li key={tc.id}>{formatToolName(tc.name)}</li>
              ))}
            </ul>
          </div>
        )}

        <p className="text-xs opacity-50 mt-1">
          {new Date(message.created_at).toLocaleTimeString()}
        </p>
      </div>
    </div>
  );
}

function formatToolName(name: string): string {
  const names: Record<string, string> = {
    add_task: "Added task",
    list_tasks: "Listed tasks",
    get_task: "Retrieved task",
    update_task: "Updated task",
    delete_task: "Deleted task",
    complete_task: "Marked task complete",
    search_tasks: "Searched tasks",
    clear_completed_tasks: "Cleared completed tasks",
  };
  return names[name] || name;
}
