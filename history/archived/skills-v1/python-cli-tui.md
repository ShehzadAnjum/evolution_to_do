# Python CLI/TUI Development Skill

## Overview
Reusable patterns for building Python command-line and terminal user interface applications.

## Two-Tier Architecture

### v1 - Basic CLI (Simple, In-Memory)
**Use case**: Quick prototypes, simple tools, learning projects

**Structure**:
```
app_v1/
├── __init__.py
├── task.py          # Data model (dataclass)
├── task_manager.py  # Business logic
└── main.py          # CLI entry point with menu loop
```

**Patterns**:
- Plain `input()` for user interaction
- Number-based menu selection (1-6, 0 to exit)
- In-memory storage (no persistence)
- Simple `print()` for output
- `dataclass` for models
- Single manager class for CRUD operations

**Example Menu Loop**:
```python
while True:
    print("\n--- Main Menu ---")
    print("1. View all tasks")
    print("2. Add new task")
    print("0. Exit")

    choice = input("Choose option: ").strip()
    if choice == "1":
        view_tasks(manager)
    elif choice == "0":
        break
```

### v2 - Enhanced TUI (Textual, Persistent)
**Use case**: Production apps, rich UX, advanced features

**Structure**:
```
app_v2/
├── __init__.py
├── models.py        # Data models with validation
├── services.py      # Business logic layer
├── storage_json.py  # JSON persistence
├── ui_cli.py        # Rich CLI (fallback)
├── app.py           # Textual TUI app
└── main.py          # Entry point with mode selection
```

**Key Libraries**:
- `textual` - Full TUI framework with widgets
- `rich` - Fallback CLI with colors/tables

## Textual TUI Patterns

### App Structure
```python
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import DataTable, Header, Footer, Static
from textual.screen import ModalScreen

class TodoApp(App):
    TITLE = "My App"

    # Disable mouse to prevent terminal escape codes
    ENABLE_COMMAND_PALETTE = False

    BINDINGS = [
        Binding("a", "add_item", "Add", show=True),
        Binding("e", "edit_item", "Edit", show=True),
        Binding("d", "delete_item", "Delete", show=True),
        Binding("q", "quit", "Quit", show=True),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield DataTable(id="main-table")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#main-table", DataTable)
        table.cursor_type = "row"
        table.add_columns("Col1", "Col2", "Col3")

def main():
    app = TodoApp()
    app.run(mouse=False)  # IMPORTANT: Disable mouse
```

### Modal Screens (Add/Edit/Confirm)
```python
class EditScreen(ModalScreen[MyModel | None]):
    CSS = """
    EditScreen { align: center middle; }
    #dialog { width: 60; height: auto; border: thick $primary; }
    """

    def __init__(self, item: MyModel):
        super().__init__()
        self._item = item  # Use underscore prefix!

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label("Edit Item")
            yield Input(value=self._item.name, id="name-input")
            with Horizontal():
                yield Button("Save", id="save-btn")
                yield Button("Cancel", id="cancel-btn")

    @on(Button.Pressed, "#save-btn")
    def save(self) -> None:
        self._item.name = self.query_one("#name-input", Input).value
        self.dismiss(self._item)

    @on(Button.Pressed, "#cancel-btn")
    def cancel(self) -> None:
        self.dismiss(None)
```

### Row Selection Pattern
```python
def get_selected_item(self) -> MyModel | None:
    table = self.query_one("#main-table", DataTable)
    if table.row_count == 0:
        return None
    try:
        cursor_row = table.cursor_row
        if cursor_row is not None and 0 <= cursor_row < len(self.filtered_items):
            return self.filtered_items[cursor_row]
    except Exception:
        pass
    return None

@on(DataTable.RowHighlighted, "#main-table")
def on_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
    self.update_detail_bar()
```

### CSS Layout Tips
```css
/* Sidebar with fixed width */
#sidebar {
    width: 20;
    height: 100%;
    padding: 1;
    border-right: solid $primary;
}

/* Hide scrollbar */
#category-list {
    height: 1fr;
    scrollbar-size: 0 0;
}

/* Filter bar with vertical alignment */
#filters {
    height: 6;
    padding: 1;
    align: left middle;
}
#filters Label {
    height: 3;
    content-align: center middle;
}

/* Detail and stats bars */
#detail-bar {
    height: 4;
    padding: 0 1;
    border-top: solid $primary;
    background: $surface-darken-1;
}
```

## Common Gotchas

### 1. Mouse Escape Codes in Terminal
**Problem**: Moving mouse produces garbage characters
**Solution**:
```python
app.run(mouse=False)
```
If terminal is stuck, run: `printf '\e[?1000l\e[?1002l\e[?1003l\e[?1006l'`

### 2. Textual Reserved Property Names
**Problem**: `AttributeError: property 'task' has no setter`
**Solution**: Use underscore prefix for instance variables
```python
# BAD
self.task = task

# GOOD
self._task = task
```

### 3. Emoji Width Inconsistency
**Problem**: Some emojis (like `⚠️`) are wider than others
**Solution**: Use consistent-width emojis or test all icons
```python
# Inconsistent widths
STATUS_ICONS = {"completed": "✅", "pending": "⏳", "overdue": "⚠️"}  # BAD

# Better - all similar width
STATUS_ICONS = {"completed": "✅", "pending": "⏳", "overdue": "❗"}  # GOOD
```

### 4. DataTable Column Alignment
**Problem**: Data doesn't align with headers
**Solution**: Pad values consistently
```python
table.add_row(
    f"{i:>2}",           # Right-align number
    f" {icon} ",         # Center icon with spaces
    f"{title:<25}",      # Left-align, fixed width
    f"{priority:<8}",    # Left-align, fixed width
)
```

### 5. Cursor Not Set After Table Update
**Problem**: "No item selected" after refresh
**Solution**: Move cursor to first row after populating
```python
def update_table(self):
    table.clear()
    for item in items:
        table.add_row(...)
    if items:
        table.move_cursor(row=0)
```

## JSON Storage Pattern
```python
import json
from pathlib import Path
from dataclasses import asdict

class JsonStorage:
    def __init__(self, filepath: str):
        self.filepath = Path(filepath)

    def load(self) -> list:
        if not self.filepath.exists():
            return []
        with open(self.filepath, "r") as f:
            data = json.load(f)
        return [Model.from_dict(d) for d in data]

    def save(self, items: list) -> None:
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.filepath, "w") as f:
            json.dump([asdict(item) for item in items], f, indent=2, default=str)
```

## Testing Pattern
```python
import pytest
from app.models import Task
from app.services import TaskService

class TestTaskService:
    @pytest.fixture
    def service(self, tmp_path):
        storage = JsonStorage(tmp_path / "test.json")
        return TaskService(storage)

    def test_add_task(self, service):
        tasks = []
        task = Task(title="Test")
        tasks = service.add_task(tasks, task)
        assert len(tasks) == 1
```

## Dependencies
```
# requirements.txt
textual>=0.40.0
rich>=13.0.0
pytest>=7.0.0
```

## Version History
- 2025-12-11: Initial skill created from Evolution Todo Phase I (2nd iteration)
