"""Beautiful CLI interface using Rich library with emojis."""

from datetime import date, datetime
from typing import List, Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

from .models import Task

# Initialize Rich console
console = Console()


# ═══════════════════════════════════════════════════════════════════════════════
# ICONS / EMOJIS
# ═══════════════════════════════════════════════════════════════════════════════

def priority_icon(priority: str) -> str:
    """Get emoji icon for priority level."""
    return {
        "low": "🟢",
        "medium": "🟡",
        "high": "🔴",
    }.get(priority, "⚪")


def status_icon(task: Task) -> str:
    """Get emoji icon for task status."""
    if task.completed:
        return "✅"
    if task.is_overdue:
        return "⚠️"
    return "⏳"


def category_icon(category: str) -> str:
    """Get emoji icon for category."""
    return {
        "work": "💼",
        "personal": "🏠",
        "study": "📚",
        "shopping": "🛒",
        "general": "📌",
    }.get(category, "📌")


# ═══════════════════════════════════════════════════════════════════════════════
# DISPLAY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def render_welcome() -> None:
    """Display welcome banner."""
    banner = Text()
    banner.append("╔══════════════════════════════════════════════════════════════╗\n", style="cyan")
    banner.append("║", style="cyan")
    banner.append("  🚀 Evolution Todo ", style="bold magenta")
    banner.append("- Console Edition v2.0                   ", style="white")
    banner.append("║\n", style="cyan")
    banner.append("║", style="cyan")
    banner.append("  Beautiful task management at your fingertips               ", style="dim")
    banner.append("║\n", style="cyan")
    banner.append("╚══════════════════════════════════════════════════════════════╝", style="cyan")
    console.print(banner)
    console.print()


def render_tasks(tasks: List[Task], title: str = "📋 Your Tasks") -> None:
    """Display tasks in a beautiful table."""
    if not tasks:
        console.print(Panel(
            "[dim]No tasks found. Add your first task![/dim]",
            title="📋 Tasks",
            border_style="dim"
        ))
        return

    table = Table(
        title=title,
        box=box.ROUNDED,
        show_header=True,
        header_style="bold cyan",
    )

    table.add_column("#", justify="right", style="dim", width=4)
    table.add_column("Status", justify="center", width=6)
    table.add_column("Title", style="white", min_width=20)
    table.add_column("Priority", justify="center", width=10)
    table.add_column("Due", justify="center", width=12)
    table.add_column("Category", justify="center", width=12)

    for idx, task in enumerate(tasks, start=1):
        # Style based on status
        title_style = "strike dim" if task.completed else ("red" if task.is_overdue else "white")

        # Format due date
        due_str = ""
        if task.due_date:
            days_diff = (task.due_date - date.today()).days
            if days_diff < 0:
                due_str = f"[red]{task.due_date}[/red]"
            elif days_diff == 0:
                due_str = "[yellow]Today[/yellow]"
            elif days_diff == 1:
                due_str = "[green]Tomorrow[/green]"
            else:
                due_str = str(task.due_date)

        table.add_row(
            str(idx),
            status_icon(task),
            f"[{title_style}]{task.title}[/{title_style}]",
            f"{priority_icon(task.priority)} {task.priority}",
            due_str,
            f"{category_icon(task.category)} {task.category}",
        )

    console.print(table)


def render_task_detail(task: Task) -> None:
    """Display detailed view of a single task."""
    status = "✅ Completed" if task.completed else ("⚠️ Overdue" if task.is_overdue else "⏳ Pending")

    content = Text()
    content.append(f"Title: ", style="cyan")
    content.append(f"{task.title}\n", style="white bold")

    content.append(f"Status: ", style="cyan")
    content.append(f"{status}\n", style="green" if task.completed else ("red" if task.is_overdue else "yellow"))

    content.append(f"Priority: ", style="cyan")
    content.append(f"{priority_icon(task.priority)} {task.priority}\n")

    content.append(f"Category: ", style="cyan")
    content.append(f"{category_icon(task.category)} {task.category}\n")

    content.append(f"Due Date: ", style="cyan")
    content.append(f"{task.due_date or 'Not set'}\n")

    if task.notes:
        content.append(f"\nNotes:\n", style="cyan")
        content.append(f"{task.notes}\n", style="dim")

    content.append(f"\nID: ", style="dim")
    content.append(f"{task.short_id}", style="dim")

    console.print(Panel(content, title="📝 Task Details", border_style="cyan"))


def render_stats(stats: dict) -> None:
    """Display task statistics."""
    content = Text()
    content.append(f"📊 Total Tasks: ", style="cyan")
    content.append(f"{stats['total']}\n", style="white bold")

    content.append(f"✅ Completed: ", style="cyan")
    content.append(f"{stats['completed']}\n", style="green")

    content.append(f"⏳ Pending: ", style="cyan")
    content.append(f"{stats['pending']}\n", style="yellow")

    content.append(f"⚠️  Overdue: ", style="cyan")
    content.append(f"{stats['overdue']}\n", style="red")

    content.append(f"\n📈 Completion Rate: ", style="cyan")
    content.append(f"{stats['completion_rate']:.1f}%", style="magenta bold")

    console.print(Panel(content, title="📊 Statistics", border_style="cyan"))


# ═══════════════════════════════════════════════════════════════════════════════
# MENU FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def render_main_menu() -> str:
    """Display main menu and get user choice."""
    console.print()
    menu = Text()
    menu.append("┌─────────────────────────────────────┐\n", style="cyan")
    menu.append("│", style="cyan")
    menu.append("           📋 Main Menu              ", style="bold white")
    menu.append("│\n", style="cyan")
    menu.append("├─────────────────────────────────────┤\n", style="cyan")
    menu.append("│", style="cyan")
    menu.append("  1. ", style="yellow")
    menu.append("📋 List all tasks                ", style="white")
    menu.append("│\n", style="cyan")
    menu.append("│", style="cyan")
    menu.append("  2. ", style="yellow")
    menu.append("➕ Add new task                  ", style="white")
    menu.append("│\n", style="cyan")
    menu.append("│", style="cyan")
    menu.append("  3. ", style="yellow")
    menu.append("✏️  Edit task                     ", style="white")
    menu.append("│\n", style="cyan")
    menu.append("│", style="cyan")
    menu.append("  4. ", style="yellow")
    menu.append("✅ Toggle complete               ", style="white")
    menu.append("│\n", style="cyan")
    menu.append("│", style="cyan")
    menu.append("  5. ", style="yellow")
    menu.append("🗑️  Delete task                  ", style="white")
    menu.append("│\n", style="cyan")
    menu.append("│", style="cyan")
    menu.append("  6. ", style="yellow")
    menu.append("🔍 Search / Filter               ", style="white")
    menu.append("│\n", style="cyan")
    menu.append("│", style="cyan")
    menu.append("  7. ", style="yellow")
    menu.append("📊 View statistics               ", style="white")
    menu.append("│\n", style="cyan")
    menu.append("│", style="cyan")
    menu.append("  0. ", style="red")
    menu.append("🚪 Exit                          ", style="white")
    menu.append("│\n", style="cyan")
    menu.append("└─────────────────────────────────────┘", style="cyan")

    console.print(menu)

    return console.input("\n[cyan]Choose an option:[/cyan] ").strip()


# ═══════════════════════════════════════════════════════════════════════════════
# INPUT FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def choose_task_index(tasks: List[Task], prompt: str = "Enter task number") -> Optional[int]:
    """Get task selection by index (1-based).

    Returns:
        0-based index if valid, None if cancelled or invalid
    """
    if not tasks:
        console.print("[yellow]No tasks available.[/yellow]")
        return None

    try:
        raw = console.input(f"[cyan]{prompt} (or Enter to cancel):[/cyan] ").strip()
        if not raw:
            return None
        idx = int(raw)
        if 1 <= idx <= len(tasks):
            return idx - 1
        console.print(f"[red]Invalid number. Please enter 1-{len(tasks)}.[/red]")
    except ValueError:
        console.print("[red]Invalid input. Please enter a number.[/red]")
    return None


def input_task_title() -> str:
    """Get task title from user."""
    while True:
        title = console.input("[cyan]Task title:[/cyan] ").strip()
        if title:
            return title[:200]
        console.print("[red]Title is required. Please enter a title.[/red]")


def input_task_notes() -> str:
    """Get optional task notes."""
    notes = console.input("[cyan]Notes (optional):[/cyan] ").strip()
    return notes[:1000]


def input_priority() -> str:
    """Get task priority."""
    console.print("[dim]Priority: (l)ow, (m)edium, (h)igh[/dim]")
    choice = console.input("[cyan]Priority [m]:[/cyan] ").strip().lower()

    if choice in ("l", "low"):
        return "low"
    elif choice in ("h", "high"):
        return "high"
    else:
        return "medium"


def input_category() -> str:
    """Get task category."""
    console.print("[dim]Categories: (g)eneral, (w)ork, (p)ersonal, (s)tudy, s(h)opping[/dim]")
    choice = console.input("[cyan]Category [g]:[/cyan] ").strip().lower()

    mapping = {
        "w": "work", "work": "work",
        "p": "personal", "personal": "personal",
        "s": "study", "study": "study",
        "h": "shopping", "shopping": "shopping",
    }
    return mapping.get(choice, "general")


def input_due_date() -> Optional[date]:
    """Get optional due date."""
    console.print("[dim]Due date format: YYYY-MM-DD (e.g., 2025-12-31)[/dim]")
    raw = console.input("[cyan]Due date (optional):[/cyan] ").strip()

    if not raw:
        return None

    try:
        return date.fromisoformat(raw)
    except ValueError:
        console.print("[yellow]Invalid date format. Skipping due date.[/yellow]")
        return None


def confirm(message: str) -> bool:
    """Get yes/no confirmation."""
    response = console.input(f"[yellow]{message} (y/n):[/yellow] ").strip().lower()
    return response in ("y", "yes")


# ═══════════════════════════════════════════════════════════════════════════════
# MESSAGE FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════════

def show_success(message: str) -> None:
    """Display success message."""
    console.print(f"[green]✅ {message}[/green]")


def show_error(message: str) -> None:
    """Display error message."""
    console.print(f"[red]❌ {message}[/red]")


def show_warning(message: str) -> None:
    """Display warning message."""
    console.print(f"[yellow]⚠️  {message}[/yellow]")


def show_info(message: str) -> None:
    """Display info message."""
    console.print(f"[cyan]ℹ️  {message}[/cyan]")


def render_goodbye() -> None:
    """Display goodbye message."""
    console.print()
    console.print(Panel(
        "[bold magenta]Thank you for using Evolution Todo! 🚀[/bold magenta]\n"
        "[dim]Your tasks have been saved. See you next time![/dim]",
        title="👋 Goodbye",
        border_style="magenta"
    ))
