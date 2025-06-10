import json
from typing import Dict, List, Optional, Any, Union
from uuid import UUID
from datetime import datetime, UTC
from taskory.schemas import Task, TaskStatus, TaskPriority
from enum import Enum
from pathlib import Path

class TaskStore:
    """
    In-memory store for managing Task objects, with optional persistent JSON file storage.
    """
    def __init__(self, file_path: Optional[str] = None) -> None:
        """
        Initializes the TaskStore with an empty dictionary or loads from file if provided.
        Args:
            file_path (Optional[str]): Path to the JSON file for persistence.
        """
        self._tasks: Dict[UUID, Task] = {}
        self.file_path = file_path
        if file_path and Path(file_path).exists():
            loaded = self.load_from_file(file_path)
            self._tasks = loaded._tasks

    def save_to_file(self, path: Optional[str] = None) -> None:
        """
        Saves all tasks to a JSON file.
        Args:
            path (Optional[str]): Path to the JSON file. Uses self.file_path if not provided.
        """
        file_path = path or self.file_path
        if not file_path:
            raise ValueError("No file path specified for saving tasks.")
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump([self._serialize_task(task) for task in self._tasks.values()], f, indent=2)

    @classmethod
    def load_from_file(cls, path: str) -> 'TaskStore':
        """
        Loads tasks from a JSON file and returns a new TaskStore instance.
        Args:
            path (str): Path to the JSON file.
        Returns:
            TaskStore: A new TaskStore instance populated with tasks from the file.
        """
        store = cls()
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                task = cls._deserialize_task(item)
                store._tasks[task.id] = task
        store.file_path = path
        return store

    @staticmethod
    def _serialize_task(task: Task) -> dict:
        """
        Serializes a Task object to a dict suitable for JSON.
        Args:
            task (Task): The task to serialize.
        Returns:
            dict: The serialized task.
        """
        return {
            'id': str(task.id),
            'title': task.title,
            'status': task.status.value if isinstance(task.status, Enum) else str(task.status),
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat(),
            'priority': int(task.priority) if task.priority is not None else None,
            'assignee': task.assignee,
            'tags': task.tags,
        }

    @staticmethod
    def _deserialize_task(data: dict) -> Task:
        """
        Deserializes a dict into a Task object.
        Args:
            data (dict): The task data.
        Returns:
            Task: The deserialized Task object.
        """
        return Task(
            id=UUID(data['id']),
            title=data['title'],
            status=TaskStatus(data['status']),
            created_at=datetime.fromisoformat(data['created_at']),
            updated_at=datetime.fromisoformat(data['updated_at']),
            priority=TaskPriority(data['priority']) if data.get('priority') is not None else None,
            assignee=data.get('assignee'),
            tags=data.get('tags'),
        )

    def _auto_save(self):
        if self.file_path:
            self.save_to_file()

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
        self._auto_save()

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
        self._auto_save()
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
        self._auto_save() 