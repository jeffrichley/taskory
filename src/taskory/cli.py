from typer import Typer, echo, Option
from pathlib import Path
from typing import Optional
from taskory.commands.task_store import TaskStore
from taskory.schemas import Task, TaskStatus

app = Typer(help="Taskory CLI - Manage your tasks from the command line.")

TASKS_DIR = Path(".taskory")
TASKS_FILE = TASKS_DIR / "tasks.json"

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
    echo(f"Task created: {task.id} - {task.title}")

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
            echo(f"Invalid status: {status}")
            raise SystemExit(1)
        tasks = store.list_tasks(status=status_enum)
    else:
        tasks = store.list_tasks()
    if not tasks:
        echo("No tasks found.")
        return
    for task in tasks:
        echo(f"{task.id} | {task.status.value} | {task.title}")

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
        echo(f"Invalid status: {status}")
        raise SystemExit(1)
    try:
        task = store.update_task(id, status=status_enum)
        save_store(store)
        echo(f"Task updated: {task.id} | {task.status.value} | {task.title}")
    except KeyError:
        echo(f"Task with id {id} not found.")
        raise SystemExit(1)
    except ValueError as e:
        echo(str(e))
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
        echo(f"Task deleted: {id}")
    except KeyError:
        echo(f"Task with id {id} not found.")
        raise SystemExit(1)
    except ValueError as e:
        echo(str(e))
        raise SystemExit(1)

if __name__ == "__main__":
    app() 