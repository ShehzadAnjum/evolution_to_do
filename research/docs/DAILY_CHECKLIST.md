# Daily Pre-Work Checklist

**Purpose**: Run this checklist BEFORE starting work each day to maintain constitutional compliance and efficiency.

**Time Required**: 10 minutes
**Time Saved**: 30-60 minutes (context loading, preventing mistakes)
**ROI**: 3-6x return

---

## Instructions

1. Copy this template for today
2. Fill in the brackets [...]
3. Complete all checkboxes
4. If any checkbox fails → resolve before starting work
5. Keep daily checklists in `docs/daily-checklists/YYYY-MM-DD.md`

---

## Today's Checklist

**Date**: [YYYY-MM-DD]
**Day of Week**: [e.g., Monday]
**Phase**: [I / II / III / IV / V]
**Time Available Today**: [e.g., 4 hours]

---

## SECTION 1: Context Loading (5-10 minutes)

### 1.1 Read Essential Documents
- [ ] Read `docs/SESSION_HANDOFF.md` (5 min)
  - Last updated: [timestamp from file]
  - Current phase: [phase number]
  - Last session accomplishments: [quick note]
  - In progress: [task name]

- [ ] Skim `docs/PROJECT_STATUS.md` (2 min)
  - Overall progress: [X/5 phases]
  - Points accumulated: [X/1000]
  - Days to next deadline: [X days]

### 1.2 Check Repository State
- [ ] Run `git status`
  - Uncommitted changes: [Yes/No, count]
  - Current branch: [branch name]
  - If uncommitted: Should I commit or stash? [Decision]

- [ ] Review last commit
  ```bash
  git log -1 --oneline
  ```
  - Last commit: [message]
  - Date: [when]

- [ ] Check for new issues/PRs (if team project)
  - New issues: [count]
  - New PRs: [count]
  - Action needed: [Yes/No, what]

---

## SECTION 2: Constitutional Review (2-3 minutes)

### 2.1 Phase Alignment Check
- [ ] What phase am I in? [Phase I/II/III/IV/V]
- [ ] What are the phase boundaries?
  - **Allowed**: [list features/technologies for current phase]
  - **Prohibited**: [list features/technologies NOT in current phase]

### 2.2 Previous Work Completion Check
- [ ] Is previous task 100% complete? [Yes/No]
  - If **No**: What's incomplete? [description]
  - If **No**: Block new work, finish previous task first
  - If **Yes**: Ready for new task ✅

**Definition of 100% Complete**:
  - [ ] Code implemented and working
  - [ ] Tests passing (if applicable)
  - [ ] Deployed (if applicable)
  - [ ] Documented
  - [ ] Spec marked complete
  - [ ] No known blockers

### 2.3 Work In Progress (WIP) Limit Check
- [ ] How many tasks are "in progress"? [count]
  - **Maximum allowed**: 1 major task
  - If >1: Choose ONE to focus on, defer others

**Current WIP**:
  - Task: [name]
  - Started: [date]
  - Progress: [X%]
  - Blocker: [if any]

---

## SECTION 3: Plan Check (2-3 minutes)

### 3.1 Today's Work Definition
- [ ] What am I working on today? [task name]
- [ ] Where is this specified? [path to spec file]
- [ ] Is this in current phase spec? [Yes/No]
  - If **No**: STOP. Work on current phase tasks only.

### 3.2 Dependency Check
- [ ] Do I have all dependencies for this task? [Yes/No]
  - Dependencies needed: [list]
  - Missing: [list]
  - If missing: Implement dependencies first OR defer task

### 3.3 Feature Necessity Test (if starting new feature)
- [ ] Is this a NEW feature? [Yes/No]
- If **Yes**, run feature necessity test:
  ```bash
  scripts/check-feature-necessity.sh
  ```
  - Result: [Proceed / Defer]
  - If Defer: Work on different task

### 3.4 Time Estimation
- [ ] Estimated time for today's task: [X hours]
- [ ] Time available today: [Y hours]
- [ ] Is X ≤ Y? [Yes/No]
  - If **No**: Reduce scope OR continue tomorrow

---

## SECTION 4: Tool Check (if using new tool today)

### 4.1 New Tool Today?
- [ ] Am I using a NEW tool/library/framework today? [Yes/No]
- If **Yes**: Tool name: [name]

### 4.2 Documentation-First Check (if new tool)
- [ ] Have I read the official documentation? [Yes/No]
- If **No**: STOP. Read documentation first (30 min minimum)
- If **Yes**: When? [date/time]

**Run Before New Tool Checklist**:
```bash
# Copy template
cp docs/BEFORE_NEW_TOOL.md docs/tools/[tool-name]-checklist.md

# Fill out and complete
vim docs/tools/[tool-name]-checklist.md
```

**Reminder**: Skipping documentation for better-auth cost 6-8 hours debugging in previous project.

### 4.3 30-Minute Reading Commitment
- [ ] Official quick start guide (10 min): [✅ / ⏳]
- [ ] Version compatibility check (5 min): [✅ / ⏳]
- [ ] Common issues review (5 min): [✅ / ⏳]
- [ ] API reference for my use case (10 min): [✅ / ⏳]

---

## SECTION 5: Ready to Start (Final Checks)

### 5.1 Pre-Start Checklist
- [ ] Context loaded (Section 1 complete)
- [ ] Constitution reviewed (Section 2 complete)
- [ ] Plan clear (Section 3 complete)
- [ ] Tools ready (Section 4 complete or N/A)

### 5.2 Session Setup
- [ ] Clear goal for today: [write goal in one sentence]
- [ ] Success criteria: [how I'll know I succeeded]
- [ ] Backup plan if blocked: [what to work on if stuck]

### 5.3 Time Blocking
- [ ] Time blocked on calendar: [start time] - [end time]
- [ ] Distractions minimized (notifications off, etc.)
- [ ] SESSION_HANDOFF.md open in editor (for end-of-session update)

### 5.4 Final Go/No-Go
- [ ] **READY TO START**: [✅ Yes / ❌ No]

**If No**: Resolve blockers listed above before starting work.

**If Yes**: Start working! 🚀

---

## SECTION 6: Session End (After Work)

### 6.1 Commit Changes
- [ ] All changes committed with clear message
  ```bash
  git status
  git add [files]
  git commit -m "[type]: [clear description]"
  ```
  - Commit message: [message]
  - Files changed: [count]

### 6.2 Update Context Documents
- [ ] Update `docs/SESSION_HANDOFF.md` (5 min)
  - Updated "Last Updated" timestamp
  - Added what accomplished
  - Updated "What's Next" priorities
  - Updated current phase/branch

- [ ] Update `docs/PROJECT_STATUS.md` (if major milestone)
  - Major milestone achieved: [Yes/No, what]

### 6.3 Mark Progress
- [ ] Update task tracker (if exists)
- [ ] Mark checkboxes in spec files
- [ ] Update phase completion percentage

### 6.4 Plan Tomorrow
- [ ] Top 3 priorities for tomorrow:
  1. [priority 1]
  2. [priority 2]
  3. [priority 3]

### 6.5 Time Tracking
- [ ] Time worked today: [X hours]
- [ ] Time effective (productive): [Y hours]
- [ ] Time wasted (debugging, context loss): [Z hours]
- [ ] Efficiency: [Y/X × 100]% (Target: >80%)

**Waste Analysis** (if efficiency <80%):
- Wasted on: [what]
- Root cause: [why]
- Prevention: [how to avoid]

### 6.6 Learnings & Reflections
- [ ] What went well: [note]
- [ ] What didn't go well: [note]
- [ ] What I learned: [note]
- [ ] What to do differently: [note]

---

## Red Flag Detection

**Check for any red flags** (if any exist, invoke emergency protocol):

- [ ] Behind schedule (2+ days behind): [Yes/No]
- [ ] Multiple WIP tasks (>1): [Yes/No]
- [ ] SESSION_HANDOFF not updated 2+ days: [Yes/No]
- [ ] Build artifacts in git: [Yes/No]
- [ ] Phase boundary violated: [Yes/No]
- [ ] Documentation not read before tool: [Yes/No]
- [ ] Efficiency <80%: [Yes/No]
- [ ] Quality issues (features broken): [Yes/No]

**Red Flags Detected**: [count]

**If any red flags**:
1. Stop immediately
2. Review `specs/CONSTITUTION.md` emergency protocols
3. Identify root cause
4. Correct course
5. Document lesson in `docs/lessons/[date]-[topic].md`

---

## Daily Metrics Summary

**Completion**:
- All checkboxes completed: [Yes/No]
- Ready to start: [Yes/No]
- Session productive: [Yes/No]

**Time**:
- Checklist time: [X min] (target: 10 min)
- Work time: [Y hours]
- Effective time: [Z hours]
- Efficiency: [Z/Y × 100]%

**Compliance**:
- Constitutional compliance: [Yes/No]
- Session handoff updated: [Yes/No]
- Repository clean: [Yes/No]

---

## Template for Tomorrow

```bash
# Copy this template for tomorrow
cp docs/DAILY_CHECKLIST.md docs/daily-checklists/$(date +%Y-%m-%d).md

# Edit tomorrow's checklist
vim docs/daily-checklists/$(date +%Y-%m-%d).md
```

---

## Notes

**Why This Checklist Exists**: Previous project lost 30-60 min per session reloading context, and made costly mistakes like not reading documentation (6-8 hours wasted).

**Time Investment**: 10 minutes daily
**Time Saved**: 30-60 minutes daily
**ROI**: 3-6x return

**This checklist is not overhead. It's an efficiency multiplier.**

---

**Checklist Version**: 1.0.0
**Last Updated**: December 4, 2025
**Part of**: Evolution of Todo Constitutional Framework
