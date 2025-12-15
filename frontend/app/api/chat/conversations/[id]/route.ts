import { NextRequest, NextResponse } from "next/server";

/**
 * Single conversation API proxy route.
 *
 * Gets or deletes a specific conversation from the backend.
 */

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;

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
      `${BACKEND_URL}/api/chat/conversations/${id}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: authorization,
        },
      }
    );

    // Parse response
    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json(
        { success: false, message: data.detail || "Failed to get conversation" },
        { status: response.status }
      );
    }

    return NextResponse.json(data);
  } catch (error) {
    console.error("Conversation proxy error:", error);
    return NextResponse.json(
      {
        success: false,
        message: error instanceof Error ? error.message : "Internal server error",
      },
      { status: 500 }
    );
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id } = await params;

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
      `${BACKEND_URL}/api/chat/conversations/${id}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: authorization,
        },
      }
    );

    // Parse response
    const data = await response.json();

    if (!response.ok) {
      return NextResponse.json(
        { success: false, message: data.detail || "Failed to delete conversation" },
        { status: response.status }
      );
    }

    return NextResponse.json(data);
  } catch (error) {
    console.error("Conversation delete proxy error:", error);
    return NextResponse.json(
      {
        success: false,
        message: error instanceof Error ? error.message : "Internal server error",
      },
      { status: 500 }
    );
  }
}
