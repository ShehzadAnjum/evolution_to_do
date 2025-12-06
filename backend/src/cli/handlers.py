"""CLI operation handlers.

This module provides handler functions for each menu operation.
"""

from src.cli.formatters import (
    format_box_line,
    format_error,
    format_success,
    format_task_details,
    format_task_line,
    format_task_summary,
    wait_for_enter,
    BOX_WIDTH,
)
from src.cli.menu import (
    display_empty_tasks,
    display_tasks_footer,
    display_tasks_header,
)
from src.lib.validators import (
    validate_confirmation,
    validate_task_id,
    validate_title,
)
from src.services.task_store import TaskStore


def add_task(store: TaskStore) -> None:
    """Handle adding a new task.

    Prompts user for title (required) and description (optional).

    Args:
        store: The task store to add to
    """
    print()

    # Get title with validation
    while True:
        title_input = input("Enter task title: ")
        valid, cleaned_title, error = validate_title(title_input)
        if valid:
            if error:  # Truncation warning
                print(error)
            break
        print(format_error(error))

    # Get optional description
    description_input = input("Enter description (optional, press Enter to skip): ")
    description = description_input.strip() if description_input.strip() else None

    # Add the task
    task = store.add(cleaned_title, description)

    # Display success message
    print()
    print(format_success("Task added successfully!"))
    for line in format_task_details(task):
        print(line)

    wait_for_enter()


def view_tasks(store: TaskStore) -> None:
    """Handle viewing all tasks.

    Displays task list with status indicators and summary.

    Args:
        store: The task store to view
    """
    if store.is_empty():
        display_empty_tasks()
        wait_for_enter()
        return

    # Display tasks
    display_tasks_header()

    for task in store.get_all():
        for line in format_task_line(task):
            print(format_box_line(line.ljust(BOX_WIDTH)))
        print(format_box_line("".ljust(BOX_WIDTH)))

    # Display summary
    summary = format_task_summary(
        store.count(), store.count_completed(), store.count_remaining()
    )
    display_tasks_footer(summary)

    wait_for_enter()


def mark_complete(store: TaskStore) -> None:
    """Handle marking a task complete/incomplete.

    Prompts for task ID and toggles completion status.

    Args:
        store: The task store
    """
    print()

    # Get task ID with validation
    while True:
        task_id_input = input("Enter task ID to toggle completion: ")
        valid, task_id, error = validate_task_id(task_id_input)
        if not valid:
            print(format_error(error))
            continue

        task = store.toggle_complete(task_id)
        if task is None:
            print(format_error(f"Task with ID {task_id} not found."))
            print("Please enter a valid task ID.")
            continue

        break

    # Display success message
    status = "complete" if task.completed else "incomplete"
    print()
    print(format_success(f"Task marked as {status}!"))
    print(f"  ID: {task.id}")
    print(f"  Title: {task.title}")
    print(f"  Status: {'Complete' if task.completed else 'Incomplete'}")

    wait_for_enter()


def update_task(store: TaskStore) -> None:
    """Handle updating a task's title and/or description.

    Prompts for task ID, shows current values, and allows updating.

    Args:
        store: The task store
    """
    print()

    # Get task ID and retrieve task
    while True:
        task_id_input = input("Enter task ID to update: ")
        valid, task_id, error = validate_task_id(task_id_input)
        if not valid:
            print(format_error(error))
            continue

        task = store.get(task_id)
        if task is None:
            print(format_error(f"Task with ID {task_id} not found."))
            print("Please enter a valid task ID.")
            continue

        break

    # Show current task
    print()
    print("Current task:")
    print(f"  Title: {task.title}")
    print(f"  Description: {task.description or 'None'}")
    print()

    # Get new values (empty = keep current)
    new_title_input = input("Enter new title (press Enter to keep current): ")
    new_desc_input = input("Enter new description (press Enter to keep current): ")

    # Determine what to update
    new_title = new_title_input.strip() if new_title_input.strip() else None
    # For description, we need to distinguish between "keep current" (no input)
    # and "clear description" (explicit empty after having content)
    new_desc = None
    if new_desc_input != "":  # User typed something (even just spaces)
        new_desc = new_desc_input.strip() if new_desc_input.strip() else ""

    # Validate new title if provided
    if new_title is not None:
        valid, new_title, error = validate_title(new_title)
        if not valid:
            print(format_error(error))
            wait_for_enter()
            return

    # Update the task
    updated = store.update(task_id, title=new_title, description=new_desc)

    # Display success message
    print()
    print(format_success("Task updated successfully!"))
    for line in format_task_details(updated):
        print(line)

    wait_for_enter()


def delete_task(store: TaskStore) -> None:
    """Handle deleting a task with confirmation.

    Prompts for task ID, shows task to delete, confirms before deletion.

    Args:
        store: The task store
    """
    print()

    # Get task ID and retrieve task
    while True:
        task_id_input = input("Enter task ID to delete: ")
        valid, task_id, error = validate_task_id(task_id_input)
        if not valid:
            print(format_error(error))
            continue

        task = store.get(task_id)
        if task is None:
            print(format_error(f"Task with ID {task_id} not found."))
            print("Please enter a valid task ID.")
            continue

        break

    # Show task to delete
    print()
    print("Task to delete:")
    print(f"  ID: {task.id}")
    print(f"  Title: {task.title}")
    print()

    # Confirm deletion
    while True:
        confirm_input = input("Are you sure you want to delete this task? (y/n): ")
        valid, confirmed, error = validate_confirmation(confirm_input)
        if not valid:
            print(format_error(error))
            continue
        break

    if confirmed:
        store.delete(task_id)
        print()
        print(format_success("Task deleted successfully!"))
    else:
        print()
        print("Deletion cancelled.")

    wait_for_enter()
