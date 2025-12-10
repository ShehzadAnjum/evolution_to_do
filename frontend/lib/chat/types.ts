/**
 * Chat types for Phase III AI Chatbot.
 *
 * These types define the data structures used for chat communication
 * between the frontend and backend.
 */

/**
 * Request to send a chat message.
 */
export interface ChatRequest {
  /** User's message to the AI assistant */
  message: string;
  /** Optional conversation ID to continue an existing conversation */
  conversation_id?: string;
}

/**
 * Response from the chat API.
 */
export interface ChatResponse {
  /** Whether the request was successful */
  success: boolean;
  /** The conversation ID (new or existing) */
  conversation_id: string;
  /** AI assistant's response message */
  message: string;
  /** Results from any tools invoked by the AI */
  tool_results?: ToolResult[];
}

/**
 * Result from a tool invocation.
 */
export interface ToolResult {
  /** Name of the tool that was invoked */
  tool: ToolName;
  /** Whether the tool executed successfully */
  success: boolean;
  /** Tool-specific result data */
  result?: Record<string, unknown>;
  /** Error message if tool failed */
  error?: string;
}

/**
 * Available tool names.
 */
export type ToolName =
  | "add_task"
  | "list_tasks"
  | "get_task"
  | "update_task"
  | "delete_task"
  | "complete_task"
  | "search_tasks";

/**
 * Chat message as stored/displayed.
 */
export interface ChatMessage {
  /** Unique message ID */
  id: string;
  /** Message role */
  role: MessageRole;
  /** Message content */
  content: string;
  /** Tool calls made by assistant (if role is assistant) */
  tool_calls?: ToolCall[];
  /** ID of the tool call this message responds to (if role is tool) */
  tool_call_id?: string;
  /** When the message was created */
  created_at: string;
}

/**
 * Message role types.
 */
export type MessageRole = "user" | "assistant" | "tool";

/**
 * Tool call made by the assistant.
 */
export interface ToolCall {
  /** Unique tool call ID */
  id: string;
  /** Tool name */
  name: ToolName;
  /** Tool arguments */
  arguments: Record<string, unknown>;
}

/**
 * Conversation summary for list view.
 */
export interface ConversationSummary {
  /** Unique conversation ID */
  id: string;
  /** Optional title (may be auto-generated) */
  title?: string;
  /** When the conversation was created */
  created_at: string;
  /** Last activity timestamp */
  updated_at: string;
  /** Number of messages */
  message_count?: number;
}

/**
 * Response from listing conversations.
 */
export interface ConversationListResponse {
  /** Whether the request was successful */
  success: boolean;
  /** List of conversations */
  conversations: ConversationSummary[];
  /** Total number of conversations */
  total_count: number;
}

/**
 * Response from getting a single conversation.
 */
export interface ConversationDetailResponse {
  /** Whether the request was successful */
  success: boolean;
  /** Conversation metadata */
  conversation: ConversationSummary;
  /** Messages in the conversation */
  messages: ChatMessage[];
}

/**
 * Error response from the API.
 */
export interface ChatError {
  /** Always false for errors */
  success: false;
  /** Error code */
  error_code: ErrorCode;
  /** Human-readable error message */
  message: string;
}

/**
 * Error codes returned by the API.
 */
export type ErrorCode =
  | "INVALID_INPUT"
  | "UNAUTHORIZED"
  | "CONVERSATION_NOT_FOUND"
  | "PERMISSION_DENIED"
  | "AI_SERVICE_ERROR"
  | "INTERNAL_ERROR";
