"""Output formatting utilities.

This module provides functions for formatting CLI output with
consistent styling, box drawing, and status indicators.
"""

from typing import Optional

from src.models.task import Task

# Box drawing characters
BOX_TOP_LEFT = "\u2554"  # ╔
BOX_TOP_RIGHT = "\u2557"  # ╗
BOX_BOTTOM_LEFT = "\u255a"  # ╚
BOX_BOTTOM_RIGHT = "\u255d"  # ╝
BOX_HORIZONTAL = "\u2550"  # ═
BOX_VERTICAL = "\u2551"  # ║
BOX_LEFT_T = "\u2560"  # ╠
BOX_RIGHT_T = "\u2563"  # ╣

# Status indicators
SUCCESS_ICON = "\u2713"  # ✓
ERROR_ICON = "\u2717"  # ✗
CHECKBOX_EMPTY = "[ ]"
CHECKBOX_CHECKED = "[\u2713]"  # [✓]

# Display constraints
MAX_TITLE_DISPLAY = 50
MAX_DESCRIPTION_DISPLAY = 80
BOX_WIDTH = 56


def format_success(message: str) -> str:
    """Format a success message with checkmark.

    Args:
        message: The success message

    Returns:
        Formatted success message
    """
    return f"{SUCCESS_ICON} {message}"


def format_error(message: str) -> str:
    """Format an error message with X mark.

    Args:
        message: The error message

    Returns:
        Formatted error message
    """
    return f"{ERROR_ICON} {message}"


def truncate_text(text: str, max_length: int) -> str:
    """Truncate text with ellipsis if too long.

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text with "..." if needed
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def format_box_line(content: str, width: int = BOX_WIDTH) -> str:
    """Format a line inside a box.

    Args:
        content: Content to put inside the box
        width: Total width of the box interior

    Returns:
        Formatted line with box borders
    """
    padded = content.ljust(width)
    return f"{BOX_VERTICAL}  {padded}  {BOX_VERTICAL}"


def format_box_top(width: int = BOX_WIDTH) -> str:
    """Format the top border of a box."""
    return f"{BOX_TOP_LEFT}{BOX_HORIZONTAL * (width + 4)}{BOX_TOP_RIGHT}"


def format_box_bottom(width: int = BOX_WIDTH) -> str:
    """Format the bottom border of a box."""
    return f"{BOX_BOTTOM_LEFT}{BOX_HORIZONTAL * (width + 4)}{BOX_BOTTOM_RIGHT}"


def format_box_separator(width: int = BOX_WIDTH) -> str:
    """Format a separator line inside a box."""
    return f"{BOX_LEFT_T}{BOX_HORIZONTAL * (width + 4)}{BOX_RIGHT_T}"


def format_task_status(completed: bool) -> str:
    """Format task completion status indicator.

    Args:
        completed: Whether the task is complete

    Returns:
        Status checkbox string
    """
    return CHECKBOX_CHECKED if completed else CHECKBOX_EMPTY


def format_task_line(task: Task) -> list[str]:
    """Format a task for display in the task list.

    Args:
        task: The task to format

    Returns:
        List of formatted lines for this task
    """
    lines = []

    # Main task line with status and title
    status = format_task_status(task.completed)
    title = truncate_text(task.title, MAX_TITLE_DISPLAY)
    lines.append(f"{status} ID: {task.id} - {title}")

    # Description line
    desc = task.description if task.description else "None"
    desc = truncate_text(desc, MAX_DESCRIPTION_DISPLAY)
    lines.append(f"    Description: {desc}")

    return lines


def format_task_summary(total: int, completed: int, remaining: int) -> str:
    """Format the task summary line.

    Args:
        total: Total number of tasks
        completed: Number of completed tasks
        remaining: Number of remaining tasks

    Returns:
        Formatted summary string
    """
    return f"Total: {total} tasks | Completed: {completed} | Remaining: {remaining}"


def format_task_details(
    task: Task,
    title_label: str = "Title",
    desc_label: str = "Description",
) -> list[str]:
    """Format task details for display.

    Args:
        task: The task to format
        title_label: Label for title field
        desc_label: Label for description field

    Returns:
        List of formatted detail lines
    """
    return [
        f"  ID: {task.id}",
        f"  {title_label}: {task.title}",
        f"  {desc_label}: {task.description or 'None'}",
    ]


def format_confirmation_prompt(action: str) -> str:
    """Format a yes/no confirmation prompt.

    Args:
        action: Description of the action to confirm

    Returns:
        Formatted confirmation prompt
    """
    return f"Are you sure you want to {action}? (y/n): "


def wait_for_enter() -> None:
    """Display and wait for enter key press."""
    input("\nPress Enter to continue...")
