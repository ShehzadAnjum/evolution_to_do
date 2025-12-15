---
name: python-cli-tui
description: Python CLI and TUI patterns with Textual. Use when building command-line interfaces, terminal UIs, or console applications.
---

# Python CLI & TUI

## Basic CLI with argparse

```python
import argparse

parser = argparse.ArgumentParser(description="Todo CLI")
parser.add_argument("command", choices=["add", "list", "complete", "delete"])
parser.add_argument("--title", "-t", help="Task title")
parser.add_argument("--id", type=int, help="Task ID")
args = parser.parse_args()
```

## Interactive Menu

```python
def show_menu():
    print("\n=== Todo Manager ===")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")
    return input("Choose: ")
```

## Textual TUI

```python
from textual.app import App
from textual.widgets import Header, Footer, ListView, ListItem

class TodoApp(App):
    BINDINGS = [("q", "quit", "Quit"), ("a", "add", "Add Task")]

    def compose(self):
        yield Header()
        yield ListView(*[ListItem(Label(t.title)) for t in tasks])
        yield Footer()

    def action_add(self):
        # Show add dialog
        pass

if __name__ == "__main__":
    TodoApp().run()
```

## Output Formatting

```python
def format_task(task):
    status = "✓" if task.is_complete else "○"
    return f"[{status}] {task.id}: {task.title}"
```
