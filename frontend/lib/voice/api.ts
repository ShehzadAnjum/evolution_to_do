import { getAuthToken } from "@/lib/auth-token";

export type VoiceLanguage = "english" | "roman_urdu" | "urdu_script";

/**
 * Synthesize speech from text using Edge TTS (FREE).
 *
 * @param text - The text to convert to speech
 * @param language - The language for voice selection
 * @returns MP3 audio blob
 */
export async function synthesizeSpeech(
  text: string,
  language: VoiceLanguage = "english"
): Promise<Blob> {
  const token = await getAuthToken();

  if (!token) {
    throw new Error("Authentication required for voice synthesis");
  }

  const response = await fetch("/api/voice/synthesize", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({ text, language }),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `TTS failed: ${response.statusText}`);
  }

  return response.blob();
}

/**
 * Play audio blob using HTML5 Audio element.
 *
 * @param audioBlob - The audio blob to play
 * @returns Promise that resolves when audio finishes playing
 */
export function playAudio(audioBlob: Blob): Promise<void> {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(audioBlob);
    const audio = new Audio(url);

    audio.onended = () => {
      URL.revokeObjectURL(url);
      resolve();
    };

    audio.onerror = (e) => {
      URL.revokeObjectURL(url);
      reject(new Error("Audio playback failed"));
    };

    audio.play().catch(reject);
  });
}

/**
 * Synthesize and play speech in one call.
 *
 * @param text - The text to speak
 * @param language - The language for voice selection
 * @returns Promise that resolves when audio finishes playing
 */
export async function speak(
  text: string,
  language: VoiceLanguage = "english"
): Promise<void> {
  const audioBlob = await synthesizeSpeech(text, language);
  await playAudio(audioBlob);
}

/**
 * Map detected input language to TTS voice language.
 */
export function mapLanguageForTTS(
  inputLanguage: string | undefined
): VoiceLanguage {
  switch (inputLanguage) {
    case "urdu_script":
      return "urdu_script";
    case "roman_urdu":
      return "roman_urdu";
    case "english":
    default:
      return "english";
  }
}
