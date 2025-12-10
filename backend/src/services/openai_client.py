"""OpenAI client wrapper for Phase III AI Chatbot.

This module provides a simple wrapper around the OpenAI API for chat completions
with function/tool calling support.
"""

from typing import Any

from openai import OpenAI

from src.api.config import get_settings

# Initialize OpenAI client
_client: OpenAI | None = None


def get_openai_client() -> OpenAI:
    """Get or create the OpenAI client instance."""
    global _client
    if _client is None:
        settings = get_settings()
        api_key = settings.openai_api_key
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        _client = OpenAI(api_key=api_key)
    return _client


async def create_chat_completion(
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]] | None = None,
    model: str = "gpt-4o-mini",
    temperature: float = 0.7,
) -> dict[str, Any]:
    """Create a chat completion with optional tool calling.

    Args:
        messages: List of message dicts with role and content
        tools: Optional list of tool definitions
        model: OpenAI model to use
        temperature: Sampling temperature

    Returns:
        The completion response as a dict
    """
    client = get_openai_client()

    kwargs: dict[str, Any] = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }

    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = "auto"

    response = client.chat.completions.create(**kwargs)
    return response.model_dump()


def parse_tool_calls(response: dict[str, Any]) -> list[dict[str, Any]]:
    """Extract tool calls from a chat completion response.

    Args:
        response: The chat completion response

    Returns:
        List of tool call dicts with id, name, and arguments
    """
    tool_calls = []
    message = response.get("choices", [{}])[0].get("message", {})

    if message.get("tool_calls"):
        for tc in message["tool_calls"]:
            tool_calls.append(
                {
                    "id": tc["id"],
                    "name": tc["function"]["name"],
                    "arguments": tc["function"]["arguments"],
                }
            )

    return tool_calls


def get_response_content(response: dict[str, Any]) -> str:
    """Extract the text content from a chat completion response.

    Args:
        response: The chat completion response

    Returns:
        The assistant's text response
    """
    message = response.get("choices", [{}])[0].get("message", {})
    return message.get("content") or ""
