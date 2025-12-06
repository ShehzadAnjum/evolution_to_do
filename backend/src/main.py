"""Main entry point for the todo application.

This module contains the main loop and menu navigation.
"""

import signal
import sys

from src.cli.formatters import format_error, wait_for_enter
from src.cli.handlers import (
    add_task,
    delete_task,
    mark_complete,
    update_task,
    view_tasks,
)
from src.cli.menu import display_goodbye, display_menu, get_menu_prompt
from src.lib.validators import validate_confirmation, validate_menu_choice
from src.services.task_store import TaskStore

# Global store instance
store = TaskStore()


def handle_interrupt(signum: int, frame: object) -> None:
    """Handle Ctrl+C interrupt with confirmation."""
    print("\n")
    while True:
        response = input("Are you sure you want to exit? (y/n): ")
        valid, confirmed, error = validate_confirmation(response)
        if valid:
            if confirmed:
                display_goodbye()
                sys.exit(0)
            else:
                print("Continuing...")
                return
        print(format_error(error))


def main() -> None:
    """Main application entry point."""
    # Set up Ctrl+C handler
    signal.signal(signal.SIGINT, handle_interrupt)

    while True:
        display_menu()
        choice_str = input(get_menu_prompt())

        valid, choice, error = validate_menu_choice(choice_str)
        if not valid:
            print(format_error(error))
            wait_for_enter()
            continue

        if choice == 1:
            add_task(store)
        elif choice == 2:
            view_tasks(store)
        elif choice == 3:
            mark_complete(store)
        elif choice == 4:
            update_task(store)
        elif choice == 5:
            delete_task(store)
        elif choice == 6:
            display_goodbye()
            break


if __name__ == "__main__":
    main()
