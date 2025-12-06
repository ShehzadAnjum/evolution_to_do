<!--
================================================================================
SYNC IMPACT REPORT - Constitution v1.1.0 Add Reusable Intelligence Principle
================================================================================
Date: 2025-12-05
Version: 1.0.0 → 1.1.0 (MINOR)
Action: Add Principle IX - Reusable Intelligence

VERSION CHANGES:
- Previous Version: 1.0.0
- Current Version: 1.1.0
- Version Bump Type: MINOR (new principle added)

PRINCIPLES (9 Core Principles - 1 ADDED):
1. Phase Boundaries Are Hard Gates
2. Complete Before Proceeding
3. Documentation-First Development
4. Context Preservation Protocol
5. Repository Hygiene from Day One
6. Spec-Driven Development
7. Value-Driven Feature Selection
8. Quality Over Speed
9. Reusable Intelligence (NEW)

CHANGES MADE:
1. Added Principle IX: Reusable Intelligence
   - Mandates extraction of reusable components
   - Covers subagents, skills, utilities, patterns
   - Enables cross-phase and cross-project reuse
   - Includes reusability checklist
2. Added Reusable Assets section under Phase Evolution Framework
3. Updated version to 1.1.0

TEMPLATE SYNCHRONIZATION STATUS:
✅ .specify/templates/spec-template.md - Compatible
✅ .specify/templates/plan-template.md - Compatible (may add reusability check)
✅ .specify/templates/tasks-template.md - Compatible
✅ .specify/templates/phr-template.prompt.md - Compatible

FILES UPDATED:
✅ .specify/memory/constitution.md - This file

COMMIT MESSAGE SUGGESTION:
docs: amend constitution to v1.1.0 (add Reusable Intelligence principle)

- Added Principle IX: Reusable Intelligence
- Mandates extraction of reusable components across phases
- Enables subagents, skills, and patterns for cross-project use
- Added Reusable Assets tracking section
- Version bump: 1.0.0 → 1.1.0 (MINOR - new principle)

================================================================================
-->

# Evolution of Todo Constitution

## Core Principles

### I. Phase Boundaries Are Hard Gates

Each phase represents a complete, deployable increment of the system. A phase MUST be 100% complete before ANY work on the subsequent phase begins.

**Non-Negotiable Rules**:
- Phase N MUST be fully implemented, tested, and submitted before Phase N+1 starts
- Features belonging to future phases are PROHIBITED in current phase scope
- Phase completion requires: all features working, documented, and submitted via official channels
- No "partial phase" work or preview implementations allowed

**Rationale**: Previous projects failed by mixing phase concerns, resulting in incomplete deliverables. Hard gates ensure each milestone delivers complete value before expanding scope.

### II. Complete Before Proceeding

Only ONE major task may be in-progress at any time. A task MUST reach 100% completion before starting the next task.

**Non-Negotiable Rules**:
- Work-in-progress limit: exactly ONE major task
- "95% complete" equals zero value delivered - completion means deployed and verified
- Tasks MUST be marked complete only when: code merged, tests passing, deployed, documented
- Context switching between incomplete tasks is PROHIBITED

**Rationale**: Partially completed work delivers no user value. Completing tasks fully ensures incremental progress and prevents accumulation of unfinished work.

### III. Documentation-First Development

Before using any new tool, library, or service, a minimum of 30 minutes MUST be spent reading official documentation.

**Non-Negotiable Rules**:
- Read official quick-start guide before implementation begins
- Review compatibility requirements and known issues
- Document key learnings and gotchas discovered
- If debugging exceeds 30 minutes, STOP and re-read documentation

**Rationale**: Skipping documentation has proven to cost 6-10x the reading time in debugging. 30 minutes reading saves hours of troubleshooting.

### IV. Context Preservation Protocol

Session context MUST be captured and preserved to enable efficient continuation of work across sessions.

**Non-Negotiable Rules**:
- Update session handoff documentation at the end of EVERY work session
- Document: what was accomplished, what was learned, what's next (prioritized)
- Include: current blockers, recent decisions with rationale, essential file changes
- Time investment: 5-10 minutes per session

**Rationale**: Context loss costs 30-60 minutes per session reload. 5-minute updates provide 6-12x return on time invested.

### V. Repository Hygiene from Day One

The repository MUST maintain cleanliness and organization from the first commit throughout the project lifecycle.

**Non-Negotiable Rules**:
- Configure ignore patterns BEFORE first commit (build outputs, dependencies, secrets)
- NEVER commit secrets, credentials, or environment-specific configurations
- Organize documentation in designated directories, not at repository root
- Delete merged branches promptly; maintain only active development branches
- Perform weekly cleanup reviews

**Rationale**: Repository mess compounds over time. Early discipline prevents future cleanup burden and security risks.

### VI. Spec-Driven Development

Human defines specifications; implementation follows specifications exactly. Specifications are the single source of truth.

**Non-Negotiable Rules**:
- All features MUST have written specifications before implementation begins
- Implementation MUST match specification exactly - no scope additions
- When spec is wrong, update the spec FIRST, then re-implement
- Manual code editing without spec reference is PROHIBITED except for bug fixes
- Use SpecKit workflow: `/sp.specify` → `/sp.plan` → `/sp.tasks` → implement

**Rationale**: Specifications provide clarity, enable AI-assisted implementation, and prevent scope creep. Spec-first ensures thinking before coding.

### VII. Value-Driven Feature Selection

Every feature MUST deliver immediate, demonstrable value within current phase constraints.

**Non-Negotiable Rules**:
- Feature MUST be in current phase scope (not future phase)
- Feature MUST have all prerequisites available (not dependent on unbuilt components)
- Feature MUST work with current functionality (not theoretical future state)
- Feature MUST be specified before implementation begins

**Decision Test**: If ANY condition fails, DEFER the feature.

**Rationale**: Building for hypothetical futures wastes effort. Features must deliver value NOW with current capabilities.

### VIII. Quality Over Speed

Each phase MUST be production-ready at its scope level. Quality CANNOT be sacrificed to meet deadlines.

**Non-Negotiable Rules**:
- "Works on my machine" is NOT acceptable - must be deployable and demonstrable
- Known bugs MUST be fixed before phase completion
- If deadline pressure exists, reduce SCOPE not QUALITY
- Each phase represents a complete, demo-ready product at that evolution stage

**Rationale**: Buggy or incomplete deliverables have zero value. A smaller scope done excellently beats a larger scope done poorly.

### IX. Reusable Intelligence

Every implementation MUST be evaluated for reusability. Reusable components, subagents, skills, and patterns MUST be extracted and documented for cross-phase and cross-project use.

**Non-Negotiable Rules**:
- Before implementing, check if a reusable component already exists
- After implementing, evaluate if the solution can be generalized
- Reusable components MUST be self-contained, independently testable, and documented
- Subagents and skills MUST have clear interfaces and be project-agnostic where possible
- Patterns and utilities MUST be extracted to dedicated locations (e.g., `lib/`, `skills/`, `agents/`)

**Reusability Checklist** (apply during planning and implementation):
- [ ] Can this logic serve multiple features within this project?
- [ ] Can this component be used in future phases without modification?
- [ ] Can this be extracted as a standalone skill or subagent?
- [ ] Would other projects benefit from this implementation?
- [ ] Is this a pattern worth documenting for future reference?

**Types of Reusable Assets**:

| Type | Description | Location |
|------|-------------|----------|
| **Subagents** | Specialized AI agents for specific tasks | `agents/` or `.specify/agents/` |
| **Skills** | Reusable capabilities/prompts for AI assistants | `skills/` or `.specify/skills/` |
| **Utilities** | Helper functions and common operations | `lib/` or `src/lib/` |
| **Patterns** | Documented architectural/design patterns | `docs/patterns/` |
| **Templates** | Reusable file/code templates | `.specify/templates/` |
| **Scripts** | Automation and workflow scripts | `scripts/` or `.specify/scripts/` |

**Extraction Triggers**:
- Same logic appears in 2+ places → Extract to utility
- Same prompt pattern used 2+ times → Extract to skill
- Complex multi-step AI workflow → Extract to subagent
- Same architectural decision across features → Document as pattern

**Rationale**: Building once and reusing multiplies value. Extracted components reduce future development time, ensure consistency, and create a growing library of proven solutions. This compounds across phases and projects, turning each implementation into an investment.

## Phase Evolution Framework

The project evolves through five distinct phases, each building upon the previous while maintaining hard boundaries.

### Phase Structure

| Phase | Focus | Key Deliverables |
|-------|-------|------------------|
| I | Foundation | Core operations, basic interface, session storage |
| II | Persistence & Users | Data persistence, user management, web interface |
| III | Intelligence | AI-powered interactions, natural language interface |
| IV | Containerization | Deployment packaging, orchestration readiness |
| V | Cloud & Advanced | Cloud deployment, event-driven features, advanced capabilities |

### Phase Transition Requirements

Before transitioning from Phase N to Phase N+1:

1. **Functional Completeness**: All phase N features implemented and working
2. **Documentation Completeness**: User-facing documentation accurate and complete
3. **Submission Completeness**: Phase submitted via official channels with demo
4. **Verification**: Phase gate checklist executed and passing
5. **Reusability Review**: Reusable components identified and extracted

### Scope Boundaries

Each phase has explicit scope boundaries:
- **In Scope**: Features and capabilities defined for that phase
- **Out of Scope**: Features belonging to later phases (even if technically feasible)
- **Non-Goals**: Explicitly excluded items that will never be implemented

### Reusable Assets Inventory

Track reusable components created during each phase:

| Phase | Asset | Type | Reuse Potential |
|-------|-------|------|-----------------|
| I | (To be identified) | - | - |
| II | (To be identified) | - | - |
| III | (To be identified) | - | - |
| IV | (To be identified) | - | - |
| V | (To be identified) | - | - |

*Update this table as reusable assets are created.*

## Development Workflow

### Daily Workflow

**Session Start (10 minutes)**:
1. Read session handoff documentation
2. Review current phase and task status
3. Verify phase alignment for planned work
4. Run daily checklist

**During Work**:
1. Follow current phase specification
2. Apply documentation-first rule for new tools
3. Complete one task fully before starting another
4. Update session context at natural breakpoints
5. **Evaluate reusability** of implementations

**Session End (10 minutes)**:
1. Commit all changes with clear messages
2. Update session handoff documentation
3. Note blockers, decisions, and next priorities
4. **Log any new reusable components** created

### Weekly Workflow

**Weekly Review (30 minutes)**:
1. Assess phase progress against deadlines
2. Execute repository cleanup procedures
3. Update project status documentation
4. Identify and mitigate risks
5. **Review and update Reusable Assets Inventory**

### Feature Development Flow

```
/sp.specify → /sp.plan → /sp.tasks → implement → test → extract reusables → complete
```

1. **Specify**: Define what (user value, requirements, success criteria)
2. **Plan**: Define how (architecture, contracts, data model) + identify reuse opportunities
3. **Tasks**: Define work (ordered, dependency-aware task list)
4. **Implement**: Build according to plan and tasks
5. **Test**: Verify against specification
6. **Extract**: Identify and extract reusable components
7. **Complete**: Document, demo, submit

## Governance

### Constitution Authority

This constitution supersedes all other project practices and guidelines. When conflict exists between this constitution and other documents, this constitution prevails.

### Amendment Process

Amendments to this constitution MUST follow the established process:

1. **Initiation**: Use `/sp.constitution` command for all amendments
2. **Documentation**: Update Sync Impact Report with all changes
3. **Versioning**: Apply semantic versioning (MAJOR.MINOR.PATCH)
4. **Traceability**: Create PHR record for every amendment

### Version Numbering

- **MAJOR** (X.0.0): Breaking changes - principle removal or fundamental redefinition
- **MINOR** (0.X.0): Additions - new principles, sections, or material expansions
- **PATCH** (0.0.X): Refinements - clarifications, typo fixes, non-semantic changes

### Compliance Requirements

- All work MUST verify compliance with these principles
- Complexity beyond specification MUST be justified
- Constitutional violations require explicit override with documented rationale
- Overrides MUST be recorded and reviewed

### Override Protocol

When constitution must be overridden:

1. STOP current action
2. Document: which principle, why override needed, impact accepted
3. Choose: revert to compliance OR proceed with documented justification
4. Record override in project history for learning

**Version**: 1.1.0 | **Ratified**: 2025-12-05 | **Last Amended**: 2025-12-05
