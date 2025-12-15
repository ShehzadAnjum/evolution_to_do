---
name: voice-chat-bilingual
description: Voice chat with bilingual support (English/Urdu). Use when implementing speech-to-text, text-to-speech, or multilingual voice interfaces using Web Speech API and Edge TTS.
---

# Voice Chat Bilingual

## Speech-to-Text (Web Speech API)

```typescript
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.continuous = false;
recognition.interimResults = false;
recognition.lang = "en-US"; // or "ur-PK" for Urdu

recognition.onresult = (event) => {
  const transcript = event.results[0][0].transcript;
  sendMessage(transcript);
};

recognition.start(); // Requires user gesture
```

## Text-to-Speech (Edge TTS)

```python
# Backend endpoint
import edge_tts

async def text_to_speech(text: str, language: str = "en") -> bytes:
    voice = "en-US-AriaNeural" if language == "en" else "ur-PK-UzmaNeural"
    communicate = edge_tts.Communicate(text, voice)

    audio_data = b""
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data += chunk["data"]
    return audio_data
```

## Language Detection

```python
def detect_language(text: str) -> str:
    urdu_chars = set("آابپتٹثجچحخدڈذرڑزژسشصضطظعغفقکگلمنوہھیے")
    roman_urdu_words = {"hai", "kya", "nahi", "aur", "mein", "yeh", "karo"}

    if any(c in urdu_chars for c in text):
        return "urdu_script"
    if any(word in text.lower().split() for word in roman_urdu_words):
        return "roman_urdu"
    return "english"
```

## Frontend Voice Toggle

```tsx
const [isListening, setIsListening] = useState(false);

<Button onClick={() => {
  if (isListening) {
    recognition.stop();
  } else {
    recognition.start();
  }
  setIsListening(!isListening);
}}>
  {isListening ? <MicOff /> : <Mic />}
</Button>
```

## Notes

- Web Speech API requires HTTPS in production
- Edge TTS is free and high-quality
- Always request microphone permission with user gesture
