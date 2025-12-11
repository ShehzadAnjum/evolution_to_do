"""Textual TUI Application for Evolution Todo."""

from datetime import date
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical, VerticalScroll
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Input,
    Label,
    OptionList,
    Select,
    Static,
)
from textual.widgets.option_list import Option
from textual.screen import ModalScreen
from textual import on

from .models import Task
from .services import TaskService
from .storage_json import JsonStorage


# Icons for visual cues
PRIORITY_ICONS = {"high": "🔴", "medium": "🟡", "low": "🟢"}
CATEGORY_ICONS = {"work": "💼", "personal": "🏠", "study": "📚", "shopping": "🛒", "general": "📌"}
STATUS_ICONS = {"completed": "✅", "pending": "⏳", "overdue": "❗"}


class AddTaskScreen(ModalScreen[Task | None]):
    """Modal screen for adding a new task."""

    CSS = """
    AddTaskScreen {
        align: center middle;
    }
    #add-dialog {
        width: 60;
        height: auto;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }
    #add-dialog Label {
        margin: 1 0 0 0;
    }
    #add-dialog Input {
        margin: 0 0 1 0;
    }
    #add-dialog Select {
        margin: 0 0 1 0;
    }
    #button-row {
        margin-top: 1;
        height: 3;
    }
    #button-row Button {
        margin: 0 1;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="add-dialog"):
            yield Label("➕ Add New Task", classes="title")
            yield Label("Title *")
            yield Input(placeholder="Enter task title...", id="title-input")
            yield Label("Notes")
            yield Input(placeholder="Enter notes (optional)...", id="notes-input")
            yield Label("Priority")
            yield Select(
                [("🟢 Low", "low"), ("🟡 Medium", "medium"), ("🔴 High", "high")],
                value="medium",
                id="priority-select",
            )
            yield Label("Category")
            yield Select(
                [
                    ("📌 General", "general"),
                    ("💼 Work", "work"),
                    ("🏠 Personal", "personal"),
                    ("📚 Study", "study"),
                    ("🛒 Shopping", "shopping"),
                ],
                value="general",
                id="category-select",
            )
            yield Label("Due Date (YYYY-MM-DD)")
            yield Input(placeholder="Optional: 2025-12-31", id="due-input")
            with Horizontal(id="button-row"):
                yield Button("Save", variant="primary", id="save-btn")
                yield Button("Cancel", variant="default", id="cancel-btn")

    @on(Button.Pressed, "#save-btn")
    def save_task(self) -> None:
        title = self.query_one("#title-input", Input).value.strip()
        if not title:
            self.notify("Title is required!", severity="error")
            return

        notes = self.query_one("#notes-input", Input).value.strip()
        priority = self.query_one("#priority-select", Select).value
        category = self.query_one("#category-select", Select).value
        due_str = self.query_one("#due-input", Input).value.strip()

        due_date = None
        if due_str:
            try:
                due_date = date.fromisoformat(due_str)
            except ValueError:
                self.notify("Invalid date format! Use YYYY-MM-DD", severity="error")
                return

        task = Task(
            title=title,
            notes=notes,
            priority=priority,
            category=category,
            due_date=due_date,
        )
        self.dismiss(task)

    @on(Button.Pressed, "#cancel-btn")
    def cancel(self) -> None:
        self.dismiss(None)


class EditTaskScreen(ModalScreen[Task | None]):
    """Modal screen for editing a task."""

    CSS = """
    EditTaskScreen {
        align: center middle;
    }
    #edit-dialog {
        width: 60;
        height: auto;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }
    #edit-dialog Label {
        margin: 1 0 0 0;
    }
    #edit-dialog Input {
        margin: 0 0 1 0;
    }
    #edit-dialog Select {
        margin: 0 0 1 0;
    }
    #button-row {
        margin-top: 1;
        height: 3;
    }
    #button-row Button {
        margin: 0 1;
    }
    """

    def __init__(self, edit_task: Task):
        super().__init__()
        self._edit_task = edit_task

    def compose(self) -> ComposeResult:
        with Vertical(id="edit-dialog"):
            yield Label("✏️ Edit Task", classes="title")
            yield Label("Title *")
            yield Input(value=self._edit_task.title, id="title-input")
            yield Label("Notes")
            yield Input(value=self._edit_task.notes, id="notes-input")
            yield Label("Priority")
            yield Select(
                [("🟢 Low", "low"), ("🟡 Medium", "medium"), ("🔴 High", "high")],
                value=self._edit_task.priority,
                id="priority-select",
            )
            yield Label("Category")
            yield Select(
                [
                    ("📌 General", "general"),
                    ("💼 Work", "work"),
                    ("🏠 Personal", "personal"),
                    ("📚 Study", "study"),
                    ("🛒 Shopping", "shopping"),
                ],
                value=self._edit_task.category,
                id="category-select",
            )
            yield Label("Due Date (YYYY-MM-DD)")
            yield Input(
                value=self._edit_task.due_date.isoformat() if self._edit_task.due_date else "",
                id="due-input",
            )
            with Horizontal(id="button-row"):
                yield Button("Save", variant="primary", id="save-btn")
                yield Button("Cancel", variant="default", id="cancel-btn")

    @on(Button.Pressed, "#save-btn")
    def save_task(self) -> None:
        title = self.query_one("#title-input", Input).value.strip()
        if not title:
            self.notify("Title is required!", severity="error")
            return

        notes = self.query_one("#notes-input", Input).value.strip()
        priority = self.query_one("#priority-select", Select).value
        category = self.query_one("#category-select", Select).value
        due_str = self.query_one("#due-input", Input).value.strip()

        due_date = None
        if due_str:
            try:
                due_date = date.fromisoformat(due_str)
            except ValueError:
                self.notify("Invalid date format! Use YYYY-MM-DD", severity="error")
                return

        self._edit_task.title = title
        self._edit_task.notes = notes
        self._edit_task.priority = priority
        self._edit_task.category = category
        self._edit_task.due_date = due_date
        self.dismiss(self._edit_task)

    @on(Button.Pressed, "#cancel-btn")
    def cancel(self) -> None:
        self.dismiss(None)


class ConfirmDeleteScreen(ModalScreen[bool]):
    """Modal screen for confirming task deletion."""

    CSS = """
    ConfirmDeleteScreen {
        align: center middle;
    }
    #confirm-dialog {
        width: 50;
        height: auto;
        border: thick $error;
        background: $surface;
        padding: 1 2;
    }
    #button-row {
        margin-top: 1;
        height: 3;
    }
    #button-row Button {
        margin: 0 1;
    }
    """

    def __init__(self, task_title: str):
        super().__init__()
        self.task_title = task_title

    def compose(self) -> ComposeResult:
        with Vertical(id="confirm-dialog"):
            yield Label("🗑️ Delete Task?", classes="title")
            yield Static(f"Are you sure you want to delete:\n\n\"{self.task_title}\"")
            with Horizontal(id="button-row"):
                yield Button("Delete", variant="error", id="delete-btn")
                yield Button("Cancel", variant="default", id="cancel-btn")

    @on(Button.Pressed, "#delete-btn")
    def confirm_delete(self) -> None:
        self.dismiss(True)

    @on(Button.Pressed, "#cancel-btn")
    def cancel(self) -> None:
        self.dismiss(False)


class TodoApp(App):
    """Evolution Todo - Textual TUI Application."""

    TITLE = "Evolution Todo v2"
    SUB_TITLE = "Task Management TUI"

    # Disable mouse support to prevent terminal escape code issues
    ENABLE_COMMAND_PALETTE = False

    CSS = """
    Screen {
        background: $surface;
    }
    #main-container {
        layout: horizontal;
    }
    #sidebar {
        width: 20;
        height: 100%;
        padding: 1;
        border-right: solid $primary;
    }
    #category-list {
        height: 1fr;
        scrollbar-size: 0 0;
    }
    #sidebar-title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }
    #content {
        width: 1fr;
        height: 100%;
    }
    #filters {
        height: 6;
        padding: 1;
        border-bottom: solid $primary;
        align: left middle;
    }
    #filters Label {
        margin-right: 1;
        height: 3;
        content-align: center middle;
    }
    #filters Select {
        width: 20;
        margin-right: 2;
    }
    #search-input {
        width: 30;
    }
    #task-table {
        height: 1fr;
    }
    DataTable > .datatable--header {
        text-style: bold;
    }
    #detail-bar {
        height: 4;
        padding: 0 1;
        border-top: solid $primary;
        background: $surface-darken-1;
    }
    #stats-bar {
        height: 3;
        padding: 0 1;
        border-top: solid $primary;
        background: $surface-darken-2;
    }
    .category-item {
        padding: 0 1;
    }
    .category-item:hover {
        background: $primary-darken-1;
    }
    .selected-category {
        background: $primary;
    }
    """

    BINDINGS = [
        Binding("a", "add_task", "Add Task", show=True),
        Binding("e", "edit_task", "Edit", show=True),
        Binding("d", "delete_task", "Delete", show=True),
        Binding("space", "toggle_complete", "Toggle", show=True),
        Binding("r", "refresh", "Refresh", show=True),
        Binding("q", "quit", "Quit", show=True),
    ]

    def __init__(self):
        super().__init__()
        self.storage = JsonStorage("console_app_v2/tasks.json")
        self.service = TaskService(self.storage)
        self.tasks: list[Task] = []
        self.filtered_tasks: list[Task] = []
        self.selected_category: str | None = None
        self.selected_priority: str | None = None
        self.selected_status: str | None = None
        self.search_text: str = ""

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main-container"):
            with Vertical(id="sidebar"):
                yield Static("📂 Categories", id="sidebar-title")
                yield OptionList(
                    Option("📋 All Tasks", id="all"),
                    Option("💼 Work", id="work"),
                    Option("🏠 Personal", id="personal"),
                    Option("📚 Study", id="study"),
                    Option("🛒 Shopping", id="shopping"),
                    Option("📌 General", id="general"),
                    Option("─" * 14, id="sep", disabled=True),
                    Option("✅ Completed", id="completed"),
                    Option("⏳ Pending", id="pending"),
                    Option("❗ Overdue", id="overdue"),
                    id="category-list",
                )
            with Vertical(id="content"):
                with Horizontal(id="filters"):
                    yield Label("🔍")
                    yield Input(placeholder="Search tasks...", id="search-input")
                    yield Label("Priority:")
                    yield Select(
                        [("All", "all"), ("🔴 High", "high"), ("🟡 Medium", "medium"), ("🟢 Low", "low")],
                        value="all",
                        id="priority-filter",
                    )
                yield DataTable(id="task-table")
                with Horizontal(id="detail-bar"):
                    yield Static("Select a task to view details", id="detail-display")
                with Horizontal(id="stats-bar"):
                    yield Static("", id="stats-display")
        yield Footer()

    def on_mount(self) -> None:
        """Initialize the app after mounting."""
        table = self.query_one("#task-table", DataTable)
        table.cursor_type = "row"
        table.zebra_stripes = True
        table.add_columns("#", "Status", "Title", "Priority", "Category", "Due Date")
        self.load_and_display_tasks()

    def load_and_display_tasks(self) -> None:
        """Load tasks from storage and update display."""
        self.tasks = self.service.load_tasks()
        self.apply_filters()

    def apply_filters(self) -> None:
        """Apply current filters and update display."""
        # Start with all tasks
        filtered = self.tasks

        # Apply category filter from sidebar
        if self.selected_category and self.selected_category not in ("all", "completed", "pending", "overdue"):
            filtered = [t for t in filtered if t.category == self.selected_category]

        # Apply status filter from sidebar
        if self.selected_category == "completed":
            filtered = [t for t in filtered if t.completed]
        elif self.selected_category == "pending":
            filtered = [t for t in filtered if not t.completed]
        elif self.selected_category == "overdue":
            filtered = [t for t in filtered if t.is_overdue]

        # Apply priority filter from dropdown
        priority_filter = self.query_one("#priority-filter", Select).value
        if priority_filter and priority_filter != "all":
            filtered = [t for t in filtered if t.priority == priority_filter]

        # Apply search text
        if self.search_text:
            search_lower = self.search_text.lower()
            filtered = [
                t for t in filtered
                if search_lower in t.title.lower() or search_lower in t.notes.lower()
            ]

        self.filtered_tasks = self.service.sort_tasks(filtered, by="priority")
        self.update_table()
        self.update_stats()
        self.update_detail_bar()

    def update_table(self) -> None:
        """Update the task table with filtered tasks."""
        table = self.query_one("#task-table", DataTable)
        table.clear()
        table.cursor_type = "row"

        for i, task in enumerate(self.filtered_tasks, 1):
            # Status icon
            if task.completed:
                status_icon = STATUS_ICONS["completed"]
            elif task.is_overdue:
                status_icon = STATUS_ICONS["overdue"]
            else:
                status_icon = STATUS_ICONS["pending"]

            # Priority icon
            priority_icon = PRIORITY_ICONS.get(task.priority, "🟡")

            # Category icon
            category_icon = CATEGORY_ICONS.get(task.category, "📌")
            category_text = f"{category_icon} {task.category.title()}"

            # Due date
            due_text = task.due_date.strftime("%Y-%m-%d") if task.due_date else "-"

            # Title (truncate if needed)
            title = task.title[:40] + "..." if len(task.title) > 40 else task.title

            # Pad values for alignment
            priority_text = f"{priority_icon} {task.priority.title():<6}"

            table.add_row(
                f"{i:>2}",
                f" {status_icon} ",
                f"{title:<25}",
                priority_text,
                f"{category_text:<12}",
                due_text,
                key=task.id,
            )

        # Select first row if there are tasks
        if self.filtered_tasks:
            table.move_cursor(row=0)

    def update_stats(self) -> None:
        """Update the stats bar."""
        stats = self.service.get_stats(self.tasks)
        stats_text = (
            f"📊 Total: {stats['total']} | "
            f"✅ Done: {stats['completed']} | "
            f"⏳ Pending: {stats['pending']} | "
            f"⚠️ Overdue: {stats['overdue']} | "
            f"📈 {stats['completion_rate']:.0f}% complete"
        )
        self.query_one("#stats-display", Static).update(stats_text)

    @on(OptionList.OptionSelected, "#category-list")
    def on_category_selected(self, event: OptionList.OptionSelected) -> None:
        """Handle category selection in sidebar."""
        option_id = event.option.id
        if option_id and option_id != "sep":
            self.selected_category = option_id if option_id != "all" else None
            self.apply_filters()

    @on(Select.Changed, "#priority-filter")
    def on_priority_filter_changed(self, event: Select.Changed) -> None:
        """Handle priority filter change."""
        self.apply_filters()

    @on(Input.Changed, "#search-input")
    def on_search_changed(self, event: Input.Changed) -> None:
        """Handle search input change."""
        self.search_text = event.value
        self.apply_filters()

    @on(DataTable.RowHighlighted, "#task-table")
    def on_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        """Handle row selection to update detail bar."""
        self.update_detail_bar()

    def update_detail_bar(self) -> None:
        """Update the detail bar with selected task info."""
        task = self.get_selected_task()
        if task:
            notes = task.notes if task.notes else "No notes"
            detail_text = f"📝 {task.title} | Notes: {notes[:80]}"
        else:
            detail_text = "Select a task to view details"
        self.query_one("#detail-display", Static).update(detail_text)

    def get_selected_task(self) -> Task | None:
        """Get the currently selected task from the table."""
        table = self.query_one("#task-table", DataTable)
        if table.row_count == 0:
            return None
        try:
            cursor_row = table.cursor_row
            if cursor_row is not None and 0 <= cursor_row < len(self.filtered_tasks):
                return self.filtered_tasks[cursor_row]
        except Exception:
            pass
        return None

    def action_add_task(self) -> None:
        """Open add task dialog."""
        def handle_result(task: Task | None) -> None:
            if task:
                self.tasks = self.service.add_task(self.tasks, task)
                self.service.save_tasks(self.tasks)
                self.apply_filters()
                self.notify(f"Task added: {task.title}", severity="information")

        self.push_screen(AddTaskScreen(), handle_result)

    def action_edit_task(self) -> None:
        """Open edit task dialog."""
        task = self.get_selected_task()
        if not task:
            self.notify("No task selected!", severity="warning")
            return

        def handle_result(updated_task: Task | None) -> None:
            if updated_task:
                self.service.save_tasks(self.tasks)
                self.apply_filters()
                self.notify(f"Task updated: {updated_task.title}", severity="information")

        self.push_screen(EditTaskScreen(task), handle_result)

    def action_delete_task(self) -> None:
        """Delete selected task with confirmation."""
        task = self.get_selected_task()
        if not task:
            self.notify("No task selected!", severity="warning")
            return

        def handle_result(confirmed: bool) -> None:
            if confirmed:
                self.tasks = self.service.delete_task(self.tasks, task.id)
                self.service.save_tasks(self.tasks)
                self.apply_filters()
                self.notify(f"Task deleted: {task.title}", severity="information")

        self.push_screen(ConfirmDeleteScreen(task.title), handle_result)

    def action_toggle_complete(self) -> None:
        """Toggle completion status of selected task."""
        task = self.get_selected_task()
        if not task:
            self.notify("No task selected!", severity="warning")
            return

        self.service.toggle_complete(task)
        self.service.save_tasks(self.tasks)
        self.apply_filters()
        status = "completed" if task.completed else "pending"
        self.notify(f"Task marked as {status}", severity="information")

    def action_refresh(self) -> None:
        """Refresh task list from storage."""
        self.load_and_display_tasks()
        self.notify("Tasks refreshed", severity="information")


def main():
    """Run the Textual TUI application."""
    app = TodoApp()
    app.run(mouse=False)  # Disable mouse to prevent terminal escape codes


if __name__ == "__main__":
    main()
