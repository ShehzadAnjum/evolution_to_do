# Skill: Voice Chat (Bilingual - English/Urdu)

**Version**: 1.0.0
**Last Updated**: 2025-12-13
**Category**: Frontend + Backend Integration

---

## Overview

FREE voice chat implementation supporting English and Urdu/Roman Urdu using:
- **STT (Speech-to-Text)**: Web Speech API (browser native, FREE)
- **TTS (Text-to-Speech)**: Edge TTS (Microsoft Neural Voices, FREE)

**Total Cost**: $0.00 per interaction

---

## Technology Stack

### Speech-to-Text (Frontend - Browser)
```typescript
// Web Speech API - FREE, built into Chrome/Edge
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.lang = 'en-US';  // or 'ur-PK' for Urdu
recognition.continuous = false;
recognition.interimResults = true;
```

### Text-to-Speech (Backend - Python)
```python
# Edge TTS - FREE Microsoft Neural Voices
import edge_tts

VOICES = {
    "english": "en-US-JennyNeural",      # Female English (natural)
    "urdu_script": "ur-PK-UzmaNeural",   # Female Urdu
    "roman_urdu": "ur-PK-UzmaNeural",    # Same for Roman Urdu
}

async def synthesize_speech(text: str, language: str) -> bytes:
    voice = VOICES.get(language, "en-US-JennyNeural")
    communicate = edge_tts.Communicate(text, voice)
    audio_bytes = BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_bytes.write(chunk["data"])
    return audio_bytes.getvalue()
```

---

## Key Patterns

### 1. TypeScript Types for Web Speech API

Browser's SpeechRecognition API needs custom type definitions:

```typescript
interface SpeechRecognitionEvent extends Event {
  results: SpeechRecognitionResultList;
  resultIndex: number;
}

interface SpeechRecognitionInstance extends EventTarget {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  start(): void;
  stop(): void;
  onstart: ((event: Event) => void) | null;
  onend: ((event: Event) => void) | null;
  onresult: ((event: SpeechRecognitionEvent) => void) | null;
  onerror: ((event: Event & { error: string }) => void) | null;
}

declare global {
  interface Window {
    SpeechRecognition?: new () => SpeechRecognitionInstance;
    webkitSpeechRecognition?: new () => SpeechRecognitionInstance;
  }
}
```

### 2. TTS Text Cleanup (Remove Punctuation)

TTS reads punctuation literally ("quote" becomes "quote quote"). Clean it:

```python
def clean_text_for_tts(text: str) -> str:
    import re

    # Remove markdown bold/italic
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # **bold** → bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # *italic* → italic

    # Remove quotes (sounds awkward)
    text = text.replace('"', '').replace("'", '')
    text = text.replace('"', '').replace('"', '')  # Smart quotes
    text = text.replace(''', '').replace(''', '')

    # Remove backticks and list markers
    text = text.replace('`', '')
    text = re.sub(r'^\s*[-•]\s*', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s*', '', text, flags=re.MULTILINE)

    # Clean multiple spaces
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
```

### 3. Bilingual Language Detection

Avoid false positives when detecting Roman Urdu vs English:

```python
# WRONG - These English words match Roman Urdu patterns:
#   "to" (English preposition) vs "tou" (Roman Urdu conjunction)
#   "ya" (English informal yes) vs "ya" (Roman Urdu "or")
#   "he/ho" (English pronouns) vs "he/ho" (Roman Urdu "is")

# CORRECT - Remove ambiguous short words from Roman Urdu patterns:
roman_urdu_patterns = [
    r'\b(kar|karo|karna|kiya|kiye)\b',  # "do" forms (NOT "ki")
    r'\b(hai|hain|hona|hua)\b',          # "is/are" (NOT "he/ho")
    r'\b(ka|ke|ko|se|ne|par|mein)\b',   # Postpositions (NOT "ki")
    r'\b(aur|lekin|phir|tou|bhi)\b',    # Conjunctions (NOT "to/ya")
]

# Decision Priority:
# 1. Strong English (1+) AND no Roman Urdu → English
# 2. Strong English (2+) → English (even with some Roman Urdu)
# 3. Roman Urdu (2+) AND no Strong English → Roman Urdu
# 4. Default → English
```

### 4. Auto-Play with Browser Policy

Browsers block auto-play until user interacts. Pattern:

```typescript
// Only enable auto-play after user has interacted (clicked mic, sent message)
const [voiceEnabled, setVoiceEnabled] = useState(false);
const [hasInteracted, setHasInteracted] = useState(false);

const handleSendMessage = () => {
  setHasInteracted(true);  // User interacted
  // ... send message
};

// In useEffect for new AI messages:
if (voiceEnabled && hasInteracted && newAIMessage) {
  speak(newAIMessage.content, responseLanguage);
}
```

---

## File Structure

```
backend/
├── src/
│   ├── services/
│   │   └── voice_service.py      # Edge TTS synthesis
│   └── api/routes/
│       └── voice.py              # POST /api/voice/synthesize

frontend/
├── lib/voice/
│   ├── use-speech-recognition.ts # Web Speech API hook
│   └── api.ts                    # TTS client, speak()
├── components/chat/
│   ├── message-input.tsx         # Mic button
│   └── chat-panel.tsx            # Auto-play TTS
└── app/api/voice/
    └── synthesize/route.ts       # Proxy to backend
```

---

## Available Voices (Edge TTS)

| Language | Voice ID | Gender | Quality |
|----------|----------|--------|---------|
| English | `en-US-JennyNeural` | Female | Natural, friendly |
| English | `en-US-GuyNeural` | Male | Professional |
| Urdu | `ur-PK-UzmaNeural` | Female | Natural |
| Urdu | `ur-PK-AsadNeural` | Male | Professional |

---

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| TypeScript error: Cannot find SpeechRecognition | Browser API not typed | Add custom interface definitions |
| TTS reading quotes aloud | Edge TTS reads punctuation | Use `clean_text_for_tts()` |
| English detected as Roman Urdu | "to", "ya" in patterns | Remove ambiguous words from patterns |
| Auto-play blocked | Browser policy | Require user interaction first |
| Wrong language response | Poor detection | Prioritize strong English indicators |

---

## Dependencies

### Backend
```toml
# pyproject.toml
dependencies = [
    "edge-tts>=6.1.0",  # FREE Microsoft TTS
]
```

### Frontend
- No npm packages needed (Web Speech API is browser native)
- HTML5 Audio element for playback

---

## Testing Checklist

- [ ] English speech → English transcript → English response
- [ ] Urdu speech → Urdu transcript → Urdu response
- [ ] Roman Urdu speech → Urdu script response
- [ ] TTS plays without reading punctuation
- [ ] Language toggle switches recognition language
- [ ] Voice toggle enables/disables auto-play
- [ ] Mic button shows recording indicator
