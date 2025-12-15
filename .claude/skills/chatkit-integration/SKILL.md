---
name: chatkit-integration
description: Integrate @chatscope/chat-ui-kit-react for chat interfaces. Use when implementing chat UI, conversation interfaces, or AI chatbot frontends. Provides ChatKit component patterns, styling with Tailwind, and backend integration.
---

# ChatKit Integration

## Quick Start

```bash
npm install @chatscope/chat-ui-kit-react @chatscope/chat-ui-kit-styles
```

## Core Components

```tsx
import {
  MainContainer,
  ChatContainer,
  MessageList,
  Message,
  MessageInput,
  ConversationList,
  Conversation,
  Sidebar,
  Avatar,
  TypingIndicator,
} from "@chatscope/chat-ui-kit-react";
import "@chatscope/chat-ui-kit-styles/dist/default/styles.min.css";
```

## Basic Chat Layout

```tsx
<MainContainer>
  <Sidebar position="left">
    <ConversationList>
      {conversations.map((c) => (
        <Conversation
          key={c.id}
          name={c.title}
          lastSenderName={c.lastMessage?.role}
          info={c.lastMessage?.content.substring(0, 50)}
          onClick={() => selectConversation(c.id)}
        />
      ))}
    </ConversationList>
  </Sidebar>

  <ChatContainer>
    <MessageList
      typingIndicator={isLoading && <TypingIndicator content="AI is thinking..." />}
    >
      {messages.map((m) => (
        <Message
          key={m.id}
          model={{
            message: m.content,
            sender: m.role,
            direction: m.role === "user" ? "outgoing" : "incoming",
            position: "single",
          }}
        />
      ))}
    </MessageList>

    <MessageInput
      placeholder="Type message here..."
      onSend={handleSend}
      disabled={isLoading}
      attachButton={false}
    />
  </ChatContainer>
</MainContainer>
```

## Styling Override for Tailwind

Create `chatkit-overrides.css`:
```css
/* Override ChatKit defaults to work with Tailwind dark mode */
.cs-main-container {
  @apply bg-background border-border;
}
.cs-message__content {
  @apply bg-muted text-foreground;
}
.cs-message--outgoing .cs-message__content {
  @apply bg-primary text-primary-foreground;
}
.cs-message-input__content-editor {
  @apply bg-background text-foreground;
}
```

## Backend Integration Pattern

```tsx
const sendMessage = async (text: string) => {
  // Optimistic UI update
  setMessages(prev => [...prev, { role: "user", content: text }]);
  setIsLoading(true);

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json", Authorization: `Bearer ${token}` },
      body: JSON.stringify({ message: text, conversation_id: conversationId }),
    });
    const data = await res.json();
    setMessages(prev => [...prev, { role: "assistant", content: data.message }]);
  } finally {
    setIsLoading(false);
  }
};
```

## Load Conversation History

```tsx
useEffect(() => {
  if (conversationId) {
    fetch(`/api/chat/conversations/${conversationId}`)
      .then(res => res.json())
      .then(data => setMessages(data.messages));
  }
}, [conversationId]);
```

## Anti-Patterns

- **Don't** initialize messages as empty array without loading history
- **Don't** forget to import the CSS styles
- **Don't** use without authentication context
