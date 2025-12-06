---
id: 002
title: Add Reusable Intelligence Principle
stage: constitution
date: 2025-12-05
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: 001-phase1-console-todo
user: anjum
command: /sp.constitution
labels: [constitution, amendment, reusability, subagents, skills]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (governance document)
---

## Prompt

User requested to add Reusable Intelligence as a core principle to the constitution. Requirements:
- Create reusable components, subagents, and skills wherever possible
- Enable cross-phase and cross-project reuse
- Make this a non-negotiable principle in the constitution

## Response snapshot

Amended constitution from v1.0.0 → v1.1.0 with new Principle IX: Reusable Intelligence

**Principle IX - Reusable Intelligence** includes:

**Non-Negotiable Rules**:
- Check for existing reusable components before implementing
- Evaluate every implementation for reusability potential
- Extract reusable components to dedicated locations
- Ensure subagents/skills are self-contained and project-agnostic

**Reusability Checklist**:
- Can serve multiple features?
- Can be used in future phases?
- Can be extracted as standalone skill/subagent?
- Would other projects benefit?
- Worth documenting as pattern?

**Types of Reusable Assets**:
| Type | Location |
|------|----------|
| Subagents | `agents/` |
| Skills | `skills/` |
| Utilities | `lib/` |
| Patterns | `docs/patterns/` |
| Templates | `.specify/templates/` |
| Scripts | `scripts/` |

**Additional Updates**:
- Added "Reusability Review" to Phase Transition Requirements
- Added Reusable Assets Inventory table
- Updated Feature Development Flow to include "extract reusables" step
- Updated daily/weekly workflows with reusability checks

## Outcome

- ✅ Impact: All implementations now require reusability evaluation
- 🧪 Tests: N/A (governance document)
- 📁 Files: .specify/memory/constitution.md updated
- 🔁 Next prompts: Continue with /sp.plan for Phase I
- 🧠 Reflection: This principle turns every implementation into a long-term investment

## Evaluation notes (flywheel)

- Failure modes observed: None - clean amendment
- Graders run and results (PASS/FAIL): PASS - principle integrates with existing structure
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Apply reusability checklist during Phase I planning
