# PHR-002: Unified UI Vision for Second Iteration

**Date**: 2025-12-10
**Phase**: Phase III+ (Second Iteration)
**Category**: UI/UX Design / Feature Request

## Vision

A unified split-pane interface that combines manual task management with AI chat assistance.

## Layout

```
┌─────────────────────────────────────────────────────────────────┐
│                         Header / Nav                             │
├─────────────────────────────────┬───────────────────────────────┤
│                                 │                               │
│      LEFT PANE (60%)            │      RIGHT PANE (40%)         │
│                                 │                               │
│   Manual Task Management        │      AI Chat Assistant        │
│                                 │                               │
│   ┌─────────────────────────┐   │   ┌─────────────────────┐     │
│   │ + Add Task              │   │   │ Message history     │     │
│   ├─────────────────────────┤   │   │                     │     │
│   │ Filter: All | Active |  │   │   │ User: Add task...   │     │
│   │         Complete        │   │   │ AI: Done! Created...│     │
│   ├─────────────────────────┤   │   │                     │     │
│   │ ☐ Buy groceries         │   │   │                     │     │
│   │ ☑ Finish report         │   │   ├─────────────────────┤     │
│   │ ☐ Call mom              │   │   │ 🎤 [Type or speak] │     │
│   │ ...                     │   │   └─────────────────────┘     │
│   └─────────────────────────┘   │                               │
│                                 │                               │
├─────────────────────────────────┴───────────────────────────────┤
│                         Summary Stats                            │
└─────────────────────────────────────────────────────────────────┘
```

## Left Pane: Enhanced Manual Task Management

### Features
- Add/edit/delete tasks with rich UI
- Drag-and-drop reordering
- Inline editing (double-click to edit)
- Filters: All, Active, Complete
- Search/filter by keyword
- Bulk actions (select multiple, delete, complete)
- Task details panel (click to expand)
- Due dates, priorities, tags (Phase V features)

### UI Enhancements
- Smooth animations (add/remove/complete)
- Visual feedback for actions
- Keyboard shortcuts (Enter to add, Delete to remove)
- Modern design with shadcn/ui components
- Dark mode support

## Right Pane: AI Chat Assistant

### Features
- Persistent chat history
- Context-aware responses (knows about user's tasks)
- Real-time task updates (chat actions reflect in left pane)
- Conversation history sidebar (collapsible)

### Voice Functionality
- **Voice Input**: Click microphone or press hotkey to speak
- **Voice Output**: AI responses can be read aloud (TTS)
- **Wake word** (optional): "Hey Todo" to start listening
- **Continuous conversation mode**: Keep mic active

### Voice Implementation Options
1. **Web Speech API** (browser native, free)
   - `SpeechRecognition` for speech-to-text
   - `SpeechSynthesis` for text-to-speech

2. **OpenAI Whisper** (higher accuracy, cost)
   - Send audio to Whisper API
   - Better for noisy environments

3. **Hybrid Approach**
   - Web Speech API for input
   - OpenAI TTS for natural voice output

## Synchronization

- Actions in left pane update immediately
- Actions via chat update left pane in real-time
- WebSocket or polling for live sync
- Optimistic updates with rollback on error

## Technical Considerations

### Frontend
- Split pane component (resizable)
- Shared state between panes (React Context or Zustand)
- WebSocket connection for real-time updates
- Media APIs for voice (getUserMedia, MediaRecorder)

### Backend
- WebSocket endpoint for real-time sync
- Audio transcription endpoint (if using Whisper)
- Event broadcasting for multi-device sync

## Priority Order

1. Split-pane layout with basic sync
2. Enhanced left pane UI
3. Voice input (Web Speech API)
4. Voice output (TTS)
5. Real-time WebSocket sync
6. Advanced features (drag-drop, bulk actions)

## References

- shadcn/ui: https://ui.shadcn.com/
- Web Speech API: https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API
- OpenAI Whisper: https://platform.openai.com/docs/guides/speech-to-text
- OpenAI TTS: https://platform.openai.com/docs/guides/text-to-speech

---

**Part of**: Evolution of Todo Reusable Intelligence
**Tags**: ui, ux, voice, chat, split-pane, second-iteration
