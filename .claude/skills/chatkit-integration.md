# Skill: ChatKit Integration

## Overview

This skill captures patterns for integrating ChatKit as the chat UI component for the AI agent in Phase III.

## Core Concepts

### ChatKit Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Next.js App                          │
├─────────────────┬───────────────────┬───────────────────────┤
│   ChatKit UI    │   API Route       │   MCP Client          │
│                 │                   │                       │
│ - Message list  │ - Stream handler  │ - Tool calls          │
│ - Input field   │ - OpenAI proxy    │ - Context mgmt        │
│ - Typing ind.   │ - User context    │ - Response format     │
└─────────────────┴───────────────────┴───────────────────────┘
```

### Component Hierarchy

```
<ChatProvider>
  <ChatContainer>
    <ChatHeader />
    <MessageList>
      <Message />
      <Message />
    </MessageList>
    <ChatInput />
  </ChatContainer>
</ChatProvider>
```

## Installation

```bash
cd frontend
npm install @chatkit/react @chatkit/core
```

## Basic Setup

### Provider Configuration

**File**: `frontend/app/providers.tsx`
```typescript
"use client";

import { ChatProvider } from "@chatkit/react";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ChatProvider
      config={{
        apiEndpoint: "/api/chat",
        streaming: true,
      }}
    >
      {children}
    </ChatProvider>
  );
}
```

### Chat Component

**File**: `frontend/components/chat/TodoChat.tsx`
```typescript
"use client";

import {
  ChatContainer,
  ChatHeader,
  MessageList,
  ChatInput,
  Message,
} from "@chatkit/react";
import { useChat } from "@chatkit/react";

export function TodoChat() {
  const { messages, sendMessage, isLoading } = useChat();

  return (
    <ChatContainer className="h-full flex flex-col">
      <ChatHeader title="Todo Assistant" />
      
      <MessageList className="flex-1 overflow-y-auto p-4">
        {messages.map((msg) => (
          <Message
            key={msg.id}
            role={msg.role}
            content={msg.content}
          />
        ))}
      </MessageList>
      
      <ChatInput
        onSend={sendMessage}
        disabled={isLoading}
        placeholder="Ask me to manage your tasks..."
      />
    </ChatContainer>
  );
}
```

## API Route Integration

**File**: `frontend/app/api/chat/route.ts`
```typescript
import { OpenAI } from "openai";
import { auth } from "@/lib/auth/config/auth";
import { headers } from "next/headers";
import { NextRequest } from "next/server";

const openai = new OpenAI();

export async function POST(req: NextRequest) {
  // Get authenticated user
  const session = await auth.api.getSession({
    headers: await headers(),
  });

  if (!session) {
    return new Response("Unauthorized", { status: 401 });
  }

  const { messages } = await req.json();

  // Call OpenAI with tools
  const response = await openai.chat.completions.create({
    model: "gpt-4o",
    messages: [
      {
        role: "system",
        content: `You are a helpful todo assistant for ${session.user.name}.
          You can help manage their tasks using the available tools.
          Be concise and friendly.`,
      },
      ...messages,
    ],
    tools: getMCPTools(),
    stream: true,
  });

  // Stream response
  const stream = new ReadableStream({
    async start(controller) {
      for await (const chunk of response) {
        const content = chunk.choices[0]?.delta?.content || "";
        controller.enqueue(new TextEncoder().encode(content));
      }
      controller.close();
    },
  });

  return new Response(stream, {
    headers: { "Content-Type": "text/plain" },
  });
}
```

## Styling with Tailwind

**File**: `frontend/components/chat/chat-styles.css`
```css
/* Custom ChatKit styling */
.chatkit-container {
  @apply bg-background border rounded-lg shadow-sm;
}

.chatkit-header {
  @apply border-b px-4 py-3;
}

.chatkit-message {
  @apply p-3 rounded-lg max-w-[80%] mb-2;
}

.chatkit-message--user {
  @apply bg-primary text-primary-foreground ml-auto;
}

.chatkit-message--assistant {
  @apply bg-muted mr-auto;
}

.chatkit-input {
  @apply border-t p-4;
}

.chatkit-input input {
  @apply w-full px-4 py-2 border rounded-lg;
}
```

## Tool Result Display

```typescript
function ToolResultMessage({ result }: { result: ToolResult }) {
  if (result.tool === "list_tasks") {
    return (
      <div className="space-y-2">
        {result.tasks.map((task) => (
          <div key={task.id} className="flex items-center gap-2">
            <Checkbox checked={task.completed} />
            <span className={task.completed ? "line-through" : ""}>
              {task.title}
            </span>
          </div>
        ))}
      </div>
    );
  }

  return <p>{result.message}</p>;
}
```

## Context Management

```typescript
// Maintain conversation context
const chatContext = {
  userId: session.user.id,
  recentTasks: [], // Last 5 tasks for quick reference
  preferences: {
    defaultView: "pending",
  },
};

// Include in system prompt
const systemPrompt = `
You are a todo assistant for ${session.user.name}.

Recent tasks context:
${chatContext.recentTasks.map(t => `- ${t.title}`).join('\n')}

Preferences:
- Default view: ${chatContext.preferences.defaultView}
`;
```

## Anti-Patterns

### ❌ No Authentication

```typescript
// DANGEROUS: No user context
export async function POST(req: NextRequest) {
  const { messages } = await req.json();
  // Anyone can call this!
}
```

### ✅ Always Authenticate

```typescript
export async function POST(req: NextRequest) {
  const session = await auth.api.getSession({
    headers: await headers(),
  });
  if (!session) {
    return new Response("Unauthorized", { status: 401 });
  }
}
```

### ❌ Blocking UI

```typescript
// Bad: Waiting for full response
const response = await fetch("/api/chat", {
  method: "POST",
  body: JSON.stringify({ messages }),
});
const data = await response.json();
setMessages([...messages, data]);
```

### ✅ Stream Responses

```typescript
// Good: Stream for better UX
const response = await fetch("/api/chat", { ... });
const reader = response.body.getReader();
while (true) {
  const { done, value } = await reader.read();
  if (done) break;
  appendToCurrentMessage(new TextDecoder().decode(value));
}
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Messages not streaming | Check stream: true in OpenAI config |
| Auth errors | Verify session in API route |
| Styling issues | Check Tailwind classes applied |
| Tool calls not working | Verify MCP tools registered |

---

**Part of**: Evolution of Todo Reusable Intelligence
**Phase**: III, IV, V
**Last Updated**: 2025-12-10
