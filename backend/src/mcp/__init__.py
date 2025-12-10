"""MCP module for Phase III AI Chatbot.

This module provides MCP server setup and tool definitions.
"""

from src.mcp.server import get_tool_definitions, server

__all__ = ["server", "get_tool_definitions"]
