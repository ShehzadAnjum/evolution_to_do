# Evolution Todo - Console App v1 (Basic)

A simple, basic console-based todo application demonstrating fundamental Python CLI patterns.

## Features

- **In-Memory Storage** - Tasks exist only during the session
- **Basic CRUD** - Add, View, Update, Delete tasks
- **Toggle Complete** - Mark tasks as done/undone
- **Simple Statistics** - Total, completed, pending counts

## Quick Start

```bash
# Run the app
cd /path/to/evolution_to_do
python -m console_app_v1.main
```

## Menu Options

```
--- Main Menu ---
1. View all tasks
2. Add new task
3. Update task
4. Delete task
5. Toggle complete
6. View statistics
0. Exit
```

## Project Structure

```
console_app_v1/
├── __init__.py      # Package init
├── main.py          # Entry point and menu loop
├── task.py          # Task class
├── task_manager.py  # Task operations (in-memory)
└── README.md        # This file
```

## Limitations (By Design)

This is the **basic v1 version** intentionally kept simple:

- No colors or emojis
- No persistence (tasks cleared on exit)
- No advanced features (priority, due dates, categories)
- Number-based navigation only

See `console_app_v2/` for the enhanced version with Textual TUI.

## Evolution Path

| Version | Features |
|---------|----------|
| **v1** (this) | Basic CLI, in-memory, plain text |
| **v2** | Textual TUI, JSON storage, advanced features |

## License

Part of Evolution Todo Hackathon II project.
