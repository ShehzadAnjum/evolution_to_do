import { NextRequest, NextResponse } from "next/server";

/**
 * Message API proxy route.
 *
 * Deletes a specific message from a conversation.
 */

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string; messageId: string }> }
) {
  try {
    const { id, messageId } = await params;

    // Get authorization header
    const authorization = request.headers.get("Authorization");
    if (!authorization) {
      return NextResponse.json(
        { success: false, message: "Authorization required" },
        { status: 401 }
      );
    }

    // Forward request to backend
    const response = await fetch(
      `${BACKEND_URL}/api/chat/conversations/${id}/messages/${messageId}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: authorization,
        },
      }
    );

    // Handle empty response (204 No Content)
    if (response.status === 204) {
      return NextResponse.json({ success: true });
    }

    // Parse response
    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
      return NextResponse.json(
        { success: false, message: data.detail || "Failed to delete message" },
        { status: response.status }
      );
    }

    return NextResponse.json({ success: true, ...data });
  } catch (error) {
    console.error("Message delete proxy error:", error);
    return NextResponse.json(
      {
        success: false,
        message: error instanceof Error ? error.message : "Internal server error",
      },
      { status: 500 }
    );
  }
}
