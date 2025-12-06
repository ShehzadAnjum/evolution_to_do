# Quickstart: Phase I Console Todo Application

**Feature**: 001-phase1-console-todo
**Date**: 2025-12-05
**Status**: Complete

## Prerequisites

Before running the application, ensure you have:

1. **Python 3.13+** installed
   ```bash
   python --version
   # Should show Python 3.13.x or higher
   ```

2. **UV package manager** installed
   ```bash
   # Install UV (if not already installed)
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Verify installation
   uv --version
   ```

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd evolution_to_do
```

### 2. Switch to Feature Branch

```bash
git checkout 001-phase1-console-todo
```

### 3. Install Dependencies

```bash
cd backend
uv sync
```

## Running the Application

### Start the Todo App

```bash
# From the backend directory
uv run python -m src.main
```

### Expected Output

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

## Example Usage Session

### Adding Tasks

```
Enter choice (1-6): 1

Enter task title: Buy groceries
Enter description (optional, press Enter to skip): Milk, eggs, bread

✓ Task added successfully!
  ID: 1
  Title: Buy groceries
  Description: Milk, eggs, bread

Press Enter to continue...
```

### Viewing Tasks

```
Enter choice (1-6): 2

╔════════════════════════════════════════════════════════╗
║                    Your Tasks                          ║
╠════════════════════════════════════════════════════════╣
║                                                        ║
║  [ ] ID: 1 - Buy groceries                            ║
║      Description: Milk, eggs, bread                    ║
║                                                        ║
║  [ ] ID: 2 - Call mom                                 ║
║      Description: None                                 ║
║                                                        ║
╠════════════════════════════════════════════════════════╣
║  Total: 2 tasks | Completed: 0 | Remaining: 2         ║
╚════════════════════════════════════════════════════════╝

Press Enter to continue...
```

### Marking Task Complete

```
Enter choice (1-6): 3

Enter task ID to toggle completion: 1

✓ Task marked as complete!
  ID: 1
  Title: Buy groceries
  Status: Complete

Press Enter to continue...
```

### Updating a Task

```
Enter choice (1-6): 4

Enter task ID to update: 2

Current task:
  Title: Call mom
  Description: None

Enter new title (press Enter to keep current): Call mom and dad
Enter new description (press Enter to keep current): Sunday afternoon

✓ Task updated successfully!
  ID: 2
  Title: Call mom and dad
  Description: Sunday afternoon

Press Enter to continue...
```

### Deleting a Task

```
Enter choice (1-6): 5

Enter task ID to delete: 1

Task to delete:
  ID: 1
  Title: Buy groceries

Are you sure you want to delete this task? (y/n): y

✓ Task deleted successfully!

Press Enter to continue...
```

### Exiting

```
Enter choice (1-6): 6

╔════════════════════════════════════╗
║     Thank you for using Todo!      ║
║            Goodbye!                ║
╚════════════════════════════════════╝
```

## Running Tests

```bash
# From the backend directory
uv run pytest tests/ -v

# With coverage report
uv run pytest tests/ -v --cov=src --cov-report=term-missing
```

## Troubleshooting

### Python Version Error

```
Error: Python 3.13+ is required
```

**Solution**: Install Python 3.13 or higher from [python.org](https://python.org) or use pyenv.

### UV Not Found

```
uv: command not found
```

**Solution**: Install UV:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc  # or restart terminal
```

### Module Not Found

```
ModuleNotFoundError: No module named 'src'
```

**Solution**: Run from the `backend` directory:
```bash
cd backend
uv run python -m src.main
```

## Project Structure

```
backend/
├── src/
│   ├── __init__.py
│   ├── main.py              # Entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task dataclass
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_store.py    # In-memory storage
│   ├── cli/
│   │   ├── __init__.py
│   │   ├── menu.py          # Menu display
│   │   ├── handlers.py      # Operation handlers
│   │   └── formatters.py    # Output formatting
│   └── lib/
│       ├── __init__.py
│       └── validators.py    # Input validation
├── tests/
│   ├── unit/
│   │   ├── test_task.py
│   │   └── test_task_store.py
│   └── integration/
│       └── test_cli.py
├── pyproject.toml
└── README.md
```

## Success Criteria Verification

After installation, verify these criteria:

| Criteria | How to Verify |
|----------|---------------|
| SC-001: Complete workflow < 60s | Time yourself: add → view → complete → update → delete |
| SC-002: 95% first-attempt success | Try each operation - should work first time |
| SC-003: Clear error messages | Enter invalid input - error should explain how to fix |
| SC-004: Instant response | All operations should feel immediate |
| SC-005: 100+ tasks | Add many tasks - performance should not degrade |
| SC-006: Understand options in 10s | Look at menu - options should be obvious |

## Next Steps

After verifying the application works:

1. ✅ All 5 operations working
2. ✅ Tests passing
3. 📹 Record demo video (< 90 seconds)
4. 📝 Run phase gate check
5. 📤 Submit via form
6. ➡️ Proceed to Phase II
