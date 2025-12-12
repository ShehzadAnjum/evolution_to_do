import { NextRequest, NextResponse } from "next/server";

/**
 * Voice synthesis API proxy route.
 *
 * Proxies TTS requests to the FastAPI backend, forwarding
 * the Authorization header for JWT authentication.
 * Returns MP3 audio bytes.
 */

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function POST(request: NextRequest) {
  try {
    // Get authorization header
    const authorization = request.headers.get("Authorization");
    if (!authorization) {
      return NextResponse.json(
        { success: false, message: "Authorization required" },
        { status: 401 }
      );
    }

    // Parse request body
    const body = await request.json();

    // Forward request to backend
    const response = await fetch(`${BACKEND_URL}/api/voice/synthesize`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: authorization,
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      return NextResponse.json(
        { success: false, message: errorData.detail || "TTS synthesis failed" },
        { status: response.status }
      );
    }

    // Return audio bytes with correct content type
    const audioBuffer = await response.arrayBuffer();
    return new NextResponse(audioBuffer, {
      status: 200,
      headers: {
        "Content-Type": "audio/mpeg",
        "Content-Disposition": "inline; filename=speech.mp3",
        "Cache-Control": "no-cache",
      },
    });
  } catch (error) {
    console.error("Voice synthesis proxy error:", error);
    return NextResponse.json(
      {
        success: false,
        message: error instanceof Error ? error.message : "Internal server error",
      },
      { status: 500 }
    );
  }
}
