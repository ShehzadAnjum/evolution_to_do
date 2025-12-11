# Evolution Todo - Console Edition v2.0

A beautiful, feature-rich console todo application with Rich UI, emojis, and local storage.

## Features

- **Rich CLI Interface** - Beautiful tables, colors, and emojis
- **Task Metadata** - Priority, due dates, categories, notes
- **JSON Persistence** - Tasks saved locally between sessions
- **Search & Filter** - Find tasks by text, priority, category, status
- **Statistics Dashboard** - Track your productivity

## Quick Start

```bash
# Install dependencies
pip install rich

# Run the app
cd /path/to/evolution_to_do
python -m console_app.main
```

## Screenshots

```
╔══════════════════════════════════════════════════════════════╗
║  🚀 Evolution Todo - Console Edition v2.0                   ║
║  Beautiful task management at your fingertips               ║
╚══════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────┐
│           📋 Main Menu              │
├─────────────────────────────────────┤
│  1. 📋 List all tasks               │
│  2. ➕ Add new task                 │
│  3. ✏️  Edit task                   │
│  4. ✅ Toggle complete              │
│  5. 🗑️  Delete task                 │
│  6. 🔍 Search / Filter              │
│  7. 📊 View statistics              │
│  0. 🚪 Exit                         │
└─────────────────────────────────────┘
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
# Install test dependencies
pip install pytest pytest-cov

# Run tests
cd console_app
pytest tests/ -v

# With coverage
pytest tests/ --cov=. --cov-report=term-missing
```

## Project Structure

```
console_app/
├── __init__.py        # Package init
├── main.py            # Entry point and main loop
├── models.py          # Task dataclass
├── services.py        # Business logic (TaskService)
├── storage_json.py    # JSON file storage
├── ui_cli.py          # Rich CLI interface
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
- **View** (`ui_cli.py`) - Rich CLI rendering
- **Controller** (`services.py`) - Business logic
- **Storage** (`storage_json.py`) - Persistence layer

## 2nd Iteration Enhancements

This is the enhanced Phase I console app for the 2nd iteration:

- [x] MVC refactor for clean architecture
- [x] Rich library for beautiful CLI
- [x] JSON local storage (not in-memory)
- [x] Task metadata (priority, due date, category)
- [x] Search and filter functionality
- [x] Unit tests with pytest
- [ ] Voice commands (future)
- [ ] Multi-language support (future)

## License

Part of Evolution Todo Hackathon II project.
