# Session Handoff

**Last Updated**: 2025-12-16 (React Query Caching + Task Visualization)
**Updated By**: AI Assistant (Claude Code)
**Current Phase**: Phase V - COMPLETE (All Phases Done)
**Current Branch**: main
**Current Version**: 05.10.007

---

## 🚨 MANDATORY: RI Announcement Protocol

**Before ANY significant task, ANNOUNCE the Reusable Intelligence being used:**

```
📋 USING: [agent-name], [subagent-name], [skill-name], [mcp-server-name]
```

**Available Resources:**
| Type | Name | Purpose |
|------|------|---------|
| Agent | `infra-devops.md` | Docker, K8s, Helm, Dapr, Cloud |
| Subagent | `cicd-pipeline-subagent.md` | GitHub Actions CI/CD |
| Subagent | `azure-cloud-subagent.md` | Azure AKS, SP, Resource Groups |
| Skill | `github-actions-cicd.md` | Workflow patterns, secrets handling |
| Skill | `azure-aks-deployment.md` | AKS commands, Helm deployment |
| **MCP Server** | `context7` | Library documentation fetcher |

**This is NON-NEGOTIABLE. Always announce. Always (including MCP servers).**

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
- **Complete: Voice Chat** - FREE STT (Web Speech) + TTS (Edge TTS)
- **Complete: Phase V Part A** - Advanced Features (search, filter, sort, time, notifications, recurring)
- **Complete: Phase V Part C** - GitHub Actions CI/CD + Azure AKS Deployment
- **Complete: Cloud Dapr** - Dapr sidecar + Pub/Sub (Redpanda/in-memory) + State Store
- **Complete: Cloud-Native Blueprint** - Reusable Intelligence skill (+200 bonus points)
- **Complete: Capstone Documents** - Phase III, IV, V capstones created
- **Parked: IoT Prototype** - ESP32 MQTT relay controller (tested, working)

### Last Session Summary (2025-12-16 React Query Caching + Task Visualization)

**React Query Chat Caching:**
- Installed `@tanstack/react-query` and `@tanstack/react-query-persist-client`
- Created `QueryProvider` with localStorage persistence (30 min cache)
- Created custom hooks: `useConversations`, `useConversationMessages`, `useDeleteMessage`
- Refactored `chatkit-panel.tsx` to use React Query for stale-while-revalidate UX
- Chat history now loads instantly from cache, syncs in background

**AI Intent Detection (Priority + Recurrence):**
- Backend: Added RULE 7 (priority inference) and RULE 8 (recurrence inference) to system prompt
- Detects "important", "urgent" → High priority
- Detects "har rouz", "har jumma", "every friday", "every month" → recurrence_pattern
- Updated `tool_executor.py` and `server.py` for recurrence support

**Chat UX Improvements:**
- Copy/Delete buttons on messages (hover to reveal)
- Delete confirmation dialog with loading state ("Deleting...")
- Preload chat history on page mount (background loading)
- Loading indicator in main header ("⏳ Loading chat history..." → "✓ Chat loaded")
- Auto-expand most recent conversation
- Wider chat panel (1.5x), taller input (2x height)
- Tasks pane shifts left when chat is open

**Task Visualization (Recharts):**
- Installed `recharts` library
- Created `TaskStats` component with:
  - Donut chart showing completed vs pending (% in center)
  - Status cards: Due Today, Overdue
  - Priority breakdown bars (High/Medium/Low)
- Integrated into Sidebar, replacing old quick stats

**Bug Fixes:**
- Created missing `/api/chat/conversations/[id]/messages/[messageId]/route.ts` (delete was 404)
- Fixed temp message ID detection for local-only deletes

**Safety Checkpoint:** `v5.10.006-pre-react-query` (can revert if needed)

---

### Previous Session (2025-12-16 ChatKit + Skills Migration)

**ChatKit Implementation:**
- Installed `@chatscope/chat-ui-kit-react` and styles
- Created `ChatKitInterface` component with:
  - Sidebar with conversation list
  - Message list with typing indicator
  - Message input with ChatKit components
  - Conversation history loading on mount
- Created API routes for conversation management
- Archived old chat implementation to `history/archived/chat-v1-shadcn/`

**Skills Migration (Anthropic Official Format):**
- Migrated 16 skills to Anthropic's official folder + SKILL.md format
- Each skill now has: `skill-name/SKILL.md` with YAML frontmatter
- Archived old skills to `history/archived/skills-v1/`
- Added `README.md` explaining skills structure

**RI Protocol Updated:**
- Added MCP servers to announcement protocol
- Example: `📋 USING: context7 MCP server`

**Capstone Corrections:**
- Fixed Phase III capstone to show ChatKit as PENDING
- Updated technology compliance section

**Safety Checkpoint:** `v5.10.005-pre-chatkit` (can revert if needed)

---

### Previous Session (2025-12-16 Capstone + Cleanup + IoT)

**Capstone Documents Created:**
- `specs/phases/phase-3-capstone.md` - AI Chatbot + MCP Tools validation
- `specs/phases/phase-4-capstone.md` - Local K8s (Docker + Helm) validation
- `specs/phases/phase-5-capstone.md` - Cloud + Advanced Features validation

**Project Cleanup:**
- Created `.env.local.example` with placeholder values
- Updated `.gitignore` for Zone.Identifier files
- Archived `I2-phase1-thoughts.md`
- Added `ScreenShots/` folder for presentation

**IoT Prototype (Parked):**
- ESP32 MQTT relay controller working with HiveMQ Cloud
- Status: Parked for future demo

---

### Previous Session (2025-12-14 Hackathon Completion)

**Dapr Cloud Deployment:**
- Installed Dapr on AKS via Helm (dapr-system namespace)
- Created Dapr components:
  - `pubsub-memory.yaml` - In-memory pub/sub for demo
  - `pubsub-redpanda.yaml` - Kafka-compatible with Redpanda Cloud
  - `statestore.yaml` - PostgreSQL state store via Neon
- Added Dapr sidecar annotations to backend deployment
- Updated CD workflow to deploy Dapr and components

**Cloud-Native Blueprint Skill Created:**
- Comprehensive skill documenting all cloud-native patterns
- Includes: CI/CD pipeline, Helm charts, Dapr components, debugging guides
- Location: `.claude/skills/cloud-native-blueprint.md`
- Value: +200 hackathon bonus points

**Commits:**
```
0ca33ab feat(dapr): add cloud-native Dapr deployment with Redpanda pub/sub
```

---

### Previous Session (2025-12-14 AKS Auth/CORS Debugging)

**Issues Fixed (4+ hours debugging):**

1. **Secure Cookies over HTTP** - Root cause of "Please log in to view tasks"
   - Problem: `useSecureCookies: NODE_ENV === "production"` but AKS uses HTTP
   - Fix: Changed to `useSecureCookies: BETTER_AUTH_URL.startsWith("https://")`
   - File: `frontend/lib/auth/core/server.ts:46`

2. **CD Pod Restart** - Images not being pulled on deploy
   - Problem: `helm upgrade` doesn't restart pods if spec unchanged (using `latest` tag)
   - Fix: Added `kubectl rollout restart` after helm upgrade
   - File: `.github/workflows/cd.yml:83-88`

3. **Backend CORS** - Browser blocking cross-origin requests
   - Problem: nip.io URL not in allowed origins
   - Fix: Added `http://172.171.119.133.nip.io:3000` to CORS origins
   - File: `backend/src/api/main.py:62`

**Commits This Session:**
```
6a4dcc3 fix(backend): add AKS nip.io URL to CORS allowed origins
5da6aab fix(cd): force pod restart to pull latest images
c5888e4 fix(auth): handle optional BETTER_AUTH_URL in TypeScript
d4a280d fix(auth): disable secure cookies for HTTP deployments (AKS)
```

**AKS Status:** ✅ FULLY WORKING
- Frontend: http://172.171.119.133.nip.io:3000 (static IP)
- Backend: http://48.200.16.149:8000 (dynamic IP, exposed via LoadBalancer)
- Auth: Login works (password + Google OAuth)
- Tasks: CRUD operations working

### Previous Session (2025-12-14 Phase V Part C - Azure AKS)

**Cloud Infrastructure Deployed:**
- GitHub Actions CI: Builds Docker images on push to main
- GHCR: Images pushed to ghcr.io/shehzadanjum/evolution_to_do/{backend,frontend}
- Azure AKS: Cluster in westus2 (1 node, Standard_B2s_v2)
- Helm Chart: evolution-todo deployed successfully
- CD Workflow: Auto-deploy on CI success

**Resources Created:**
| Resource | Details |
|----------|---------|
| Resource Group | `evo-todo-rg` (westus2) |
| AKS Cluster | `evo-todo-aks` (K8s 1.33) |
| Azure SP | `evolution-todo-github-actions` |

**GitHub Secrets Configured:** ✅
- `AZURE_CREDENTIALS` - Service principal JSON
- `DATABASE_URL` - Neon PostgreSQL URL
- `BETTER_AUTH_SECRET` - Auth secret
- `OPENAI_API_KEY` - OpenAI key

**CI/CD Pipeline:** ✅ WORKING
- Push to main → CI builds images → CD deploys to AKS

### Previous Session (2025-12-14 Reusable Intelligence Update)

**Phase V Part A: COMPLETE** - All advanced features implemented and tested.

#### Features Delivered:
1. **Search & Filter** - Backend query params + frontend search bar + category pills
2. **Sort Tasks** - By created_at, due_date, priority, title (asc/desc)
3. **Due Dates with Time** - Time picker + 12-hour display
4. **Browser Notifications** - Bell sound + vibration animation + 10-sec continuous alarm
5. **Recurring Tasks** - Daily/weekly/biweekly/monthly auto-reschedule

#### Commits This Session:
```
6d30b16 fix(notifications): reuse single AudioContext for all chimes
5085bed fix(notifications): fix continuous bell ringing
d76d36a feat(notifications): continuous bell ringing for 10 seconds
82bbca4 feat(notifications): add bell sound and vibration animation
6b525cd fix(notifications): add debug logging and test button
42187de feat(phase-v): Advanced features - search, filter, sort, time, notifications, recurring
```

---

## Reusable Knowledge (React Query + Recharts)

### 1. React Query with localStorage Persistence
```typescript
// components/providers/query-provider.tsx
const CACHE_KEY = "app-query-cache";

function persistCache(client: QueryClient) {
  const cache = client.getQueryCache().getAll();
  const dataToStore = cache
    .filter(query => query.state.data !== undefined)
    .map(query => ({
      queryKey: query.queryKey,
      data: query.state.data,
      dataUpdatedAt: query.state.dataUpdatedAt,
    }));
  localStorage.setItem(CACHE_KEY, JSON.stringify(dataToStore));
}

function restoreCache(client: QueryClient) {
  const cached = localStorage.getItem(CACHE_KEY);
  if (cached) {
    JSON.parse(cached).forEach((item) => {
      // Only restore if cache is less than 30 minutes old
      if (Date.now() - item.dataUpdatedAt < 1000 * 60 * 30) {
        client.setQueryData(item.queryKey, item.data);
      }
    });
  }
}
```

### 2. Custom React Query Hooks Pattern
```typescript
// lib/chat/use-chat-queries.ts
export const chatKeys = {
  all: ["chat"] as const,
  conversations: () => [...chatKeys.all, "conversations"] as const,
  conversation: (id: string) => [...chatKeys.all, "conversation", id] as const,
};

export function useConversations() {
  return useQuery({
    queryKey: chatKeys.conversations(),
    queryFn: fetchConversations,
    staleTime: 1000 * 60 * 2, // 2 minutes
  });
}

export function usePrefetchConversation() {
  const queryClient = useQueryClient();
  return (id: string) => {
    queryClient.prefetchQuery({
      queryKey: chatKeys.conversation(id),
      queryFn: () => fetchMessages(id),
    });
  };
}
```

### 3. Recharts Donut Chart with Center Label
```tsx
<div className="relative h-32">
  <ResponsiveContainer width="100%" height="100%">
    <PieChart>
      <Pie
        data={[
          { name: "Done", value: completed, color: "#22c55e" },
          { name: "Pending", value: pending, color: "#64748b" },
        ]}
        innerRadius={35}
        outerRadius={50}
        paddingAngle={2}
        dataKey="value"
      >
        {data.map((entry, i) => <Cell key={i} fill={entry.color} />)}
      </Pie>
    </PieChart>
  </ResponsiveContainer>
  {/* Center label (absolute positioned) */}
  <div className="absolute inset-0 flex flex-col items-center justify-center">
    <span className="text-xl font-bold">{completionRate}%</span>
  </div>
</div>
```

---

## Reusable Knowledge (Phase V Part A)

### 4. Web Audio API - Bell Sound Pattern
```typescript
// IMPORTANT: Reuse single AudioContext (browsers limit instances!)
let sharedAudioContext: AudioContext | null = null;

function getAudioContext(): AudioContext | null {
  if (!sharedAudioContext) {
    sharedAudioContext = new (window.AudioContext || (window as any).webkitAudioContext)();
  }
  // Resume if suspended (browser autoplay policy)
  if (sharedAudioContext.state === 'suspended') {
    sharedAudioContext.resume();
  }
  return sharedAudioContext;
}

// Bell chime with harmonics
function playBellChime() {
  const ctx = getAudioContext();
  const playTone = (freq, start, duration, volume) => {
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.frequency.value = freq;
    osc.type = 'sine';
    gain.gain.setValueAtTime(0, ctx.currentTime + start);
    gain.gain.linearRampToValueAtTime(volume, ctx.currentTime + start + 0.01);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + start + duration);
    osc.start(ctx.currentTime + start);
    osc.stop(ctx.currentTime + start + duration);
  };
  // Harmonics: 800Hz fundamental + 1200Hz + 1600Hz
  playTone(800, 0, 0.5, 0.3);
  playTone(1200, 0, 0.4, 0.15);
  playTone(1600, 0, 0.3, 0.1);
}
```

### 2. CSS Bell Vibration Animation
```css
@keyframes bellRing {
  0%, 100% { transform: rotate(0deg); }
  5% { transform: rotate(20deg); }
  10% { transform: rotate(-18deg); }
  15% { transform: rotate(16deg); }
  20% { transform: rotate(-14deg); }
  25% { transform: rotate(12deg); }
  30% { transform: rotate(-10deg); }
  35% { transform: rotate(8deg); }
  40% { transform: rotate(-6deg); }
  45% { transform: rotate(4deg); }
  50% { transform: rotate(0deg); }
}
.animate-bell-ring {
  animation: bellRing 0.8s ease-in-out infinite;
  transform-origin: top center;
}
```

### 3. Browser Notifications Pattern
```typescript
// Request permission first (requires user gesture)
const permission = await Notification.requestPermission();

// Schedule notification with setTimeout (tab must stay open!)
const msUntilDue = dueDateTime.getTime() - Date.now();
if (msUntilDue > 0) {
  setTimeout(() => {
    new Notification(title, { body, icon, requireInteraction: true });
  }, msUntilDue);
}

// Limitation: setTimeout only works while tab is open
// For true background notifications, need Service Workers + Push API
```

### 4. Recurring Task Auto-Reschedule Pattern
```python
def calculate_next_due_date(current_date: date, pattern: str) -> date:
    if pattern == "daily":
        return current_date + timedelta(days=1)
    elif pattern == "weekly":
        return current_date + timedelta(weeks=1)
    elif pattern == "biweekly":
        return current_date + timedelta(weeks=2)
    elif pattern == "monthly":
        year, month = current_date.year, current_date.month + 1
        if month > 12:
            month, year = 1, year + 1
        day = min(current_date.day, 28)  # Safe for all months
        return date(year, month, day)
    return current_date

# On task completion: advance due_date, keep is_complete=False
if task.recurrence_pattern and task.recurrence_pattern != "none":
    task.due_date = calculate_next_due_date(task.due_date, task.recurrence_pattern)
    task.is_complete = False  # Task stays incomplete, date advances
```

### 5. Database Migration Without Alembic
```python
def run_migrations():
    migrations = [
        ("tasks", "due_time", "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS due_time VARCHAR(5)"),
        ("tasks", "recurrence_pattern", "ALTER TABLE tasks ADD COLUMN IF NOT EXISTS recurrence_pattern VARCHAR(10) DEFAULT 'none'"),
    ]
    with Session(engine) as session:
        for table, column, sql in migrations:
            session.exec(text(sql))
            session.commit()
```

### 6. Client-Side Sorting with useMemo
```typescript
const sortedTasks = useMemo(() => {
  return [...tasks].sort((a, b) => {
    let cmp = 0;
    switch (sortBy) {
      case "priority":
        const order = { high: 0, medium: 1, low: 2 };
        cmp = order[a.priority] - order[b.priority];
        break;
      case "due_date":
        if (!a.due_date) cmp = 1;
        else if (!b.due_date) cmp = -1;
        else cmp = a.due_date.localeCompare(b.due_date);
        break;
      // ... other cases
    }
    return sortOrder === "asc" ? cmp : -cmp;
  });
}, [tasks, sortBy, sortOrder]);
```

---

## Key Lessons Learned

### AKS/K8s Deployment Issues (2025-12-14)

| Issue | Root Cause | Solution |
|-------|------------|----------|
| "Please log in" after login | `useSecureCookies` based on NODE_ENV | Base on URL scheme: `BETTER_AUTH_URL.startsWith("https://")` |
| Pods not pulling new images | `latest` tag + unchanged spec = no restart | Add `kubectl rollout restart` to CD |
| "Cannot connect to backend" | CORS blocking nip.io origin | Add frontend URL to backend CORS origins |
| BETTER_AUTH_URL undefined | TypeScript optional property | Use nullish coalescing: `env.BETTER_AUTH_URL ?? "http://localhost:3000"` |

### Audio/Notifications (Phase V Part A)

| Issue | Solution |
|-------|----------|
| AudioContext limit | Reuse single shared instance |
| AudioContext suspended | Call `.resume()` before playing |
| setTimeout notifications | Only work when tab is open |
| Recurring tasks | Advance due_date, keep incomplete |
| Monthly date overflow | Use `min(day, 28)` for safety |

---

## Hackathon Completion Status

### All Phases Complete

| Phase | Status | Points |
|-------|--------|--------|
| **Phase I** | Console App (v1 + v2 TUI) | ✅ 100 |
| **Phase II** | Web App (Next.js + FastAPI) | ✅ 150 |
| **Phase III** | AI Chatbot + MCP Tools | ✅ 200 |
| **Phase IV** | Local K8s (Docker + Helm) | ✅ 150 |
| **Phase V Part A** | Advanced Features | ✅ 100 |
| **Phase V Part B** | Voice Chat (Bilingual) | ✅ 100 |
| **Phase V Part C** | Cloud (AKS + Dapr) | ✅ 200 |
| **Cloud-Native Blueprint** | Agent Skill | ✅ 200 |
| **Reusable Intelligence** | Full RI Framework | ✅ 200 |
| **Capstones** | Phase documents | ✅ 100 |
| **TOTAL** | | **~1600** |

### What Could Be Enhanced (Optional)

| Enhancement | Description | Benefit |
|-------------|-------------|---------|
| Redpanda Cloud | Connect to real Kafka cluster | Production-ready events |
| Custom Domain | Set up domain + HTTPS | Better OAuth URLs |
| HPA | Horizontal Pod Autoscaler | Auto-scaling |
| Monitoring | Prometheus + Grafana | Observability |

---

## Deployments

| Service | Platform | URL | Status |
|---------|----------|-----|--------|
| Frontend (v2) | Vercel | https://evolution-to-do.vercel.app | Live |
| Backend | Railway | https://evolutiontodo-production-e1b6.up.railway.app | Live |
| Database | Neon | PostgreSQL (v2.0.0 schema) | Connected |
| **Frontend (AKS)** | Azure AKS | http://172.171.119.133.nip.io:3000 | ✅ Live |
| **Backend (AKS)** | Azure AKS | http://48.200.16.149:8000 (LoadBalancer) | ✅ Live |
| CI/CD | GitHub Actions | Push → Build → Deploy → Restart | ✅ Active |

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
