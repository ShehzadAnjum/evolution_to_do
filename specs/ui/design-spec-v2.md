# UI Design Specification v2.0

**Feature**: Phase II/III (2nd Iteration) - Modern Todo Web Application
**Date**: 2025-12-12
**Version**: 2.0.0
**Status**: Draft - Pending Approval

---

## Design Philosophy

### Core Principles
1. **Outclass Aesthetic** - Premium, modern look exceeding Todoist/TickTick
2. **Accessibility First** - WCAG 2.1 AA compliant, 4.5:1 contrast ratio minimum
3. **Bilingual Support** - English + Urdu (RTL) with auto Roman-Urdu conversion
4. **Mobile-First Responsive** - Beautiful on all devices
5. **Dark Mode Default** - With light mode toggle
6. **Voice-First Input** - Prominent voice input for task creation

---

## Color Palette

### Dark Mode (Default)

Based on [Material Design dark theme guidelines](https://www.toptal.com/designers/ui/dark-ui-design) and [WCAG best practices](https://dubbot.com/dubblog/2023/dark-mode-a11y.html):

```
Background Hierarchy:
├── bg-primary:     #0D1117  (GitHub-style dark, not pure black)
├── bg-secondary:   #161B22  (Elevated surfaces)
├── bg-tertiary:    #21262D  (Cards, modals)
├── bg-hover:       #30363D  (Hover states)
└── bg-active:      #388BFD15 (Selected items with accent tint)

Text Hierarchy:
├── text-primary:   #E6EDF3  (Headings, important text)
├── text-secondary: #8B949E  (Body text, descriptions)
├── text-tertiary:  #6E7681  (Placeholders, disabled)
└── text-link:      #58A6FF  (Links, clickable)

Accent Colors:
├── accent-primary:   #58A6FF  (Primary actions, links)
├── accent-success:   #3FB950  (Complete, success)
├── accent-warning:   #D29922  (Due soon, medium priority)
├── accent-danger:    #F85149  (Overdue, high priority, delete)
└── accent-info:      #A371F7  (Info, low priority)

Priority Colors:
├── priority-high:    #F85149  (Red - urgent)
├── priority-medium:  #D29922  (Amber - normal)
└── priority-low:     #3FB950  (Green - low)

Category Colors:
├── category-work:      #58A6FF  (Blue)
├── category-personal:  #A371F7  (Purple)
├── category-study:     #D29922  (Amber)
├── category-shopping:  #3FB950  (Green)
└── category-general:   #8B949E  (Gray)
```

### Light Mode

```
Background Hierarchy:
├── bg-primary:     #FFFFFF
├── bg-secondary:   #F6F8FA
├── bg-tertiary:    #EAEEF2
├── bg-hover:       #DFE3E6
└── bg-active:      #DDF4FF

Text Hierarchy:
├── text-primary:   #1F2328
├── text-secondary: #57606A
├── text-tertiary:  #8C959F
└── text-link:      #0969DA

Accent Colors:
├── accent-primary:   #0969DA
├── accent-success:   #1A7F37
├── accent-warning:   #9A6700
├── accent-danger:    #CF222E
└── accent-info:      #8250DF
```

---

## Typography

### English Font Stack
```css
font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
```

### Urdu Font Stack (RTL)
Based on [Google Fonts research](https://fonts.google.com/noto/specimen/Noto+Nastaliq+Urdu):

```css
/* Primary: Noto Nastaliq Urdu - Most authentic Nastaliq */
/* Fallback: Gulzar - Modern, Latin counterpart */
font-family: 'Noto Nastaliq Urdu', 'Gulzar', 'Mehr Nastaliq', serif;
```

**Font Loading:**
```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Nastaliq+Urdu:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### Type Scale
```
Heading 1:   2.25rem (36px) - 700 weight - Page titles
Heading 2:   1.5rem  (24px) - 600 weight - Section titles
Heading 3:   1.25rem (20px) - 600 weight - Card titles
Body:        1rem    (16px) - 400 weight - Default text
Body Small:  0.875rem(14px) - 400 weight - Secondary text
Caption:     0.75rem (12px) - 400 weight - Timestamps, hints
```

---

## Layout Structure

### Desktop Layout (≥1024px)

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Header Bar (h: 64px, fixed)                                              │
│  ┌────────────────────────────────────────────────────────────────────┐  │
│  │ 🎯 Evolution Todo    [🔍 Search...        ] [🎤] [🌙/☀️] [👤 User ▼]│  │
│  └────────────────────────────────────────────────────────────────────┘  │
├──────────────┬───────────────────────────────────────────────────────────┤
│              │                                                           │
│  Sidebar     │  Main Content Area                                        │
│  (w: 260px)  │                                                           │
│              │  ┌─────────────────────────────────────────────────────┐  │
│  ┌────────┐  │  │ + Add task...                    [🎤 Voice Input]   │  │
│  │ 📋 All │  │  └─────────────────────────────────────────────────────┘  │
│  │ 📅 Today│  │                                                           │
│  │ 📆 Week │  │  ┌─ Filters ───────────────────────────────────────────┐  │
│  │ ⭐ Prio │  │  │ [All ▼] [Work ▼] [High ▼] [Sort: Priority ▼]       │  │
│  │ ✅ Done │  │  └─────────────────────────────────────────────────────┘  │
│  └────────┘  │                                                           │
│              │  ┌─ Task List ──────────────────────────────────────────┐  │
│  ─────────── │  │                                                       │  │
│              │  │  ☐ 🔴 Task title here...          💼 Work    Dec 15   │  │
│  Categories  │  │     Notes preview text...                            │  │
│  ┌────────┐  │  │  ────────────────────────────────────────────────── │  │
│  │ 💼 Work│  │  │  ☐ 🟡 Another task               🏠 Personal Today   │  │
│  │🏠Person│  │  │     Some description...                              │  │
│  │ 📚Study│  │  │  ────────────────────────────────────────────────── │  │
│  │🛒 Shop │  │  │  ✓ 🟢 Completed task (strikethrough)  📚 Study       │  │
│  │ 📌 Gen │  │  │                                                       │  │
│  │ + Add  │  │  └─────────────────────────────────────────────────────┘  │
│  └────────┘  │                                                           │
│              │  ┌─ Stats Bar ──────────────────────────────────────────┐  │
│  ─────────── │  │ 📊 12 tasks | ✅ 5 done | ⏳ 7 pending | 40% complete │  │
│              │  └─────────────────────────────────────────────────────┘  │
│  Quick Links │                                                           │
│  ┌────────┐  │                                                           │
│  │ 💬 Chat│  │                                                           │
│  │ ⚙️ Set │  │                                                           │
│  │ 🌐 Lang│  │                                                           │
│  └────────┘  │                                                           │
│              │                                                           │
└──────────────┴───────────────────────────────────────────────────────────┘
```

### Tablet Layout (768px - 1023px)

```
┌──────────────────────────────────────────────────────────────────────────┐
│  Header Bar (collapsible sidebar toggle)                                  │
│  [☰] 🎯 Evolution Todo    [🔍] [🎤] [🌙] [👤]                            │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Main Content (full width when sidebar collapsed)                        │
│                                                                          │
│  ┌───────────────────────────────────────────────────────────────────┐   │
│  │ + Add task...                                         [🎤]        │   │
│  └───────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌─ Quick Filters (horizontal scroll) ───────────────────────────────┐   │
│  │ [📋 All] [📅 Today] [⭐ Priority] [💼 Work] [🏠 Personal] [More ▼] │   │
│  └───────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  Task List...                                                            │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

### Mobile Layout (<768px)

```
┌─────────────────────────────────┐
│  Header (h: 56px)               │
│  [☰] 🎯 Todo   [🔍] [🎤] [👤]   │
├─────────────────────────────────┤
│                                 │
│  ┌─ Add Task ─────────────────┐ │
│  │ + What needs to be done?   │ │
│  │                     [🎤]   │ │
│  └────────────────────────────┘ │
│                                 │
│  ┌─ Filter Pills (scroll) ────┐ │
│  │ [All][Today][Work][More ▼] │ │
│  └────────────────────────────┘ │
│                                 │
│  ┌─ Task Item ────────────────┐ │
│  │ ☐ 🔴 Task title            │ │
│  │    💼 Work • Dec 15        │ │
│  └────────────────────────────┘ │
│                                 │
│  ┌─ Task Item ────────────────┐ │
│  │ ☐ 🟡 Another task          │ │
│  │    🏠 Personal • Today     │ │
│  └────────────────────────────┘ │
│                                 │
│           ...                   │
│                                 │
├─────────────────────────────────┤
│  Bottom Nav (h: 64px)           │
│  [📋Tasks] [📅Cal] [💬Chat] [⚙️]│
└─────────────────────────────────┘
```

---

## Component Specifications

### 1. Header Bar

```
Properties:
├── Height: 64px (desktop), 56px (mobile)
├── Position: Fixed top
├── Background: bg-secondary
├── Border: 1px solid border-color
└── Z-index: 50

Elements:
├── Logo: "🎯 Evolution Todo" or icon only on mobile
├── Search: Expandable input with icon
├── Voice Button: Microphone icon, prominent
├── Theme Toggle: Sun/Moon icon
├── User Menu: Avatar + dropdown (Profile, Language, Logout)
└── Mobile: Hamburger menu for sidebar
```

### 2. Sidebar

```
Properties:
├── Width: 260px (desktop), full overlay (mobile)
├── Background: bg-primary
├── Border: 1px solid border-color on right
├── Position: Fixed left (desktop), slide-in drawer (mobile)
└── Collapsible: Yes, with toggle

Sections:
├── Views
│   ├── 📋 All Tasks (default)
│   ├── 📅 Today (due_date = today)
│   ├── 📆 This Week (due_date within 7 days)
│   ├── ⭐ Priority (sorted by priority)
│   ├── ✅ Completed (is_complete = true)
│   └── ⚠️ Overdue (due_date < today, not complete)
│
├── Categories (collapsible)
│   ├── 💼 Work
│   ├── 🏠 Personal
│   ├── 📚 Study
│   ├── 🛒 Shopping
│   ├── 📌 General
│   └── [+ Add Category] (user can add custom)
│
└── Quick Links
    ├── 💬 AI Chat
    ├── 📊 Statistics
    ├── 🌐 Language (EN/UR)
    └── ⚙️ Settings
```

### 3. Task Input Bar

```
Properties:
├── Background: bg-tertiary
├── Border: 1px solid border-color
├── Border-radius: 12px
├── Padding: 16px
├── Margin-bottom: 16px
└── Shadow: subtle drop shadow

Elements:
├── Text Input
│   ├── Placeholder: "What needs to be done?" / "کیا کرنا ہے؟"
│   ├── Full width
│   ├── Natural language parsing support
│   └── Roman Urdu auto-detection
│
├── Voice Input Button
│   ├── Microphone icon
│   ├── Position: Right side
│   ├── States: idle, listening (pulsing), processing
│   └── Tooltip: "Voice input (Ctrl+Shift+V)"
│
├── Quick Options (shown on focus/hover)
│   ├── Priority selector (dots: 🔴🟡🟢)
│   ├── Category selector
│   ├── Due date picker
│   └── Submit button
│
└── Keyboard Shortcuts
    ├── Enter: Create task
    ├── Ctrl+Enter: Create and continue
    └── Escape: Clear/Close
```

### 4. Task Item

```
Properties:
├── Background: bg-tertiary (hover: bg-hover)
├── Border-radius: 8px
├── Padding: 12px 16px
├── Margin-bottom: 8px
├── Transition: smooth hover effects
└── Cursor: pointer

Layout:
┌────────────────────────────────────────────────────────────────────┐
│ ☐  🔴  Task Title Here                          💼 Work    Dec 15  │
│        Task description or notes preview...              [⋯]       │
└────────────────────────────────────────────────────────────────────┘

Elements:
├── Checkbox (left)
│   ├── Unchecked: ☐ (border only)
│   ├── Checked: ✓ (filled with accent-success)
│   └── Click: Toggle completion
│
├── Priority Indicator
│   ├── 🔴 High (or filled circle)
│   ├── 🟡 Medium
│   └── 🟢 Low
│
├── Title
│   ├── Primary text
│   ├── Strikethrough when completed
│   └── Max 2 lines, ellipsis
│
├── Description Preview
│   ├── Secondary text
│   ├── Max 1 line, ellipsis
│   └── Only if description exists
│
├── Category Badge
│   ├── Icon + short name
│   ├── Color-coded
│   └── Clickable (filter by category)
│
├── Due Date
│   ├── Relative: "Today", "Tomorrow", "Dec 15"
│   ├── Overdue: Red color
│   └── None: Hidden
│
└── Actions Menu (⋯)
    ├── ✏️ Edit
    ├── 📋 Duplicate
    ├── ↕️ Move to category
    └── 🗑️ Delete (danger)
```

### 5. Task Detail Modal

```
Properties:
├── Type: Slide-in panel (desktop) / Full screen (mobile)
├── Width: 480px (desktop)
├── Background: bg-secondary
├── Animation: Slide from right
└── Overlay: Semi-transparent backdrop

Layout:
┌──────────────────────────────────────────┐
│  ← Back                    [🗑️] [✕]      │
├──────────────────────────────────────────┤
│                                          │
│  ☐ Task Title                            │
│  ────────────────────────────────────── │
│                                          │
│  📝 Description                          │
│  ┌────────────────────────────────────┐  │
│  │ Full description text here...      │  │
│  │                                    │  │
│  └────────────────────────────────────┘  │
│                                          │
│  ⚡ Priority        [🔴 High      ▼]     │
│  📂 Category        [💼 Work      ▼]     │
│  📅 Due Date        [Dec 15, 2025  ▼]    │
│                                          │
│  ────────────────────────────────────── │
│                                          │
│  Created: Dec 10, 2025                   │
│  Updated: Dec 12, 2025                   │
│                                          │
│          [Cancel]  [Save Changes]        │
│                                          │
└──────────────────────────────────────────┘
```

### 6. Voice Input Modal

```
Properties:
├── Type: Centered modal
├── Size: 400px x 300px
├── Background: bg-secondary with blur backdrop
└── Animation: Scale + fade in

Layout:
┌────────────────────────────────────────┐
│                  ✕                      │
│                                        │
│              🎤                         │
│         (pulsing animation)            │
│                                        │
│     "Listening... Speak now"           │
│                                        │
│   ┌────────────────────────────────┐   │
│   │ "Add task buy groceries..."    │   │
│   │ (real-time transcription)      │   │
│   └────────────────────────────────┘   │
│                                        │
│        [Cancel]  [Create Task]         │
│                                        │
└────────────────────────────────────────┘

States:
├── idle: "Click to start"
├── listening: Pulsing mic, waveform animation
├── processing: "Processing..."
└── error: "Couldn't hear you. Try again."
```

### 7. Category Management

```
Add Category Modal:
┌────────────────────────────────────────┐
│  Add New Category                  ✕   │
├────────────────────────────────────────┤
│                                        │
│  Name                                  │
│  ┌────────────────────────────────┐   │
│  │ Health & Fitness               │   │
│  └────────────────────────────────┘   │
│                                        │
│  Icon                                  │
│  [🏋️][🎯][📱][🎵][✈️][🎮][💡][🔧]     │
│  (scrollable emoji picker)             │
│                                        │
│  Color                                 │
│  [●][●][●][●][●][●][●][●]             │
│  (color palette)                       │
│                                        │
│          [Cancel]  [Add Category]      │
│                                        │
└────────────────────────────────────────┘
```

### 8. Language Toggle (English ↔ Urdu)

```
Dropdown:
┌────────────────────────┐
│ 🌐 Language            │
├────────────────────────┤
│ ● English              │
│ ○ اردو (Urdu)          │
├────────────────────────┤
│ Auto-convert Roman     │
│ Urdu to Urdu script    │
│ [✓ Enabled]            │
└────────────────────────┘

When Urdu:
├── RTL layout
├── Noto Nastaliq Urdu font
├── All UI labels in Urdu
└── Roman Urdu input auto-converted
```

### 9. Chat Interface (AI Assistant)

```
Layout:
┌──────────────────────────────────────────┐
│  💬 AI Task Assistant            [✕]     │
├──────────────────────────────────────────┤
│                                          │
│  ┌─ Assistant ─────────────────────────┐ │
│  │ Hi! I can help you manage tasks.    │ │
│  │ Try: "Add task buy milk tomorrow"   │ │
│  └─────────────────────────────────────┘ │
│                                          │
│  ┌─ You ───────────────────────────────┐ │
│  │ میرے کام دکھاؤ                        │ │
│  │ (Show my tasks - auto-converted)    │ │
│  └─────────────────────────────────────┘ │
│                                          │
│  ┌─ Assistant ─────────────────────────┐ │
│  │ آپ کے 5 کام ہیں:                      │ │
│  │ 1. ✅ Complete report                │ │
│  │ 2. ⏳ Buy groceries                  │ │
│  │ ...                                 │ │
│  └─────────────────────────────────────┘ │
│                                          │
├──────────────────────────────────────────┤
│  ┌────────────────────────────┐  [🎤]   │
│  │ Type or speak...           │  [→]   │
│  └────────────────────────────┘         │
└──────────────────────────────────────────┘
```

---

## Animations & Micro-interactions

### Task Interactions
```
Task Creation:
├── Slide down + fade in (300ms)
└── Subtle bounce at end

Task Completion:
├── Checkbox: Scale bounce (200ms)
├── Title: Strikethrough sweep (300ms)
└── Row: Subtle gray overlay

Task Deletion:
├── Swipe left (mobile)
├── Fade out + height collapse (300ms)
└── Undo toast appears

Task Drag (future):
├── Lift with shadow increase
├── Drop with spring animation
└── Other items slide to make room
```

### Voice Input
```
Mic Button:
├── idle: Static
├── hover: Subtle scale (1.05)
├── active: Pulsing glow animation
└── processing: Spinning loader

Waveform:
├── Real-time audio visualization
├── CSS/Canvas based
└── Smooth transitions
```

### Page Transitions
```
Route Changes:
├── Fade (200ms)
└── Maintain scroll position

Modal Open:
├── Backdrop: Fade in (200ms)
├── Content: Scale up from 0.95 (300ms)
└── Spring easing

Sidebar Toggle:
├── Desktop: Width transition (300ms)
└── Mobile: Slide from left (300ms)
```

---

## Accessibility Requirements

### WCAG 2.1 AA Compliance
```
Contrast Ratios:
├── Normal text: ≥4.5:1
├── Large text (18px+): ≥3:1
├── UI components: ≥3:1
└── Focus indicators: ≥3:1

Keyboard Navigation:
├── All interactive elements focusable
├── Visible focus ring (2px solid accent)
├── Tab order logical
├── Escape closes modals
└── Arrow keys for lists

Screen Reader:
├── Semantic HTML (header, nav, main, section)
├── ARIA labels on icon buttons
├── Live regions for dynamic content
├── Alt text for images/icons
└── Form labels associated with inputs

Motion:
├── Respect prefers-reduced-motion
├── Provide alternative to animations
└── No flashing content
```

### RTL Support (Urdu)
```
Layout:
├── dir="rtl" on html/body when Urdu
├── Flex/Grid direction reversed
├── Text alignment right
└── Icons flip where appropriate

Fonts:
├── Noto Nastaliq Urdu primary
├── Line height: 2.2 (taller for Nastaliq)
└── Letter spacing: normal
```

---

## Roman Urdu to Urdu Conversion

### Implementation Approach

Based on [research](https://github.com/Anas1108/Transliteration-RomantoUrdu-And-ViceVersa):

```
Option 1: Backend API (Recommended)
├── Python urduhack library
├── AI4Bharat transliteration
├── POST /api/transliterate { text: "kaam", to: "ur" }
└── Response: { text: "کام" }

Option 2: Client-side (Fallback)
├── Simple mapping dictionary for common words
├── Rule-based conversion for basic patterns
└── Flag for "unsure" words

Auto-Detection:
├── Detect if input contains only Latin characters
├── Check for Urdu language setting
├── If both true, auto-convert
└── Show preview: "kaam → کام"
```

---

## Component Inventory

### New Components Needed

| Component | Priority | Complexity |
|-----------|----------|------------|
| Sidebar | High | Medium |
| TaskInput | High | Medium |
| TaskItem | High | Low |
| TaskDetail | High | Medium |
| VoiceInput | High | High |
| CategoryManager | Medium | Medium |
| ThemeToggle | Medium | Low |
| LanguageToggle | Medium | Medium |
| FilterBar | Medium | Low |
| StatsBar | Low | Low |
| BottomNav | Medium | Low |

### Existing Components to Update

| Component | Changes |
|-----------|---------|
| TaskList | Add filters, grouping |
| TaskForm | Add voice, inline creation |
| ChatInterface | Add Urdu support, voice |
| Header | Add search, voice, theme toggle |

---

## Responsive Breakpoints

```css
/* Mobile First */
@media (min-width: 640px)  { /* sm */ }
@media (min-width: 768px)  { /* md - tablet */ }
@media (min-width: 1024px) { /* lg - desktop */ }
@media (min-width: 1280px) { /* xl - large desktop */ }
```

---

## References & Inspiration

### Design Sources
- [Todoist](https://todoist.com) - Clean simplicity
- [TickTick](https://ticktick.com) - Feature richness
- [Things 3](https://thesweetsetup.com/apps/best-personal-gtd-app-suite/) - Apple-level polish
- [Dribbble Todo Designs](https://dribbble.com/tags/todo-app)
- [GitHub Dark Mode](https://github.com) - Color palette inspiration

### Technical References
- [Dark Mode Best Practices 2024](https://www.algoworks.com/blog/dark-mode-designs-in-2024/)
- [WCAG Dark Mode Accessibility](https://dubbot.com/dubblog/2023/dark-mode-a11y.html)
- [Noto Nastaliq Urdu Font](https://fonts.google.com/noto/specimen/Noto+Nastaliq+Urdu)
- [AI4Bharat Transliteration](https://pypi.org/project/ai4bharat-transliteration/)

---

## Approval Checklist

- [ ] Color palette approved
- [ ] Typography approved
- [ ] Layout structure approved
- [ ] Component specifications approved
- [ ] Accessibility requirements reviewed
- [ ] RTL/Urdu approach approved
- [ ] Voice input approach approved
- [ ] Roman Urdu conversion approach approved

---

**Document Version**: 2.0.0
**Created**: 2025-12-12
**Author**: AI Assistant (utilizing Frontend Web Agent)
**Status**: Awaiting User Approval
