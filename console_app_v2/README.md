# Evolution Todo - Console App v2 (Enhanced TUI)

A beautiful, feature-rich console todo application with Textual TUI, arrow key navigation, and local storage.

## Features

- **Textual TUI** - Dark theme, arrow key navigation, modern interface
- **Sidebar** - Filter tasks by category (Work, Personal, Study, Shopping)
- **Filter Bar** - Search and priority filtering on top
- **Task Metadata** - Priority, due dates, categories, notes
- **JSON Persistence** - Tasks saved locally between sessions
- **Statistics Bar** - Track your productivity at a glance
- **Keyboard Shortcuts** - Fast task management with single keys

## Quick Start

```bash
# Install dependencies
cd /path/to/evolution_to_do/console_app_v2
uv venv && source .venv/bin/activate
uv pip install textual rich

# Run the Textual TUI (default)
python -m console_app_v2.main

# Or run legacy Rich CLI mode
python -m console_app_v2.main --cli
```

## Keyboard Shortcuts (TUI Mode)

| Key | Action |
|-----|--------|
| `a` | Add new task |
| `e` | Edit selected task |
| `d` | Delete selected task |
| `Space` | Toggle complete |
| `r` | Refresh task list |
| `q` | Quit application |
| `↑/↓` | Navigate tasks |

## TUI Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ Evolution Todo v2                              Task Management  │
├──────────────┬──────────────────────────────────────────────────┤
│ 📂 Categories│ 🔍 [Search...      ] Priority: [All ▼]          │
│ ───────────  │──────────────────────────────────────────────────│
│ 📋 All Tasks │ # │ Status │ Title          │ Priority │ Due    │
│ 💼 Work      │ 1 │ ⏳     │ Buy groceries  │ 🔴 High  │ Today  │
│ 🏠 Personal  │ 2 │ ✅     │ Submit report  │ 🟡 Med   │ -      │
│ 📚 Study     │ 3 │ ⚠️     │ Call dentist   │ 🟢 Low   │ Overdue│
│ 🛒 Shopping  │ ...                                              │
│ ───────────  ├──────────────────────────────────────────────────│
│ ✅ Completed │ 📊 Total: 5 │ ✅ Done: 2 │ ⏳ Pending: 2 │ ⚠️: 1 │
│ ⏳ Pending   └──────────────────────────────────────────────────┘
│ ⚠️ Overdue   │ a:Add e:Edit d:Delete Space:Toggle r:Refresh q:Quit
└──────────────┴──────────────────────────────────────────────────┘
```

## Task Properties

| Property | Options | Description |
|----------|---------|-------------|
| Title | Text (max 200) | Task name (required) |
| Notes | Text (max 1000) | Additional details |
| Priority | 🟢 Low, 🟡 Medium, 🔴 High | Task urgency |
| Category | 💼 Work, 🏠 Personal, 📚 Study, 🛒 Shopping, 📌 General | Task type |
| Due Date | YYYY-MM-DD | Optional deadline |
| Status | ✅ Complete, ⏳ Pending, ⚠️ Overdue | Task state |

## Running Tests

```bash
# Activate venv
cd console_app_v2 && source .venv/bin/activate

# Install test dependencies
uv pip install pytest pytest-cov

# Run tests from project root
cd ..
PYTHONPATH=. pytest console_app_v2/tests/ -v

# With coverage
PYTHONPATH=. pytest console_app_v2/tests/ --cov=console_app_v2 --cov-report=term-missing
```

## Project Structure

```
console_app_v2/
├── __init__.py        # Package init
├── main.py            # Entry point (routes to TUI or CLI)
├── app.py             # Textual TUI application
├── main_cli.py        # Legacy Rich CLI mode
├── models.py          # Task dataclass
├── services.py        # Business logic (TaskService)
├── storage_json.py    # JSON file storage
├── ui_cli.py          # Rich CLI interface (legacy)
├── pyproject.toml     # Project config
├── README.md          # This file
├── tasks.json         # Task data (auto-created)
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_services.py
    └── test_storage_json.py
```

## Architecture (MVC)

- **Model** (`models.py`) - Task dataclass with validation
- **View** (`app.py`) - Textual TUI / (`ui_cli.py`) - Rich CLI
- **Controller** (`services.py`) - Business logic
- **Storage** (`storage_json.py`) - Persistence layer

## Version Comparison

| Feature | v1 (Basic) | v2 (Enhanced) |
|---------|-----------|---------------|
| UI | Plain text | Textual TUI with dark theme |
| Storage | In-memory | JSON file persistence |
| Navigation | Number keys | Arrow keys + shortcuts |
| Task Fields | title, description | + priority, due_date, category |
| Filtering | None | Sidebar + search + filters |
| Statistics | Basic counts | Live stats bar |

## Modes

1. **Textual TUI** (default): `python -m console_app_v2.main`
2. **Rich CLI** (legacy): `python -m console_app_v2.main --cli`

## License

Part of Evolution Todo Hackathon II project.
