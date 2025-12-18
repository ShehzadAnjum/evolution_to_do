/**
 * Central Version Management - SINGLE SOURCE OF TRUTH
 *
 * Version Format: mm.nn.ooo
 * - mm  = Major version (phase/iteration changes)
 * - nn  = Feature version (new features within phase)
 * - ooo = Patch version (bug fixes, iterations on current feature)
 *
 * ┌─────────────────────────────────────────────────────────────────┐
 * │  IMPORTANT: Increment this version with EVERY code change!     │
 * │                                                                 │
 * │  Bug fix?      → Increment ooo (05.07.002 → 05.07.003)        │
 * │  New feature?  → Increment nn, reset ooo (05.07.003 → 05.08.001)│
 * │  Major change? → Increment mm, reset nn/ooo (05.08.001 → 06.01.001)│
 * └─────────────────────────────────────────────────────────────────┘
 */

// ═══════════════════════════════════════════════════════════════════
//                    CURRENT VERSION - UPDATE HERE
// ═══════════════════════════════════════════════════════════════════
export const VERSION = {
  major: 5,
  feature: 11,
  patch: 0,
} as const;

// Computed version strings
export const VERSION_STRING = `${String(VERSION.major).padStart(2, '0')}.${String(VERSION.feature).padStart(2, '0')}.${String(VERSION.patch).padStart(3, '0')}`;
export const VERSION_DISPLAY = `v${VERSION_STRING}`;

// Legacy export for backward compatibility
export const APP_VERSION = VERSION_STRING;

/**
 * Version History (recent):
 *
 * v05.11.000 - 2025-12-17 - FreeRTOS MQTT task, task auto-complete, sidebar fix
 * v05.10.007 - 2025-12-16 - ESP32 LCD scroll fix, MQTT update on task edit
 * v05.08.002 - 2025-12-13 - Voice fixes: Language detection, TTS cleanup, strict relevance
 * v05.08.001 - 2025-12-13 - Voice chat: FREE STT (Web Speech) + TTS (Edge TTS)
 * v05.07.016 - 2024-12-12 - Smaller stats + added "3 Days" upcoming count
 * v05.07.015 - 2024-12-12 - Fixed Today count timezone + AI must use actual task ID/title
 * v05.07.014 - 2024-12-12 - Strict rule: NEVER dump all tasks, filter by relevance
 * v05.07.013 - 2024-12-12 - Improved language detection (strong vs weak English words)
 * v05.07.012 - 2024-12-12 - Enhanced humor for wife/spouse situations
 * v05.07.011 - 2024-12-12 - Moved language indicator between user msg and AI reply
 * v05.07.010 - 2024-12-12 - Fixed backend ChatResponse to include language fields
 * v05.07.009 - 2024-12-12 - Debug logging for language display in UI
 * v05.07.008 - 2024-12-12 - Simple English detection + explicit language prefix to AI
 * v05.07.007 - 2024-12-12 - Language display in chat + brighter version color
 * v05.07.006 - 2024-12-12 - AI self-detects language (removed regex patterns)
 * v05.07.005 - 2024-12-12 - Debug logging for chat + larger Urdu font
 * v05.07.004 - 2024-12-12 - Language detection FIRST + task refresh emphasis
 * v05.07.003 - 2024-12-12 - Generic situation impact analysis (not hardcoded categories)
 * v05.07.002 - 2024-12-12 - Fixed Roman Urdu detection (removed English words)
 * v05.07.001 - 2024-12-12 - Added version display + language detection
 * v05.06.000 - 2024-12-12 - Chat history context + humor rule
 */
