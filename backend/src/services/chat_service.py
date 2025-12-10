"""Chat service for Phase III AI Chatbot.

This module provides the ChatService class that orchestrates chat interactions
between users and the AI assistant, including tool execution.
"""

import json
import logging
import uuid
from datetime import datetime
from typing import Any

from sqlmodel import Session, select

from src.models.conversation import Conversation
from src.models.message import Message
from src.mcp.server import get_tool_definitions
from src.services.openai_client import (
    create_chat_completion,
    get_response_content,
    parse_tool_calls,
)

logger = logging.getLogger(__name__)

# System prompt for the task assistant
SYSTEM_PROMPT = """You are a helpful task management assistant. You help users manage their tasks through natural language.

You have access to the following tools:
- add_task: Create a new task with a title and optional description
- list_tasks: List all tasks, optionally filtered by status (all, complete, incomplete)
- get_task: Get details of a specific task by ID or title
- update_task: Update a task's title or description
- delete_task: Delete a task permanently
- complete_task: Mark a task as complete or toggle its status
- search_tasks: Search tasks by keyword

When users ask you to manage tasks, use the appropriate tools. Be helpful and concise in your responses.
After performing an action, briefly confirm what was done.

Examples of user requests you can handle:
- "Add a task to buy groceries"
- "Show me my tasks"
- "Mark 'buy groceries' as complete"
- "Delete the task about groceries"
- "Rename 'buy groceries' to 'buy organic groceries'"
- "Find tasks about work"
"""


class ChatService:
    """Service for managing chat interactions with the AI assistant."""

    def __init__(self, db: Session, user_id: str):
        """Initialize the chat service.

        Args:
            db: Database session
            user_id: ID of the authenticated user
        """
        self.db = db
        self.user_id = user_id
        self._tool_executor: Any = None

    def set_tool_executor(self, executor: Any) -> None:
        """Set the tool executor (for dependency injection).

        Args:
            executor: Object with execute_tool(name, args) method
        """
        self._tool_executor = executor

    async def process_message(
        self,
        message: str,
        conversation_id: uuid.UUID | None = None,
    ) -> dict[str, Any]:
        """Process a user message and get AI response.

        Args:
            message: User's message text
            conversation_id: Optional conversation ID to continue

        Returns:
            Dict with success, conversation_id, message, and tool_results
        """
        # Get or create conversation
        conversation = await self._get_or_create_conversation(conversation_id)

        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=message,
        )
        self.db.add(user_message)
        self.db.commit()

        # Build message history for OpenAI
        messages = await self._build_message_history(conversation.id)

        # Get AI response with tools
        tools = get_tool_definitions()
        response = await create_chat_completion(messages, tools)

        # Process tool calls if any
        tool_results = []
        tool_calls = parse_tool_calls(response)

        if tool_calls:
            # Save assistant message with tool calls
            assistant_content = get_response_content(response) or ""
            tool_calls_json = json.dumps(tool_calls)

            assistant_message = Message(
                conversation_id=conversation.id,
                role="assistant",
                content=assistant_content,
                tool_calls=tool_calls_json,
            )
            self.db.add(assistant_message)
            self.db.commit()

            # Execute tools and save results
            for tc in tool_calls:
                try:
                    result = await self._execute_tool(tc["name"], json.loads(tc["arguments"]))
                    tool_results.append(
                        {
                            "tool": tc["name"],
                            "success": result.get("success", True),
                            "result": result,
                        }
                    )

                    # Save tool result message
                    tool_message = Message(
                        conversation_id=conversation.id,
                        role="tool",
                        content=json.dumps(result),
                        tool_call_id=tc["id"],
                    )
                    self.db.add(tool_message)
                except Exception as e:
                    logger.error(f"Tool execution error: {e}")
                    tool_results.append(
                        {
                            "tool": tc["name"],
                            "success": False,
                            "error": str(e),
                        }
                    )

            self.db.commit()

            # Get follow-up response from AI with tool results
            messages = await self._build_message_history(conversation.id)
            response = await create_chat_completion(messages, tools)

        # Save final assistant response
        final_content = get_response_content(response)
        if final_content:
            final_message = Message(
                conversation_id=conversation.id,
                role="assistant",
                content=final_content,
            )
            self.db.add(final_message)

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        self.db.commit()

        return {
            "success": True,
            "conversation_id": str(conversation.id),
            "message": final_content,
            "tool_results": tool_results if tool_results else None,
        }

    async def _get_or_create_conversation(
        self, conversation_id: uuid.UUID | None
    ) -> Conversation:
        """Get existing conversation or create a new one.

        Args:
            conversation_id: Optional existing conversation ID

        Returns:
            Conversation instance
        """
        if conversation_id:
            # Try to get existing conversation
            statement = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == self.user_id,
            )
            conversation = self.db.exec(statement).first()
            if conversation:
                return conversation

        # Create new conversation
        conversation = Conversation(user_id=self.user_id)
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    async def _build_message_history(self, conversation_id: uuid.UUID) -> list[dict[str, Any]]:
        """Build message history for OpenAI API.

        Args:
            conversation_id: Conversation ID

        Returns:
            List of message dicts for OpenAI
        """
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        # Get all messages for this conversation
        statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        )
        db_messages = self.db.exec(statement).all()

        for msg in db_messages:
            if msg.role == "user":
                messages.append({"role": "user", "content": msg.content})
            elif msg.role == "assistant":
                msg_dict: dict[str, Any] = {"role": "assistant", "content": msg.content or ""}
                if msg.tool_calls:
                    # Parse tool_calls and convert to OpenAI format
                    tool_calls = json.loads(msg.tool_calls)
                    msg_dict["tool_calls"] = [
                        {
                            "id": tc["id"],
                            "type": "function",
                            "function": {
                                "name": tc["name"],
                                "arguments": tc["arguments"]
                                if isinstance(tc["arguments"], str)
                                else json.dumps(tc["arguments"]),
                            },
                        }
                        for tc in tool_calls
                    ]
                messages.append(msg_dict)
            elif msg.role == "tool":
                messages.append(
                    {
                        "role": "tool",
                        "content": msg.content,
                        "tool_call_id": msg.tool_call_id,
                    }
                )

        return messages

    async def _execute_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        """Execute a tool and return the result.

        Args:
            name: Tool name
            arguments: Tool arguments

        Returns:
            Tool execution result
        """
        if self._tool_executor:
            return await self._tool_executor.execute_tool(name, arguments)

        # Default implementation - return error if no executor set
        return {
            "success": False,
            "error": f"Tool executor not configured for tool: {name}",
        }

    async def get_conversations(self, limit: int = 20, offset: int = 0) -> dict[str, Any]:
        """Get user's conversations.

        Args:
            limit: Maximum conversations to return
            offset: Number to skip

        Returns:
            Dict with conversations list and total count
        """
        # Get conversations
        statement = (
            select(Conversation)
            .where(Conversation.user_id == self.user_id)
            .order_by(Conversation.updated_at.desc())
            .offset(offset)
            .limit(limit)
        )
        conversations = self.db.exec(statement).all()

        # Get total count
        count_statement = select(Conversation).where(Conversation.user_id == self.user_id)
        total_count = len(self.db.exec(count_statement).all())

        return {
            "success": True,
            "conversations": [
                {
                    "id": str(c.id),
                    "title": c.title,
                    "created_at": c.created_at.isoformat(),
                    "updated_at": c.updated_at.isoformat(),
                }
                for c in conversations
            ],
            "total_count": total_count,
        }

    async def get_conversation(self, conversation_id: uuid.UUID) -> dict[str, Any] | None:
        """Get a specific conversation with messages.

        Args:
            conversation_id: Conversation ID

        Returns:
            Dict with conversation and messages, or None if not found
        """
        # Get conversation
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == self.user_id,
        )
        conversation = self.db.exec(statement).first()

        if not conversation:
            return None

        # Get messages
        msg_statement = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        )
        messages = self.db.exec(msg_statement).all()

        return {
            "success": True,
            "conversation": {
                "id": str(conversation.id),
                "title": conversation.title,
                "created_at": conversation.created_at.isoformat(),
                "updated_at": conversation.updated_at.isoformat(),
                "message_count": len(messages),
            },
            "messages": [
                {
                    "id": str(m.id),
                    "role": m.role,
                    "content": m.content,
                    "tool_calls": json.loads(m.tool_calls) if m.tool_calls else None,
                    "tool_call_id": m.tool_call_id,
                    "created_at": m.created_at.isoformat(),
                }
                for m in messages
            ],
        }

    async def delete_conversation(self, conversation_id: uuid.UUID) -> bool:
        """Delete a conversation and its messages.

        Args:
            conversation_id: Conversation ID

        Returns:
            True if deleted, False if not found
        """
        # Get conversation
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == self.user_id,
        )
        conversation = self.db.exec(statement).first()

        if not conversation:
            return False

        # Delete messages first
        msg_statement = select(Message).where(Message.conversation_id == conversation_id)
        messages = self.db.exec(msg_statement).all()
        for msg in messages:
            self.db.delete(msg)

        # Delete conversation
        self.db.delete(conversation)
        self.db.commit()

        return True
