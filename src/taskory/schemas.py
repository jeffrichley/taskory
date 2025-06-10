from typing import List, Optional
from uuid import uuid4, UUID
from datetime import datetime, UTC
from pydantic import BaseModel, Field, field_validator
from enum import Enum

class TaskStatus(str, Enum):
    """
    Enum for task status.
    """
    todo = "todo"
    in_progress = "in_progress"
    done = "done"

class TaskPriority(int, Enum):
    """
    Enum for task priority.
    """
    low = 1
    medium = 2
    high = 3

class Task(BaseModel):
    """
    Represents a task in the Taskory system.

    Args:
        id (UUID): Unique identifier for the task.
        title (str): Title of the task.
        status (TaskStatus): Status of the task.
        created_at (datetime): Creation timestamp.
        updated_at (datetime): Last update timestamp.
        priority (Optional[TaskPriority]): Priority of the task.
        assignee (Optional[str]): Person assigned to the task.
        tags (Optional[List[str]]): Tags associated with the task.

    Returns:
        Task: A validated Task object.
    """
    id: UUID = Field(default_factory=uuid4)
    title: str
    status: TaskStatus = TaskStatus.todo
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    priority: Optional[TaskPriority] = None
    assignee: Optional[str] = None
    tags: Optional[List[str]] = None

    @field_validator("updated_at", mode="before")
    @classmethod
    def set_updated_at(cls, v, values):
        # Reason: Ensure updated_at is set to created_at if not provided
        return v or values.data.get("created_at") or datetime.now(UTC) 