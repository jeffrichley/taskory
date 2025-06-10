import sys
import pytest
from uuid import UUID
from datetime import datetime

sys.path.insert(0, "src")
from taskory.schemas import Task, TaskStatus, TaskPriority

def test_task_full_fields():
    """
    Test creating a Task with all fields provided.
    """
    task = Task(
        title="Test Task",
        status=TaskStatus.in_progress,
        priority=TaskPriority.high,
        assignee="jeff",
        tags=["urgent", "backend"]
    )
    assert isinstance(task.id, UUID)
    assert task.title == "Test Task"
    assert task.status == TaskStatus.in_progress
    assert task.priority == TaskPriority.high
    assert task.assignee == "jeff"
    assert task.tags == ["urgent", "backend"]
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)

def test_task_minimal_fields():
    """
    Test creating a Task with only the required field.
    """
    task = Task(title="Minimal Task")
    assert isinstance(task.id, UUID)
    assert task.title == "Minimal Task"
    assert task.status == TaskStatus.todo
    assert task.priority is None
    assert task.assignee is None
    assert task.tags is None
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)

def test_task_missing_title():
    """
    Test failure when required field 'title' is missing.
    """
    with pytest.raises(Exception):
        Task() 