"""Menu display system with box drawing.

This module provides the main menu display and navigation for the todo app.
"""

from src.cli.formatters import (
    BOX_WIDTH,
    format_box_bottom,
    format_box_line,
    format_box_separator,
    format_box_top,
)

# Menu options
MENU_OPTIONS = [
    "1. Add Task",
    "2. View Tasks",
    "3. Mark Complete/Incomplete",
    "4. Update Task",
    "5. Delete Task",
    "6. Exit",
]

APP_TITLE = "Todo Application v1.0"


def display_menu() -> None:
    """Display the main application menu."""
    print()
    print(format_box_top(BOX_WIDTH))
    print(format_box_line(APP_TITLE.center(BOX_WIDTH)))
    print(format_box_separator(BOX_WIDTH))

    for option in MENU_OPTIONS:
        print(format_box_line(option.ljust(BOX_WIDTH)))

    print(format_box_bottom(BOX_WIDTH))
    print()


def get_menu_prompt() -> str:
    """Get the menu input prompt."""
    return "Enter choice (1-6): "


def display_goodbye() -> None:
    """Display the goodbye message."""
    print()
    print(format_box_top(BOX_WIDTH))
    print(format_box_line("Thank you for using Todo!".center(BOX_WIDTH)))
    print(format_box_line("Goodbye!".center(BOX_WIDTH)))
    print(format_box_bottom(BOX_WIDTH))
    print()


def display_empty_tasks() -> None:
    """Display the empty tasks message."""
    print()
    print(format_box_top(BOX_WIDTH))
    print(format_box_line("Your Tasks".center(BOX_WIDTH)))
    print(format_box_separator(BOX_WIDTH))
    print(format_box_line("No tasks yet.".ljust(BOX_WIDTH)))
    print(format_box_line("Add your first task with".ljust(BOX_WIDTH)))
    print(format_box_line("option 1!".ljust(BOX_WIDTH)))
    print(format_box_bottom(BOX_WIDTH))
    print()


def display_tasks_header() -> None:
    """Display the tasks list header."""
    print()
    print(format_box_top(BOX_WIDTH))
    print(format_box_line("Your Tasks".center(BOX_WIDTH)))
    print(format_box_separator(BOX_WIDTH))
    print(format_box_line("".ljust(BOX_WIDTH)))


def display_tasks_footer(summary: str) -> None:
    """Display the tasks list footer with summary."""
    print(format_box_line("".ljust(BOX_WIDTH)))
    print(format_box_separator(BOX_WIDTH))
    print(format_box_line(summary.center(BOX_WIDTH)))
    print(format_box_bottom(BOX_WIDTH))
    print()
