from typer import Typer, echo, Option
from pathlib import Path
from typing import Optional
from taskory.commands.task_store import TaskStore
from taskory.schemas import Task, TaskStatus
from rich.console import Console
from rich.table import Table
from rich.text import Text

app = Typer(help="Taskory CLI - Manage your tasks from the command line.")

TASKS_DIR = Path(".taskory")
TASKS_FILE = TASKS_DIR / "tasks.json"

console = Console()

# Ensure the .taskory directory exists before any file operations
def ensure_tasks_dir():
    TASKS_DIR.mkdir(parents=True, exist_ok=True)

def get_store() -> TaskStore:
    """
    Load the TaskStore from the .taskory/tasks.json file.

    Returns:
        TaskStore: The loaded task store.
    """
    ensure_tasks_dir()
    if TASKS_FILE.exists():
        return TaskStore.load_from_file(str(TASKS_FILE))
    return TaskStore()

def save_store(store: TaskStore):
    """
    Save the TaskStore to the .taskory/tasks.json file.

    Args:
        store (TaskStore): The task store to save.
    """
    ensure_tasks_dir()
    store.save_to_file(str(TASKS_FILE))

@app.command()
def new(title: str):
    """
    Create a new task with the given title.

    Args:
        title (str): The title of the new task.
    """
    store = get_store()
    task = Task(title=title)
    store.add_task(task)
    save_store(store)
    console.print(f"Task created: {task.id} - {task.title}", style="bold green")

@app.command()
def list(status: Optional[str] = Option(None, help="Filter by status: todo, in_progress, done")):
    """
    List all tasks, optionally filtered by status.

    Args:
        status (Optional[str]): Filter tasks by status.
    """
    store = get_store()
    if status:
        try:
            status_enum = TaskStatus(status)
        except ValueError:
            console.print(f"Invalid status: {status}", style="bold red")
            raise SystemExit(1)
        tasks = store.list_tasks(status=status_enum)
    else:
        tasks = store.list_tasks()
    if not tasks:
        console.print("No tasks found.", style="yellow")
        return
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", overflow="fold")
    table.add_column("Status")
    table.add_column("Title")
    for task in tasks:
        status_color = {
            "todo": "yellow",
            "in_progress": "cyan",
            "done": "green"
        }.get(task.status.value, "white")
        table.add_row(str(task.id), Text(task.status.value, style=status_color), task.title)
    console.print(table)

@app.command()
def update(id: str, status: str = Option("in_progress", help="New status: todo, in_progress, done")):
    """
    Update the status of a task by its ID.

    Args:
        id (str): The ID of the task to update.
        status (str): The new status for the task (default: in_progress).
    """
    store = get_store()
    try:
        status_enum = TaskStatus(status)
    except ValueError:
        console.print(f"Invalid status: {status}", style="bold red")
        raise SystemExit(1)
    try:
        task = store.update_task(id, status=status_enum)
        save_store(store)
        console.print(f"Task updated: {task.id} | {task.status.value} | {task.title}", style="bold green")
    except KeyError:
        console.print(f"Task with id {id} not found.", style="bold red")
        raise SystemExit(1)
    except ValueError as e:
        console.print(str(e), style="bold red")
        raise SystemExit(1)

@app.command()
def delete(id: str):
    """
    Delete a task by its ID.

    Args:
        id (str): The ID of the task to delete.
    """
    store = get_store()
    try:
        store.delete_task(id)
        save_store(store)
        console.print(f"Task deleted: {id}", style="bold green")
    except KeyError:
        console.print(f"Task with id {id} not found.", style="bold red")
        raise SystemExit(1)
    except ValueError as e:
        console.print(str(e), style="bold red")
        raise SystemExit(1)

if __name__ == "__main__":
    app() 