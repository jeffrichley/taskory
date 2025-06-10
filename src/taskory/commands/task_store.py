from typing import Dict, List, Optional, Any, Union
from uuid import UUID
from datetime import datetime, UTC
from taskory.schemas import Task, TaskStatus

class TaskStore:
    """
    In-memory store for managing Task objects.
    """
    def __init__(self) -> None:
        """
        Initializes the TaskStore with an empty dictionary.
        """
        self._tasks: Dict[UUID, Task] = {}

    def add_task(self, task: Task) -> None:
        """
        Adds a new task to the store.

        Args:
            task (Task): The task to add.

        Raises:
            ValueError: If a task with the same ID already exists.
        """
        if task.id in self._tasks:
            raise ValueError(f"Task with id {task.id} already exists.")
        self._tasks[task.id] = task

    def list_tasks(self, status: Optional[TaskStatus] = None) -> List[Task]:
        """
        Lists all tasks, optionally filtered by status.

        Args:
            status (Optional[TaskStatus]): Status to filter by.

        Returns:
            List[Task]: List of tasks.
        """
        if status is None:
            return list(self._tasks.values())
        return [task for task in self._tasks.values() if task.status == status]

    def get_task_by_id(self, task_id: Union[str, UUID]) -> Task:
        """
        Retrieves a task by its ID.

        Args:
            task_id (str | UUID): The ID of the task (as string or UUID).

        Returns:
            Task: The found task.

        Raises:
            KeyError: If the task is not found.
            ValueError: If the ID string is not a valid UUID.
        """
        if isinstance(task_id, str):
            try:
                task_id = UUID(task_id)
            except Exception as e:
                raise ValueError(f"Invalid UUID string: {task_id}") from e
        try:
            return self._tasks[task_id]
        except KeyError:
            raise KeyError(f"Task with id {task_id} not found.")

    def update_task(self, task_id: Union[str, UUID], **kwargs: Any) -> Task:
        """
        Updates fields of a task by ID.

        Args:
            task_id (str | UUID): The ID of the task to update (as string or UUID).
            **kwargs: Fields to update.

        Returns:
            Task: The updated task.

        Raises:
            KeyError: If the task is not found.
            ValueError: If an invalid field is provided or ID is invalid.
        """
        task = self.get_task_by_id(task_id)
        update_fields = kwargs.copy()
        for key, value in update_fields.items():
            if not hasattr(task, key):
                raise ValueError(f"Invalid field: {key}")
            setattr(task, key, value)
        # Always update the updated_at timestamp
        task.updated_at = datetime.now(UTC)
        self._tasks[task.id] = task
        return task

    def delete_task(self, task_id: Union[str, UUID]) -> None:
        """
        Deletes a task by its ID.

        Args:
            task_id (str | UUID): The ID of the task to delete (as string or UUID).

        Raises:
            KeyError: If the task is not found.
            ValueError: If the ID string is not a valid UUID.
        """
        if isinstance(task_id, str):
            try:
                task_id = UUID(task_id)
            except Exception as e:
                raise ValueError(f"Invalid UUID string: {task_id}") from e
        if task_id not in self._tasks:
            raise KeyError(f"Task with id {task_id} not found.")
        del self._tasks[task_id] 