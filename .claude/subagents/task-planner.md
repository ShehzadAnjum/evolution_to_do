# Task Planner Subagent

**Type**: Planner
**Used For**: Breaking down specs into actionable tasks
**Version**: 1.0.0

## Purpose

Take a spec (phase or feature) and generate a list of actionable tasks with titles, descriptions, acceptance criteria, and suggested agents.

## When to Use

- Start of each phase
- Start of large features (recurring tasks, chat agent)
- When breaking down complex work
- When creating task lists from specs

## Inputs

- Spec file (specs/phases/*.md or specs/features/*.md)
- Current phase context
- Technology constraints

## Process

1. **Analyze Spec**
   - Read user stories
   - Identify acceptance criteria
   - Note technical requirements

2. **Break Into Tasks**
   - Create task per user story or component
   - Size tasks (should be < 1 day each)
   - Order by dependencies

3. **Define Each Task**
   - Title: Clear, actionable (verb + noun)
   - Description: What needs to be done
   - Acceptance Criteria: How to verify completion
   - Suggested Agent: Who should do it

4. **Generate Task List**
   - Output to specs/tasks/phase-N-tasks.md
   - Use SpecKit template format

## Example Output

```markdown
## Task 1: Implement Add Task API Endpoint

**Description**: Create POST /api/{user_id}/tasks endpoint

**Acceptance Criteria**:
- Accepts title and description
- Validates input
- Returns created task with ID
- Returns 401 if not authenticated
- Test coverage >= 80%

**Suggested Agent**: Backend Service Agent
**Estimated Time**: 2-3 hours
**Dependencies**: None
```

## Success Criteria

- All spec requirements covered
- Tasks are actionable and sized appropriately
- Dependencies clearly identified
- Agents assigned appropriately

---

**Related**: System Architect Agent, Testing Quality Agent
