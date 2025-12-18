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
 * Strip emojis and symbols from text for cleaner TTS output.
 */
function stripEmojisAndSymbols(text: string): string {
  return text
    // Remove emojis (most common Unicode ranges)
    .replace(/[\u{1F600}-\u{1F64F}]/gu, '') // Emoticons
    .replace(/[\u{1F300}-\u{1F5FF}]/gu, '') // Misc Symbols and Pictographs
    .replace(/[\u{1F680}-\u{1F6FF}]/gu, '') // Transport and Map
    .replace(/[\u{1F700}-\u{1F77F}]/gu, '') // Alchemical Symbols
    .replace(/[\u{1F780}-\u{1F7FF}]/gu, '') // Geometric Shapes Extended
    .replace(/[\u{1F800}-\u{1F8FF}]/gu, '') // Supplemental Arrows-C
    .replace(/[\u{1F900}-\u{1F9FF}]/gu, '') // Supplemental Symbols and Pictographs
    .replace(/[\u{1FA00}-\u{1FA6F}]/gu, '') // Chess Symbols
    .replace(/[\u{1FA70}-\u{1FAFF}]/gu, '') // Symbols and Pictographs Extended-A
    .replace(/[\u{2600}-\u{26FF}]/gu, '')   // Misc symbols
    .replace(/[\u{2700}-\u{27BF}]/gu, '')   // Dingbats
    .replace(/[\u{FE00}-\u{FE0F}]/gu, '')   // Variation Selectors
    .replace(/[\u{1F000}-\u{1F02F}]/gu, '') // Mahjong Tiles
    .replace(/[\u{1F0A0}-\u{1F0FF}]/gu, '') // Playing Cards
    // Remove box drawing and special symbols
    .replace(/[─│┌┐└┘├┤┬┴┼═║╒╓╔╕╖╗╘╙╚╛╜╝╞╟╠╡╢╣╤╥╦╧╨╩╪╫╬█▀▄▌▐░▒▓■□▪▫●○◌◍◎★☆]/g, '')
    // Clean up extra whitespace
    .replace(/\s+/g, ' ')
    .trim();
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
  const cleanText = stripEmojisAndSymbols(text);
  if (!cleanText) return; // Don't speak if only emojis
  const audioBlob = await synthesizeSpeech(cleanText, language);
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
