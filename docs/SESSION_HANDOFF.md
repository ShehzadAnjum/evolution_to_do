# Session Handoff

**Last Updated**: 2025-12-13 (Voice Chat Fixes Session)
**Updated By**: AI Assistant (Claude Code)
**Current Phase**: Phase III - AI Chat Agent Enhancement
**Current Branch**: main
**Current Version**: 05.08.002

---

## Quick Status (30-Second Read)

### Current State
- **Complete: 1st Iteration LOCKED** (tag: `v1.0.0-iteration1`)
- **Complete: Phase I (2nd Iteration)** - Console App v1 (Basic) & v2 (Textual TUI)
- **Complete: Phase II/III (1st Iteration) LOCKED** (tag: `v1.0.0-phase2-3-web`)
- **Complete: Phase II/III (2nd Iteration)** - Backend v2.0.0 + Frontend GUI v2.0.0
- **Complete: Custom Categories** - Database-persistent user categories
- **Complete: Phase IV** - Docker + Kubernetes + Helm (local Minikube)
- **Complete: Phase V Local** - Kafka + Dapr on Minikube WORKING
- **Complete: AI Chat Agent v2.2** - Bilingual + Humor + Smart Filtering
- **Deferred: Phase V Cloud** - GKE quota exceeded, pending increase

### Last Session Summary (2025-12-13 Voice Chat Fixes)
- What accomplished:
  - **Voice Chat Fixes (v05.08.002)**:
    - **Language Detection Fix**: Removed false positives from Roman Urdu patterns
      - Words removed: `to`, `ya`, `he`, `ho`, `ki`, `na`, `g`, `din`, `wife`, `office`
      - Now: Strong English (1+) with no Roman Urdu → English
      - English speech now correctly stays in English
    - **TTS Punctuation Fix**: Added `clean_text_for_tts()` function
      - Strips: quotes (`"`, `'`), markdown (`**`, `*`), backticks, list markers
      - TTS now sounds natural without reading punctuation
    - **Task Relevance Fix**: Added "STRICT RELEVANCE" rule to system prompt
      - Only suggest tasks with DIRECT logical connection
      - "grocery shopping" → groceries, shopping, food (NOT "hang out with friends")
      - Test: "Does this task have a LOGICAL connection?" - if NO, don't suggest

- **Previous Session (Voice Chat Feature v05.08.001)** - FREE, no API costs!
    - **Speech-to-Text**: Web Speech API (browser native)
      - Supports English (en-US) and Urdu (ur-PK)
      - Language toggle in chat input area
      - Real-time interim transcription display
      - Auto-send on speech completion
    - **Text-to-Speech**: Edge TTS (Microsoft Neural Voices)
      - English: `en-US-JennyNeural` (female)
      - Urdu: `ur-PK-UzmaNeural` (female)
      - Auto-play AI responses when voice enabled
      - Mute/unmute toggle in chat header
    - **UI Enhancements**:
      - 🎤 Mic button for voice input
      - 🔊 Voice toggle button (green when enabled)
      - Recording indicator with red pulse animation
      - Speaking indicator when TTS playing

  - **Backend Voice Service**:
    - New `/api/voice/synthesize` endpoint
    - Edge TTS integration (FREE Microsoft neural voices)
    - Language-aware voice selection

  - **Frontend Voice Components**:
    - `use-speech-recognition.ts` hook (Web Speech API)
    - `voice/api.ts` for TTS client
    - Updated `message-input.tsx` with mic button
    - Updated `chat-panel.tsx` with auto-play TTS

- What learned:
  - Web Speech API is FREE and built into Chrome/Edge
  - Edge TTS provides neural voices for FREE (no API key needed)
  - TypeScript needs custom types for SpeechRecognition API
  - Auto-play requires user interaction first (browser policy)

- **Previous Session (2025-12-12 Night)**:
  - Bilingual language detection (Strong vs Weak English)
  - Enhanced humor for wife/spouse situations
  - Context-aware task filtering
  - AI must use actual task ID/title
  - Today count timezone fix
  - Sidebar stats redesign

- **What's next (TO REVISIT)**:
  1. Test voice in production (Vercel/Railway)
  2. More sophisticated situation analysis
  3. Voice command shortcuts
  4. Better error handling for voice

---

## AI Chat System Prompt Rules Summary

### Current Rules (in order):
1. **LANGUAGE RULE** - Detect and respond in user's language (English/Roman Urdu/Urdu Script)
2. **REFRESH & FILTER TASKS** - Context-aware relevance, NEVER dump all tasks
3. **USE ACTUAL TASK ID/TITLE** - Never use translations, use exact title from JSON
4. **VERIFY BEFORE CONFIRMING** - Check success field, report actual results
5. **SPECIFICITY AND HONESTY** - Never mention fictional tasks, exact details only
6. **HUMOR WHERE APPROPRIATE** - Wife/spouse situations, light teasing with emojis

### Language Detection Logic (v05.08.002):
- **Strong English**: articles (the/a/an), be verbs (is/are/was), modals, contractions
- **Weak English**: task, add, delete, priority, tomorrow (commonly borrowed)
- **Roman Urdu**: kar/karo/hai/kal/mujhe/nahe (NOT: to, ya, he, ho, ki, na, din, wife, office)
- **Decision Priority**:
  1. Strong English (1+) AND no Roman Urdu → English
  2. Strong English (2+) → English (even with some Roman Urdu)
  3. Roman Urdu (2+) AND no Strong English → Roman Urdu
  4. Default → English

---

## Version History (Recent)

| Version | Description |
|---------|-------------|
| 05.08.002 | Voice fixes: Language detection, TTS cleanup, strict relevance |
| 05.08.001 | Voice chat: FREE STT (Web Speech) + TTS (Edge TTS) |
| 05.07.016 | Smaller stats + "Next 3 Days" upcoming count |
| 05.07.015 | Fixed Today count timezone + AI must use actual task ID/title |
| 05.07.014 | Strict rule: NEVER dump all tasks, filter by relevance |
| 05.07.013 | Improved language detection (strong vs weak English) |
| 05.07.012 | Enhanced humor for wife/spouse situations |
| 05.07.011 | Moved language indicator between user msg and AI reply |
| 05.07.010 | Fixed backend ChatResponse to include language fields |

---

## Files Modified This Session

### Backend (NEW):
- `backend/src/services/voice_service.py` - Edge TTS service (FREE neural voices)
- `backend/src/api/routes/voice.py` - `/api/voice/synthesize` endpoint
- `backend/src/api/main.py` - Registered voice router
- `backend/pyproject.toml` - Added edge-tts dependency

### Frontend (NEW):
- `frontend/lib/voice/use-speech-recognition.ts` - Web Speech API hook
- `frontend/lib/voice/api.ts` - TTS API client, speak() function
- `frontend/app/api/voice/synthesize/route.ts` - Next.js proxy to backend

### Frontend (MODIFIED):
- `frontend/components/chat/message-input.tsx` - Mic button, voice language toggle
- `frontend/components/chat/chat-panel.tsx` - Auto-play TTS, voice toggle button
- `frontend/lib/version.ts` - v05.08.001

---

## Deployments

| Service | Platform | URL | Status |
|---------|----------|-----|--------|
| Frontend (v2) | Vercel | https://evolution-to-do.vercel.app | Live |
| Backend | Railway | https://evolutiontodo-production-e1b6.up.railway.app | Live |
| Database | Neon | PostgreSQL (v2.0.0 schema) | Connected |

---

## Commands Reference

```bash
# Backend development
cd backend
uv run uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

# Frontend development
cd frontend
npm run dev

# For local testing, ensure frontend/.env.local has:
NEXT_PUBLIC_API_URL="http://localhost:8000"
```

---
