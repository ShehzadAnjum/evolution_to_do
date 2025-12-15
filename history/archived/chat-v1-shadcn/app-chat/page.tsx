"use client";

import { ChatInterface } from "@/components/chat";
import { SignOutButton } from "@/app/dashboard/SignOutButton";
import Link from "next/link";

/**
 * Chat page for Phase III AI Chatbot.
 *
 * Provides a chat interface for users to interact with the
 * AI task management assistant.
 */
export default function ChatPage() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5 p-8">
      <div className="max-w-3xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold bg-gradient-to-r from-primary via-accent to-primary bg-clip-text text-transparent">
              Task Assistant
            </h1>
            <p className="text-muted-foreground mt-1">
              Chat with AI to manage your tasks
            </p>
          </div>
          <div className="flex items-center gap-4">
            <Link
              href="/tasks"
              className="text-sm text-muted-foreground hover:text-foreground transition-colors"
            >
              View Tasks
            </Link>
            <SignOutButton />
          </div>
        </div>

        {/* Chat Interface */}
        <ChatInterface
          onConversationCreated={(id) => {
            // Could update URL or store conversation ID
            console.log("New conversation created:", id);
          }}
        />

        {/* Help text */}
        <div className="mt-4 text-center text-sm text-muted-foreground">
          <p>
            Try: &quot;Add a task&quot;, &quot;Show my tasks&quot;, or &quot;Mark
            task as complete&quot;
          </p>
        </div>
      </div>
    </div>
  );
}
