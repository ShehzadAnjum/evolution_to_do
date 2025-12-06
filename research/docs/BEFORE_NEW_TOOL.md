# Before Using New Tool Checklist

**Purpose**: Prevent wasting 6-8 hours debugging by spending 30 minutes reading documentation first.

**Lesson from Previous Project**: Skipped better-auth documentation → manually created wrong schema → 6-8 hours debugging. **30 minutes of reading would have saved 6 hours.**

**Rule**: Complete this checklist BEFORE using any new tool, library, or framework.

---

## Tool Information

**Tool Name**: _______________________________________________

**Date**: _____________________________________________________

**Phase**: [I / II / III / IV / V]

**Why I Need This Tool**: ___________________________________
_______________________________________________________________

**Alternatives Considered**: ___________________________________
_______________________________________________________________

---

## PART 1: Research Phase (30 minutes minimum)

### Step 1: Official Quick Start Guide (10 minutes)

- [ ] Found official documentation URL: _______________________________________________

- [ ] Read quick start / getting started guide (10 min)

**Key Takeaways** (write 3-5 bullet points):
- _______________________________________________________________
- _______________________________________________________________
- _______________________________________________________________
- _______________________________________________________________
- _______________________________________________________________

**Official Installation Command** (copy exact command from docs):
```bash
_______________________________________________________________
```

---

### Step 2: Version Compatibility Check (5 minutes)

- [ ] What versions are my current tools?
  - Node.js: _______________
  - Python: _______________
  - npm/pnpm/yarn: _______________
  - Other: _______________

- [ ] What versions does this new tool require?
  - Minimum: _______________
  - Recommended: _______________
  - Maximum: _______________

- [ ] Are my versions compatible? [✅ Yes / ❌ No]

- [ ] If No, what needs upgrading?
  - Tool to upgrade: _______________
  - From version: _______________ → To version: _______________
  - Risk of upgrading: [Low / Medium / High]

---

### Step 3: Common Issues / Troubleshooting Review (5 minutes)

- [ ] Found "Troubleshooting" or "Common Issues" section: [✅ Yes / ❌ No]
  - URL: _______________________________________________

**Common Issues I Might Hit** (write 3-5 issues + solutions):
1. **Issue**: _______________________________________________________________
   **Solution**: _______________________________________________________________

2. **Issue**: _______________________________________________________________
   **Solution**: _______________________________________________________________

3. **Issue**: _______________________________________________________________
   **Solution**: _______________________________________________________________

4. **Issue**: _______________________________________________________________
   **Solution**: _______________________________________________________________

5. **Issue**: _______________________________________________________________
   **Solution**: _______________________________________________________________

---

### Step 4: API Reference for My Use Case (10 minutes)

**My Use Case** (what I'm trying to do): _______________________________________________
_______________________________________________________________

- [ ] Read API documentation for relevant features (10 min)
  - URL: _______________________________________________

**Key APIs I'll Use**:
1. API/Function: _______________
   Purpose: _______________________________________________________________
   Parameters: _______________________________________________________________
   Returns: _______________________________________________________________

2. API/Function: _______________
   Purpose: _______________________________________________________________
   Parameters: _______________________________________________________________
   Returns: _______________________________________________________________

3. API/Function: _______________
   Purpose: _______________________________________________________________
   Parameters: _______________________________________________________________
   Returns: _______________________________________________________________

**Example Code from Docs** (copy official example):
```python / javascript / bash
_______________________________________________________________
_______________________________________________________________
_______________________________________________________________
```

---

### Step 5: Recent Issues Check (5 minutes)

- [ ] Checked GitHub issues for this tool: [✅ Yes / ❌ No]
  - GitHub URL: _______________________________________________

- [ ] Filtered by: [⚠️ Open issues / 🐛 Bugs / 💬 Recent discussions]

**Recent Problems People Are Having**:
1. Issue: _______________________________________________________________
   Status: [Open / Closed / Workaround available]
   Relevance to me: [High / Medium / Low]

2. Issue: _______________________________________________________________
   Status: [Open / Closed / Workaround available]
   Relevance to me: [High / Medium / Low]

3. Issue: _______________________________________________________________
   Status: [Open / Closed / Workaround available]
   Relevance to me: [High / Medium / Low]

**Known Workarounds** (if any issues affect me):
- _______________________________________________________________
- _______________________________________________________________

---

## PART 2: Implementation Planning (10 minutes)

### Step 6: Official Example/Template

- [ ] Does official documentation provide example/template? [✅ Yes / ❌ No]

**If Yes**:
- Example URL: _______________________________________________
- Example repo (if exists): _______________________________________________
- [ ] Downloaded / cloned example
- [ ] Tested example locally
- [ ] Example works: [✅ Yes / ❌ No]

**If No**:
- Plan to start from: _______________________________________________

---

### Step 7: Testing Strategy

**How I'll Test This Tool** (before integrating into main project):

- [ ] Test in isolation first (separate test project/file)
  - Test project location: _______________________________________________

- [ ] Test with minimal example
  - What I'll test: _______________________________________________________________

- [ ] Verify basic functionality works
  - Success criteria: _______________________________________________________________

- [ ] Only then integrate into main project

**Isolation Test Plan**:
```bash
# Commands to test in isolation
_______________________________________________________________
_______________________________________________________________
_______________________________________________________________
```

---

### Step 8: Deviation Documentation

**Will I deviate from official documentation?** [Yes / No]

**If Yes, why?**:
- Reason: _______________________________________________________________
- Risk: [Low / Medium / High]
- Backup plan if this fails: _______________________________________________________________

**Deviations**:
1. **Official approach**: _______________________________________________________________
   **My approach**: _______________________________________________________________
   **Why different**: _______________________________________________________________

2. **Official approach**: _______________________________________________________________
   **My approach**: _______________________________________________________________
   **Why different**: _______________________________________________________________

---

## PART 3: Safety Checks

### Step 9: Security Review (if applicable)

- [ ] Does this tool require API keys / secrets? [Yes / No]

**If Yes**:
- [ ] How to store securely? [Environment variables / Secret manager / Other: ___]
- [ ] Added to `.env.example`: [✅ Yes / ⏳ TODO]
- [ ] Verified `.env` in `.gitignore`: [✅ Yes / ⚠️ Need to add]

- [ ] Does this tool have known security vulnerabilities?
  - Checked: [npm audit / pip safety / other: _______________]
  - Result: [✅ Safe / ⚠️ Warnings / ❌ Critical issues]

---

### Step 10: License Check

- [ ] What license does this tool have? _______________________________________________

- [ ] Is it compatible with my project license? [✅ Yes / ❌ No / ⚠️ Unsure]

- [ ] Any usage restrictions? _______________________________________________________________

---

## PART 4: Ready to Implement

### Final Checklist

- [ ] Official documentation read (30 min minimum)
- [ ] Version compatibility verified
- [ ] Common issues reviewed
- [ ] API reference for my use case read
- [ ] Recent GitHub issues checked
- [ ] Testing strategy defined
- [ ] Security considerations addressed
- [ ] License compatible

**Total Time Spent on Research**: _____ minutes (minimum 30)

**Am I Ready to Use This Tool?** [✅ Yes / ❌ No]

**If No, what's missing?**:
- _______________________________________________________________

**If Yes, next steps**:
1. _______________________________________________________________
2. _______________________________________________________________
3. _______________________________________________________________

---

## PART 5: During Implementation

### Implementation Notes

**Started**: [Date & Time]

**Installation Command Used**:
```bash
_______________________________________________________________
```

**Installation Result**: [✅ Success / ❌ Failed]

**If Failed**:
- Error message: _______________________________________________________________
- Solution tried: _______________________________________________________________
- Result: _______________________________________________________________

---

### First Test

**Test Performed**: _______________________________________________________________

**Expected Result**: _______________________________________________________________

**Actual Result**: _______________________________________________________________

**Match?** [✅ Yes / ❌ No]

**If No**:
- [ ] Re-read documentation (don't assume I understood)
- [ ] Search official GitHub issues
- [ ] Ask in official community/Discord
- [ ] Then debug on my own

---

## PART 6: If Stuck After 30 Minutes

**30-Minute Rule**: If debugging for 30 minutes without progress, STOP and follow this protocol.

### Debugging Protocol

**Time Started Debugging**: [Time]

**Time When Stuck** (30 min later): [Time]

**Problem Description**: _______________________________________________________________
_______________________________________________________________

**What I Tried**:
1. _______________________________________________________________
2. _______________________________________________________________
3. _______________________________________________________________

### Mandatory Steps (in order)

- [ ] **Step 1**: Re-read documentation (assume I misunderstood)
  - What I missed: _______________________________________________________________
  - Did this fix it? [Yes / No]

- [ ] **Step 2**: Search official GitHub issues
  - Search query: _______________________________________________
  - Found similar issue: [Yes / No]
  - Issue URL: _______________________________________________
  - Solution: _______________________________________________________________
  - Did this fix it? [Yes / No]

- [ ] **Step 3**: Ask in official community/Discord
  - Community URL: _______________________________________________
  - Question posted: [Yes / No]
  - Response: _______________________________________________________________
  - Did this fix it? [Yes / No]

- [ ] **Step 4**: Stack Overflow search
  - Query: _______________________________________________
  - Found answer: [Yes / No]
  - URL: _______________________________________________
  - Did this fix it? [Yes / No]

- [ ] **Step 5**: Only then debug on my own
  - Hypothesis: _______________________________________________________________
  - Test: _______________________________________________________________
  - Result: _______________________________________________________________

---

## PART 7: Success & Documentation

### When It Works

**Successful Implementation**: [✅ Yes / ⏳ In Progress]

**Total Time Spent**:
- Reading docs: _____ min
- Testing in isolation: _____ min
- Debugging: _____ min
- Integration: _____ min
- **Total**: _____ min

**Time Saved by Reading Docs First**: Estimated _____ hours
(Based on better-auth: 30 min reading saved 6-8 hours debugging)

---

### Document for Future

**Create Tool Knowledge Base**: `docs/tools/[tool-name]-guide.md`

**Include**:
- [ ] Setup instructions (exact commands that worked)
- [ ] Common gotchas I encountered
- [ ] Solutions to problems I hit
- [ ] Code examples that work
- [ ] Links to useful resources

**Template**:
```markdown
# [Tool Name] Guide

## Setup
[Exact commands]

## Common Issues
[Problems I hit + solutions]

## Working Examples
[Code that works]

## Resources
[Useful links]

## Created
[Date]

## Last Updated
[Date]
```

---

## Summary & Reflection

### What Went Well
- _______________________________________________________________

### What Didn't Go Well
- _______________________________________________________________

### What I Learned
- _______________________________________________________________

### What I'd Do Differently
- _______________________________________________________________

### Advice for Future Self
- _______________________________________________________________

---

## Checklist Archive

**Save completed checklists**: `docs/tools/[tool-name]-checklist-[date].md`

**Why**: Reference for next time, or when helping others with same tool.

---

## Constitutional Reminder

**Principle III: Documentation First (30-Minute Rule)**

> Before using any new tool, spend 30 minutes reading official documentation.
>
> **Cost of skipping**: 6-8 hours debugging (proven by better-auth experience)
>
> **30-minute rule**: If debugging for 30 minutes, STOP and read documentation.

**This checklist enforces Principle III.**

---

**Checklist Version**: 1.0.0
**Created**: December 4, 2025
**Part of**: Evolution of Todo Constitutional Framework
**Estimated Time**: 30-45 minutes (research) + implementation time
**Time Saved**: 6+ hours (based on empirical evidence)
**ROI**: 8-12x return on time invested
