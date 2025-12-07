# CLI Interface Contract: Phase I Console Todo Application

**Feature**: 001-phase1-console-todo
**Date**: 2025-12-04
**Status**: Complete

## Overview

This document specifies the CLI interface contract for the Phase I console todo application. It defines all user interactions, input formats, and output formats.

## Main Menu

### Display Format

```
╔════════════════════════════════════╗
║       Todo Application v1.0        ║
╠════════════════════════════════════╣
║  1. Add Task                       ║
║  2. View Tasks                     ║
║  3. Mark Complete/Incomplete       ║
║  4. Update Task                    ║
║  5. Delete Task                    ║
║  6. Exit                           ║
╚════════════════════════════════════╝

Enter choice (1-6): _
```

**Requirements Mapped**: FR-001 (menu-driven interface with all operations)

### Menu Options

| Option | Action | Requirements |
|--------|--------|--------------|
| 1 | Add Task | FR-002 |
| 2 | View Tasks | FR-004, FR-011, FR-013 |
| 3 | Mark Complete/Incomplete | FR-005 |
| 4 | Update Task | FR-006 |
| 5 | Delete Task | FR-007 |
| 6 | Exit | FR-012 |

---

## Operation Contracts

### 1. Add Task

**Input Flow**:
```
Enter task title: _
Enter description (optional, press Enter to skip): _
```

**Success Output**:
```
✓ Task added successfully!
  ID: {id}
  Title: {title}
  Description: {description or "None"}

Press Enter to continue...
```

**Validation**:
- Title: Required, non-empty after trim
- Description: Optional, can be empty

**Error Cases**:
```
✗ Error: Task title cannot be empty.
Please enter a valid title.

Enter task title: _
```

**Requirements Mapped**: FR-002, US1

---

### 2. View Tasks

**Empty State Output**:
```
╔════════════════════════════════════╗
║           Your Tasks               ║
╠════════════════════════════════════╣
║  No tasks yet.                     ║
║  Add your first task with          ║
║  option 1!                         ║
╚════════════════════════════════════╝

Press Enter to continue...
```

**With Tasks Output**:
```
╔════════════════════════════════════════════════════════╗
║                    Your Tasks                          ║
╠════════════════════════════════════════════════════════╣
║                                                        ║
║  [ ] ID: 1 - Buy groceries                            ║
║      Description: Milk, eggs, bread                    ║
║                                                        ║
║  [✓] ID: 2 - Call mom                                 ║
║      Description: None                                 ║
║                                                        ║
║  [ ] ID: 3 - Finish project                           ║
║      Description: Complete Phase I todo app            ║
║                                                        ║
╠════════════════════════════════════════════════════════╣
║  Total: 3 tasks | Completed: 1 | Remaining: 2         ║
╚════════════════════════════════════════════════════════╝

Press Enter to continue...
```

**Status Indicators**:
- `[ ]` = Incomplete
- `[✓]` = Complete

**Requirements Mapped**: FR-004, FR-011, FR-013, US1

---

### 3. Mark Complete/Incomplete

**Input Flow**:
```
Enter task ID to toggle completion: _
```

**Success Output** (marking complete):
```
✓ Task marked as complete!
  ID: {id}
  Title: {title}
  Status: Complete

Press Enter to continue...
```

**Success Output** (marking incomplete):
```
✓ Task marked as incomplete!
  ID: {id}
  Title: {title}
  Status: Incomplete

Press Enter to continue...
```

**Error Cases**:
```
✗ Error: Task with ID {id} not found.
Please enter a valid task ID.

Enter task ID to toggle completion: _
```

```
✗ Error: Invalid input. Please enter a number.

Enter task ID to toggle completion: _
```

**Requirements Mapped**: FR-005, FR-008, US2

---

### 4. Update Task

**Input Flow**:
```
Enter task ID to update: _

Current task:
  Title: {current_title}
  Description: {current_description or "None"}

Enter new title (press Enter to keep current): _
Enter new description (press Enter to keep current): _
```

**Success Output**:
```
✓ Task updated successfully!
  ID: {id}
  Title: {new_title or current_title}
  Description: {new_description or current_description or "None"}

Press Enter to continue...
```

**Validation**:
- Empty title input: Keep current title (FR-006, US3 Scenario 2)
- Empty description input: Keep current description (FR-006, US3 Scenario 3)
- Both provided: Update both (US3 Scenario 4)

**Error Cases**:
```
✗ Error: Task with ID {id} not found.
Please enter a valid task ID.

Enter task ID to update: _
```

**Requirements Mapped**: FR-006, FR-008, US3

---

### 5. Delete Task

**Input Flow**:
```
Enter task ID to delete: _

Task to delete:
  ID: {id}
  Title: {title}

Are you sure you want to delete this task? (y/n): _
```

**Success Output** (confirmed):
```
✓ Task deleted successfully!

Press Enter to continue...
```

**Cancelled Output**:
```
✗ Deletion cancelled.

Press Enter to continue...
```

**Error Cases**:
```
✗ Error: Task with ID {id} not found.
Please enter a valid task ID.

Enter task ID to delete: _
```

**Requirements Mapped**: FR-007, FR-008, US4

---

### 6. Exit

**Output**:
```
╔════════════════════════════════════╗
║     Thank you for using Todo!      ║
║          Goodbye! 👋               ║
╚════════════════════════════════════╝
```

**Requirements Mapped**: FR-012

---

## Error Message Templates

### Invalid Menu Selection

```
✗ Invalid choice. Please enter a number between 1 and 6.

Enter choice (1-6): _
```

**Requirements Mapped**: FR-009, Edge Case: Invalid menu selection

### Invalid Task ID

```
✗ Error: Task with ID {id} not found.
```

**Requirements Mapped**: FR-008, FR-009, Edge Case: Invalid task ID

### Empty Required Input

```
✗ Error: {field_name} cannot be empty.
```

**Requirements Mapped**: FR-009, Edge Case: Empty required input

### Non-Numeric Input

```
✗ Error: Invalid input. Please enter a number.
```

**Requirements Mapped**: FR-009

---

## Input Validation Rules

| Input | Validation | Error Response |
|-------|------------|----------------|
| Menu choice | Integer 1-6 | Re-prompt with error |
| Task ID | Positive integer, exists in store | Re-prompt with error |
| Task title | Non-empty after trim | Re-prompt with error |
| Task description | Any string (including empty) | Accept as-is |
| Confirmation (y/n) | 'y', 'Y', 'n', 'N' | Re-prompt with error |

---

## Display Constraints

| Element | Max Display Length | Behavior if Exceeded |
|---------|-------------------|---------------------|
| Title | 50 characters | Truncate with "..." |
| Description | 80 characters | Truncate with "..." |

**Requirements Mapped**: Edge Case: Very long input

---

## Accessibility Notes

1. All prompts end with `: ` to indicate input expected
2. Success messages start with `✓`
3. Error messages start with `✗`
4. Box drawing characters for visual structure
5. "Press Enter to continue" after each operation for clarity
