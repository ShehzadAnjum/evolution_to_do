#!/usr/bin/env python3
"""Evolution Todo v2 - Textual TUI Application.

A beautiful, feature-rich console todo application with Textual TUI.

Usage:
    python -m console_app_v2.main        # Run Textual TUI (default)
    python -m console_app_v2.main --cli  # Run Rich CLI (legacy)

Features:
    - Dark theme with arrow key navigation
    - Sidebar for category filtering
    - Task metadata (priority, due date, category, notes)
    - JSON local storage
    - Search and filter
    - Statistics dashboard
"""

import sys


def main():
    """Main entry point."""
    # Check for CLI mode flag
    if "--cli" in sys.argv:
        # Run legacy Rich CLI
        from .main_cli import main as cli_main
        cli_main()
    else:
        # Run Textual TUI (default)
        from .app import main as tui_main
        tui_main()


if __name__ == "__main__":
    main()
