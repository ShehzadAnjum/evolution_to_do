#!/usr/bin/env python3
"""Evolution Todo - Console Application v1 (Basic)

A simple console-based todo application.

Usage:
    python -m console_app_v1.main
    python console_app_v1/main.py

Features:
    - Add, View, Update, Delete tasks
    - Mark tasks as complete/incomplete
    - In-memory storage (not persisted)
"""

import sys
from .task_manager import TaskManager


def print_header():
    """Display application header."""
    print("\n" + "=" * 50)
    print("       EVOLUTION TODO - Console App v1")
    print("=" * 50)


def print_menu():
    """Display main menu."""
    print("\n--- Main Menu ---")
    print("1. View all tasks")
    print("2. Add new task")
    print("3. Update task")
    print("4. Delete task")
    print("5. Toggle complete")
    print("6. View statistics")
    print("0. Exit")
    print("-" * 20)


def view_tasks(manager: TaskManager):
    """Display all tasks."""
    tasks = manager.get_all_tasks()

    if not tasks:
        print("\nNo tasks yet. Add your first task!")
        return

    print("\n--- Your Tasks ---")
    for task in tasks:
        print(task)
    print(f"\nTotal: {len(tasks)} task(s)")


def add_task(manager: TaskManager):
    """Add a new task."""
    print("\n--- Add New Task ---")

    title = input("Enter task title: ").strip()
    if not title:
        print("Error: Title is required.")
        return

    description = input("Enter description (optional): ").strip()

    task = manager.add_task(title, description)
    print(f"Task added: {task}")


def update_task(manager: TaskManager):
    """Update an existing task."""
    if not manager.get_all_tasks():
        print("\nNo tasks to update.")
        return

    view_tasks(manager)
    print("\n--- Update Task ---")

    try:
        task_id = int(input("Enter task ID to update: ").strip())
    except ValueError:
        print("Error: Invalid ID.")
        return

    task = manager.get_task(task_id)
    if not task:
        print(f"Error: Task {task_id} not found.")
        return

    print(f"Current: {task}")
    print("(Press Enter to keep current value)")

    new_title = input(f"New title [{task.title}]: ").strip()
    new_desc = input(f"New description [{task.description or 'none'}]: ").strip()

    manager.update_task(
        task_id,
        title=new_title if new_title else None,
        description=new_desc if new_desc else None,
    )
    print(f"Task updated: {manager.get_task(task_id)}")


def delete_task(manager: TaskManager):
    """Delete a task."""
    if not manager.get_all_tasks():
        print("\nNo tasks to delete.")
        return

    view_tasks(manager)
    print("\n--- Delete Task ---")

    try:
        task_id = int(input("Enter task ID to delete: ").strip())
    except ValueError:
        print("Error: Invalid ID.")
        return

    task = manager.get_task(task_id)
    if not task:
        print(f"Error: Task {task_id} not found.")
        return

    confirm = input(f"Delete '{task.title}'? (y/n): ").strip().lower()
    if confirm == "y":
        manager.delete_task(task_id)
        print("Task deleted.")
    else:
        print("Deletion cancelled.")


def toggle_complete(manager: TaskManager):
    """Toggle task completion status."""
    if not manager.get_all_tasks():
        print("\nNo tasks to toggle.")
        return

    view_tasks(manager)
    print("\n--- Toggle Complete ---")

    try:
        task_id = int(input("Enter task ID to toggle: ").strip())
    except ValueError:
        print("Error: Invalid ID.")
        return

    if manager.toggle_complete(task_id):
        task = manager.get_task(task_id)
        status = "completed" if task.completed else "pending"
        print(f"Task marked as {status}: {task}")
    else:
        print(f"Error: Task {task_id} not found.")


def view_stats(manager: TaskManager):
    """Display task statistics."""
    stats = manager.get_stats()
    print("\n--- Statistics ---")
    print(f"Total tasks:     {stats['total']}")
    print(f"Completed:       {stats['completed']}")
    print(f"Pending:         {stats['pending']}")


def main():
    """Main application loop."""
    manager = TaskManager()

    print_header()
    print("\nNote: Tasks are stored in memory only.")
    print("      They will be cleared when you exit.")

    while True:
        print_menu()

        choice = input("Choose option (0-6): ").strip()

        if choice == "1":
            view_tasks(manager)
        elif choice == "2":
            add_task(manager)
        elif choice == "3":
            update_task(manager)
        elif choice == "4":
            delete_task(manager)
        elif choice == "5":
            toggle_complete(manager)
        elif choice == "6":
            view_stats(manager)
        elif choice == "0":
            print("\nGoodbye! Your tasks have been cleared.")
            sys.exit(0)
        else:
            print("Invalid option. Please choose 0-6.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting... Goodbye!")
        sys.exit(0)
