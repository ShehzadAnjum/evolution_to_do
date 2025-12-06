"""Input validation utilities.

This module provides validation functions for user input.
"""

from src.models.task import MAX_DESCRIPTION_LENGTH, MAX_TITLE_LENGTH


def validate_title(title: str) -> tuple[bool, str, str]:
    """Validate a task title.

    Args:
        title: The title to validate

    Returns:
        Tuple of (is_valid, cleaned_title, error_message)
    """
    if not title or not title.strip():
        return False, "", "Task title cannot be empty."

    cleaned = title.strip()
    if len(cleaned) > MAX_TITLE_LENGTH:
        cleaned = cleaned[:MAX_TITLE_LENGTH]
        return True, cleaned, f"Title truncated to {MAX_TITLE_LENGTH} characters."

    return True, cleaned, ""


def validate_description(description: str) -> tuple[bool, str, str]:
    """Validate a task description.

    Args:
        description: The description to validate

    Returns:
        Tuple of (is_valid, cleaned_description, error_message)
    """
    if not description:
        return True, "", ""

    cleaned = description.strip()
    if len(cleaned) > MAX_DESCRIPTION_LENGTH:
        cleaned = cleaned[:MAX_DESCRIPTION_LENGTH]
        return True, cleaned, f"Description truncated to {MAX_DESCRIPTION_LENGTH} characters."

    return True, cleaned, ""


def validate_task_id(task_id_str: str) -> tuple[bool, int, str]:
    """Validate a task ID input.

    Args:
        task_id_str: The task ID string to validate

    Returns:
        Tuple of (is_valid, task_id, error_message)
    """
    if not task_id_str or not task_id_str.strip():
        return False, 0, "Please enter a task ID."

    try:
        task_id = int(task_id_str.strip())
        if task_id <= 0:
            return False, 0, "Task ID must be a positive number."
        return True, task_id, ""
    except ValueError:
        return False, 0, "Invalid input. Please enter a number."


def validate_menu_choice(choice_str: str, max_choice: int = 6) -> tuple[bool, int, str]:
    """Validate a menu choice input.

    Args:
        choice_str: The menu choice string to validate
        max_choice: Maximum valid menu option (default: 6)

    Returns:
        Tuple of (is_valid, choice, error_message)
    """
    if not choice_str or not choice_str.strip():
        return False, 0, f"Please enter a number between 1 and {max_choice}."

    try:
        choice = int(choice_str.strip())
        if choice < 1 or choice > max_choice:
            return False, 0, f"Invalid choice. Please enter a number between 1 and {max_choice}."
        return True, choice, ""
    except ValueError:
        return False, 0, f"Invalid choice. Please enter a number between 1 and {max_choice}."


def validate_confirmation(response: str) -> tuple[bool, bool, str]:
    """Validate a yes/no confirmation response.

    Args:
        response: The confirmation response to validate

    Returns:
        Tuple of (is_valid, confirmed, error_message)
    """
    if not response or not response.strip():
        return False, False, "Please enter 'y' for yes or 'n' for no."

    cleaned = response.strip().lower()
    if cleaned in ("y", "yes"):
        return True, True, ""
    if cleaned in ("n", "no"):
        return True, False, ""

    return False, False, "Please enter 'y' for yes or 'n' for no."
