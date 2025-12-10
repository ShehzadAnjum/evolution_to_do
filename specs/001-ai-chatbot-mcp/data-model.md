# Data Model: Phase III AI Chatbot with MCP Tools

**Feature**: `001-ai-chatbot-mcp`
**Date**: 2025-12-10
**Status**: Complete

## Overview

This document defines the database entities required for the Phase III AI Chatbot feature. These entities extend the existing Phase II schema (user, session, task).

---

## Entity Relationship Diagram

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│      User       │       │  Conversation   │       │     Message     │
│  (from Phase II)│       │     (NEW)       │       │     (NEW)       │
├─────────────────┤       ├─────────────────┤       ├─────────────────┤
│ id (PK)         │──────<│ id (PK)         │──────<│ id (PK)         │
│ email           │       │ user_id (FK)    │       │ conversation_id │
│ name            │       │ title           │       │ role            │
│ ...             │       │ created_at      │       │ content         │
└─────────────────┘       │ updated_at      │       │ tool_calls      │
        │                 └─────────────────┘       │ tool_call_id    │
        │                                           │ created_at      │
        │                                           └─────────────────┘
        │
        │         ┌─────────────────┐
        └────────<│      Task       │
                  │  (from Phase II)│
                  ├─────────────────┤
                  │ id (PK)         │
                  │ user_id (FK)    │
                  │ title           │
                  │ description     │
                  │ is_complete     │
                  │ created_at      │
                  │ updated_at      │
                  └─────────────────┘

Legend:
──────<  One-to-Many relationship
(PK)     Primary Key
(FK)     Foreign Key
```

---

## New Entities

### Conversation

Represents a chat session between a user and the AI assistant.

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | Unique conversation identifier |
| user_id | String | FK → user.id, NOT NULL | Owner of the conversation |
| title | String | nullable, max 255 | Optional title (can be auto-generated from first message) |
| created_at | DateTime | NOT NULL, default now() | When conversation started |
| updated_at | DateTime | NOT NULL, default now() | Last activity timestamp |

**Indexes**:
- `idx_conversation_user_id` on `user_id` (for listing user's conversations)
- `idx_conversation_updated_at` on `updated_at` (for sorting by recent)

**SQLModel Definition**:

```python
import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Conversation(SQLModel, table=True):
    __tablename__ = "conversation"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(foreign_key="user.id", nullable=False, index=True)
    title: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

---

### Message

Represents a single message in a conversation (user message, assistant response, or tool result).

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PK, default uuid4 | Unique message identifier |
| conversation_id | UUID | FK → conversation.id, NOT NULL | Parent conversation |
| role | String | NOT NULL, enum | Message role: "user", "assistant", "tool" |
| content | Text | NOT NULL | Message content |
| tool_calls | JSON | nullable | Tool calls made by assistant (JSON array) |
| tool_call_id | String | nullable | Tool call ID this message responds to (for role="tool") |
| created_at | DateTime | NOT NULL, default now() | When message was created |

**Role Values**:
- `user` - Message from the user
- `assistant` - Response from the AI assistant
- `tool` - Result from executing a tool

**Indexes**:
- `idx_message_conversation_id` on `conversation_id` (for loading conversation messages)
- `idx_message_created_at` on `created_at` (for ordering messages)

**SQLModel Definition**:

```python
import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

class Message(SQLModel, table=True):
    __tablename__ = "message"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(
        foreign_key="conversation.id",
        nullable=False,
        index=True
    )
    role: str = Field(nullable=False)  # "user", "assistant", "tool"
    content: str = Field(nullable=False)
    tool_calls: Optional[str] = Field(default=None)  # JSON string
    tool_call_id: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
```

---

## Existing Entities (Phase II - No Changes)

### User

From Better Auth - no modifications needed.

| Field | Type | Description |
|-------|------|-------------|
| id | String | Primary key |
| email | String | User email |
| name | String | Display name |
| emailVerified | Boolean | Email verification status |
| image | String | Profile image URL |
| createdAt | DateTime | Account creation time |
| updatedAt | DateTime | Last update time |

### Task

From Phase II - no modifications needed.

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Primary key |
| user_id | String | FK to user |
| title | String | Task title |
| description | String | Task description |
| is_complete | Boolean | Completion status |
| created_at | DateTime | Creation time |
| updated_at | DateTime | Last update time |

---

## Validation Rules

### Conversation

1. **user_id**: Must reference an existing user
2. **title**: If provided, must be 1-255 characters

### Message

1. **conversation_id**: Must reference an existing conversation
2. **role**: Must be one of: "user", "assistant", "tool"
3. **content**: Must not be empty (after trimming whitespace)
4. **tool_calls**: If provided, must be valid JSON array
5. **tool_call_id**: Required if role is "tool", must match a tool call from previous assistant message

---

## State Transitions

### Conversation Lifecycle

```
Created (empty) → Active (has messages) → Archived (optional future feature)
     │                    │
     │                    │ User sends message
     │                    ▼
     │              Has Messages
     │                    │
     │                    │ Assistant responds
     │                    ▼
     │              Has Responses
     │                    │
     │                    │ (loop: user message → tool calls → assistant response)
     │                    ▼
     └──────────────  Active
```

### Message Types Flow

```
User Message
     │
     ▼
Assistant Message (may include tool_calls)
     │
     ├── If tool_calls present:
     │       │
     │       ▼
     │   Tool Result Message(s)
     │       │
     │       ▼
     │   Assistant Follow-up Message
     │
     └── If no tool_calls:
             │
             ▼
         (await next user message)
```

---

## Migration Notes

### Alembic Migration

```python
"""Add conversation and message tables for Phase III

Revision ID: phase3_001
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

def upgrade():
    # Create conversation table
    op.create_table(
        'conversation',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', sa.String(), sa.ForeignKey('user.id'), nullable=False),
        sa.Column('title', sa.String(255), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_conversation_user_id', 'conversation', ['user_id'])
    op.create_index('idx_conversation_updated_at', 'conversation', ['updated_at'])

    # Create message table
    op.create_table(
        'message',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('conversation_id', UUID(as_uuid=True),
                  sa.ForeignKey('conversation.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('tool_calls', sa.Text(), nullable=True),
        sa.Column('tool_call_id', sa.String(100), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_index('idx_message_conversation_id', 'message', ['conversation_id'])
    op.create_index('idx_message_created_at', 'message', ['created_at'])

def downgrade():
    op.drop_table('message')
    op.drop_table('conversation')
```

---

## Query Patterns

### Common Queries

```python
# Get user's conversations (most recent first)
async def get_user_conversations(user_id: str, limit: int = 20):
    return await session.exec(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(limit)
    )

# Get conversation messages
async def get_conversation_messages(conversation_id: UUID):
    return await session.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )

# Get or create conversation for user
async def get_or_create_conversation(user_id: str) -> Conversation:
    # Get most recent active conversation or create new
    conversation = await session.exec(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(1)
    ).first()

    if not conversation:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)

    return conversation
```

---

## Storage Estimates

| Entity | Est. Rows/User | Avg. Row Size | Est. Storage/User |
|--------|----------------|---------------|-------------------|
| Conversation | 10-50 | 200 bytes | 10 KB |
| Message | 500-2000 | 1 KB | 2 MB |

**Total estimated storage per active user**: ~2 MB

**Notes**:
- Message content is the largest field (can be up to several KB)
- tool_calls JSON can add significant size when tools are called
- Consider implementing message archival for long-term storage optimization
