"""Voice API endpoints for Text-to-Speech synthesis.

This module provides voice synthesis using FREE Edge TTS (Microsoft Neural Voices).
Supports English and Urdu languages.
"""

from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel, Field

from ..deps import get_current_user_id
from ...services.voice_service import synthesize_speech, get_available_voices


router = APIRouter(prefix="/api/voice", tags=["voice"])


class SynthesizeRequest(BaseModel):
    """Request body for TTS synthesis."""

    text: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Text to convert to speech"
    )
    language: Literal["english", "roman_urdu", "urdu_script"] = Field(
        default="english",
        description="Language for voice selection"
    )


@router.post("/synthesize")
async def synthesize(
    request: SynthesizeRequest,
    user_id: str = Depends(get_current_user_id),
):
    """Convert text to speech using Edge TTS.

    Returns MP3 audio bytes. This is a FREE service using Microsoft Neural Voices.

    Supported languages and voices:
    - english: en-US-JennyNeural (female)
    - urdu_script: ur-PK-UzmaNeural (female)
    - roman_urdu: ur-PK-UzmaNeural (female)

    Args:
        request: Synthesis request with text and language
        user_id: Authenticated user ID from JWT

    Returns:
        MP3 audio as binary response
    """
    try:
        audio_bytes = await synthesize_speech(
            text=request.text,
            language=request.language
        )

        if not audio_bytes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to generate audio - empty text or synthesis error"
            )

        return Response(
            content=audio_bytes,
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "inline; filename=speech.mp3",
                "Cache-Control": "no-cache",
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"TTS synthesis failed: {str(e)}"
        )


@router.get("/voices")
async def list_voices(
    user_id: str = Depends(get_current_user_id),
):
    """List available TTS voices.

    Returns information about available English and Urdu voices.
    Useful for debugging or offering voice selection in future.

    Args:
        user_id: Authenticated user ID from JWT

    Returns:
        Dictionary with voice information
    """
    try:
        voices = await get_available_voices()
        return {"success": True, "voices": voices}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list voices: {str(e)}"
        )
