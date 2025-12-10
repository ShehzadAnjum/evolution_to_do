"""Chat API endpoints for Phase III AI Chatbot.

This module provides chat endpoints for interacting with the AI assistant.
"""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlmodel import Session

from ..deps import get_session, get_current_user_id
from ...services.chat_service import ChatService
from ...mcp.tools.tool_executor import ToolExecutor


router = APIRouter(prefix="/api/chat", tags=["chat"])


class ChatRequest(BaseModel):
    """Request body for sending a chat message."""

    message: str = Field(..., min_length=1, max_length=4000, description="User message")
    conversation_id: Optional[str] = Field(
        default=None, description="Optional conversation ID to continue"
    )


class ChatResponse(BaseModel):
    """Response from the chat endpoint."""

    success: bool
    conversation_id: str
    message: str
    tool_results: Optional[list[dict]] = None


@router.post("/", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Send a message to the AI assistant.

    The assistant can use tools to manage tasks on behalf of the user.

    Args:
        request: Chat request with message and optional conversation_id
        user_id: Authenticated user ID from JWT
        session: Database session

    Returns:
        Chat response with AI message and any tool results
    """
    # Create chat service and tool executor
    chat_service = ChatService(session, user_id)
    tool_executor = ToolExecutor(session, user_id)
    chat_service.set_tool_executor(tool_executor)

    # Parse conversation_id if provided
    conversation_uuid = None
    if request.conversation_id:
        try:
            conversation_uuid = UUID(request.conversation_id)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid conversation ID format",
            )

    # Process the message
    try:
        result = await chat_service.process_message(
            message=request.message,
            conversation_id=conversation_uuid,
        )
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing message: {str(e)}",
        )


@router.get("/conversations")
async def list_conversations(
    limit: int = 20,
    offset: int = 0,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """List user's conversations.

    Args:
        limit: Maximum conversations to return (default 20, max 100)
        offset: Number of conversations to skip
        user_id: Authenticated user ID
        session: Database session

    Returns:
        List of conversations with total count
    """
    # Validate parameters
    if limit < 1 or limit > 100:
        limit = 20
    if offset < 0:
        offset = 0

    chat_service = ChatService(session, user_id)
    return await chat_service.get_conversations(limit, offset)


@router.get("/conversations/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Get a specific conversation with messages.

    Args:
        conversation_id: UUID of the conversation
        user_id: Authenticated user ID
        session: Database session

    Returns:
        Conversation details with messages
    """
    try:
        conv_uuid = UUID(conversation_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID format",
        )

    chat_service = ChatService(session, user_id)
    result = await chat_service.get_conversation(conv_uuid)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    return result


@router.delete("/conversations/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """Delete a conversation and its messages.

    Args:
        conversation_id: UUID of the conversation
        user_id: Authenticated user ID
        session: Database session

    Returns:
        Success message
    """
    try:
        conv_uuid = UUID(conversation_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid conversation ID format",
        )

    chat_service = ChatService(session, user_id)
    deleted = await chat_service.delete_conversation(conv_uuid)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    return {"success": True, "message": "Conversation deleted"}
