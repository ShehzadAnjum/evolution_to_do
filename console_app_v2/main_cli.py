#!/usr/bin/env python3
"""Evolution Todo v2 - Rich CLI Mode (Legacy).

This is the legacy Rich-based CLI interface.
Run with: python -m console_app_v2.main --cli

For the Textual TUI, run without --cli flag.
"""

import signal
import sys
from pathlib import Path

from .models import Task
from .services import TaskService
from .storage_json import JsonStorage
from . import ui_cli as ui


def setup_storage() -> JsonStorage:
    """Initialize storage with default location."""
    app_dir = Path(__file__).parent
    return JsonStorage(str(app_dir / "tasks.json"))


def handle_list_tasks(service: TaskService, tasks: list) -> None:
    """Display all tasks."""
    ui.render_tasks(tasks)


def handle_add_task(service: TaskService, tasks: list) -> list:
    """Add a new task."""
    ui.console.print("\n[bold cyan]➕ Add New Task[/bold cyan]\n")

    title = ui.input_task_title()
    notes = ui.input_task_notes()
    priority = ui.input_priority()
    category = ui.input_category()
    due_date = ui.input_due_date()

    task = Task(
        title=title,
        notes=notes,
        priority=priority,
        category=category,
        due_date=due_date,
    )

    tasks = service.add_task(tasks, task)
    service.save_tasks(tasks)

    ui.show_success(f"Task added: {task.title}")
    return tasks


def handle_edit_task(service: TaskService, tasks: list) -> list:
    """Edit an existing task."""
    if not tasks:
        ui.show_warning("No tasks to edit.")
        return tasks

    ui.console.print("\n[bold cyan]✏️  Edit Task[/bold cyan]\n")
    ui.render_tasks(tasks)

    idx = ui.choose_task_index(tasks, "Enter task number to edit")
    if idx is None:
        return tasks

    task = tasks[idx]
    ui.console.print(f"\n[dim]Editing: {task.title}[/dim]")
    ui.console.print("[dim]Press Enter to keep current value[/dim]\n")

    # Get new values (empty = keep current)
    new_title = ui.console.input(f"[cyan]Title [{task.title}]:[/cyan] ").strip()
    new_notes = ui.console.input(f"[cyan]Notes [{task.notes or 'none'}]:[/cyan] ").strip()

    ui.console.print(f"[dim]Current priority: {task.priority}[/dim]")
    new_priority = ui.console.input("[cyan]New priority (l/m/h) or Enter to keep:[/cyan] ").strip().lower()
    if new_priority in ("l", "low"):
        new_priority = "low"
    elif new_priority in ("h", "high"):
        new_priority = "high"
    elif new_priority in ("m", "medium"):
        new_priority = "medium"
    else:
        new_priority = None

    ui.console.print(f"[dim]Current category: {task.category}[/dim]")
    new_category = ui.console.input("[cyan]New category (g/w/p/s/h) or Enter to keep:[/cyan] ").strip().lower()
    category_map = {"w": "work", "p": "personal", "s": "study", "h": "shopping", "g": "general"}
    new_category = category_map.get(new_category)

    ui.console.print(f"[dim]Current due date: {task.due_date or 'not set'}[/dim]")
    new_due = ui.console.input("[cyan]New due date (YYYY-MM-DD) or Enter to keep:[/cyan] ").strip()
    if new_due:
        try:
            from datetime import date
            new_due = date.fromisoformat(new_due)
        except ValueError:
            ui.show_warning("Invalid date format, keeping current.")
            new_due = None
    else:
        new_due = None

    # Apply updates
    service.update_task(
        task,
        title=new_title if new_title else None,
        notes=new_notes if new_notes else None,
        priority=new_priority,
        due_date=new_due,
        category=new_category,
    )

    service.save_tasks(tasks)
    ui.show_success(f"Task updated: {task.title}")
    return tasks


def handle_toggle_complete(service: TaskService, tasks: list) -> list:
    """Toggle task completion status."""
    if not tasks:
        ui.show_warning("No tasks to complete.")
        return tasks

    ui.console.print("\n[bold cyan]✅ Toggle Complete[/bold cyan]\n")
    ui.render_tasks(tasks)

    idx = ui.choose_task_index(tasks, "Enter task number to toggle")
    if idx is None:
        return tasks

    task = tasks[idx]
    service.toggle_complete(task)
    service.save_tasks(tasks)

    status = "completed" if task.completed else "pending"
    ui.show_success(f"Task marked as {status}: {task.title}")
    return tasks


def handle_delete_task(service: TaskService, tasks: list) -> list:
    """Delete a task."""
    if not tasks:
        ui.show_warning("No tasks to delete.")
        return tasks

    ui.console.print("\n[bold cyan]🗑️  Delete Task[/bold cyan]\n")
    ui.render_tasks(tasks)

    idx = ui.choose_task_index(tasks, "Enter task number to delete")
    if idx is None:
        return tasks

    task = tasks[idx]

    if ui.confirm(f"Delete '{task.title}'?"):
        tasks = service.delete_task(tasks, task.id)
        service.save_tasks(tasks)
        ui.show_success(f"Task deleted: {task.title}")
    else:
        ui.show_info("Deletion cancelled.")

    return tasks


def handle_search(service: TaskService, tasks: list) -> None:
    """Search and filter tasks."""
    if not tasks:
        ui.show_warning("No tasks to search.")
        return

    ui.console.print("\n[bold cyan]🔍 Search / Filter Tasks[/bold cyan]\n")

    # Get search criteria
    text = ui.console.input("[cyan]Search text (title/notes, empty for none):[/cyan] ").strip()

    ui.console.print("[dim]Priority filter: (l)ow, (m)edium, (h)igh, (a)ll[/dim]")
    priority_input = ui.console.input("[cyan]Priority [all]:[/cyan] ").strip().lower()
    priority = None
    if priority_input in ("l", "low"):
        priority = "low"
    elif priority_input in ("m", "medium"):
        priority = "medium"
    elif priority_input in ("h", "high"):
        priority = "high"

    ui.console.print("[dim]Category: (g)eneral, (w)ork, (p)ersonal, (s)tudy, s(h)opping, (a)ll[/dim]")
    category_input = ui.console.input("[cyan]Category [all]:[/cyan] ").strip().lower()
    category = {"w": "work", "p": "personal", "s": "study", "h": "shopping", "g": "general"}.get(category_input)

    ui.console.print("[dim]Status: (a)ll, (p)ending, (c)ompleted[/dim]")
    status_input = ui.console.input("[cyan]Status [all]:[/cyan] ").strip().lower()
    completed = None
    if status_input in ("p", "pending"):
        completed = False
    elif status_input in ("c", "completed"):
        completed = True

    # Perform search
    results = service.search(
        tasks,
        text=text,
        priority=priority,
        category=category,
        completed=completed,
    )

    # Display results
    ui.console.print()
    if results:
        ui.render_tasks(results, title=f"🔍 Search Results ({len(results)} found)")
    else:
        ui.show_info("No tasks match your criteria.")


def handle_stats(service: TaskService, tasks: list) -> None:
    """Display task statistics."""
    ui.console.print()
    stats = service.get_stats(tasks)
    ui.render_stats(stats)


def handle_exit(service: TaskService, tasks: list) -> None:
    """Handle graceful exit."""
    service.save_tasks(tasks)
    ui.render_goodbye()
    sys.exit(0)


def handle_interrupt(signum, frame):
    """Handle Ctrl+C interrupt."""
    ui.console.print()
    if ui.confirm("Are you sure you want to exit?"):
        ui.render_goodbye()
        sys.exit(0)
    ui.console.print()


def main():
    """Main application loop (Rich CLI mode)."""
    # Setup signal handler for Ctrl+C
    signal.signal(signal.SIGINT, handle_interrupt)

    # Initialize storage and service
    storage = setup_storage()
    service = TaskService(storage)

    # Load existing tasks
    tasks = service.load_tasks()

    # Welcome message
    ui.render_welcome()

    # Main loop
    while True:
        choice = ui.render_main_menu()

        if choice == "1":
            handle_list_tasks(service, tasks)
        elif choice == "2":
            tasks = handle_add_task(service, tasks)
        elif choice == "3":
            tasks = handle_edit_task(service, tasks)
        elif choice == "4":
            tasks = handle_toggle_complete(service, tasks)
        elif choice == "5":
            tasks = handle_delete_task(service, tasks)
        elif choice == "6":
            handle_search(service, tasks)
        elif choice == "7":
            handle_stats(service, tasks)
        elif choice == "0":
            handle_exit(service, tasks)
        else:
            ui.show_error("Invalid option. Please choose 0-7.")


if __name__ == "__main__":
    main()
