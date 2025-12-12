"""
Voice Service - Text-to-Speech using FREE Edge TTS (Microsoft Neural Voices)

This service provides high-quality TTS without any API costs.
Supports English and Urdu voices.
"""

import logging
from io import BytesIO

import edge_tts

log = logging.getLogger(__name__)

# Voice mapping for different languages
# All voices are FREE Microsoft Neural voices
VOICES = {
    "english": "en-US-JennyNeural",       # Female English (natural, friendly)
    "urdu_script": "ur-PK-UzmaNeural",    # Female Urdu
    "roman_urdu": "ur-PK-UzmaNeural",     # Female Urdu (same as urdu_script)
}

# Alternative voices (can be used for variety)
ALTERNATIVE_VOICES = {
    "english_male": "en-US-GuyNeural",
    "urdu_male": "ur-PK-AsadNeural",
}


async def synthesize_speech(text: str, language: str = "english") -> bytes:
    """
    Convert text to speech using Edge TTS (FREE Microsoft Neural Voices).

    Args:
        text: The text to convert to speech
        language: One of 'english', 'roman_urdu', or 'urdu_script'

    Returns:
        MP3 audio bytes
    """
    if not text or not text.strip():
        log.warning("Empty text provided for TTS")
        return b""

    # Select voice based on language
    voice = VOICES.get(language, VOICES["english"])
    log.info(f"Synthesizing speech: language={language}, voice={voice}, text_length={len(text)}")

    try:
        # Create Edge TTS communicator
        communicate = edge_tts.Communicate(text, voice)

        # Collect audio chunks
        audio_bytes = BytesIO()
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_bytes.write(chunk["data"])

        audio_data = audio_bytes.getvalue()
        log.info(f"TTS completed: {len(audio_data)} bytes generated")
        return audio_data

    except Exception as e:
        log.error(f"TTS synthesis failed: {e}")
        raise


async def get_available_voices() -> dict:
    """
    Get list of available Edge TTS voices.
    Useful for debugging or offering voice selection.

    Returns:
        Dictionary with voice information
    """
    try:
        voices = await edge_tts.list_voices()
        # Filter to relevant languages
        relevant_voices = [
            v for v in voices
            if v.get("Locale", "").startswith(("en-", "ur-"))
        ]
        return {
            "total": len(voices),
            "english_urdu_voices": relevant_voices
        }
    except Exception as e:
        log.error(f"Failed to list voices: {e}")
        return {"error": str(e)}
