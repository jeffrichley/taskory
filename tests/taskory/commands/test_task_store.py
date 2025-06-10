import sys
import os
import pytest
from uuid import uuid4
from datetime import datetime, timedelta, UTC
import time

# Add /src to sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../src')))

from taskory.commands.task_store import TaskStore
from taskory.schemas import Task, TaskStatus, TaskPriority

@pytest.fixture
def sample_task():
    return Task(
        title="Test Task",
        status=TaskStatus.todo,
        priority=TaskPriority.medium,
        assignee="jeff",
        tags=["test", "sample"]
    )

def test_add_and_get_task(sample_task):
    store = TaskStore()
    store.add_task(sample_task)
    fetched = store.get_task_by_id(sample_task.id)
    assert fetched.id == sample_task.id
    assert fetched.title == "Test Task"

def test_add_duplicate_task_raises(sample_task):
    store = TaskStore()
    store.add_task(sample_task)
    with pytest.raises(ValueError):
        store.add_task(sample_task)

def test_list_tasks_filters_by_status(sample_task):
    store = TaskStore()
    store.add_task(sample_task)
    done_task = Task(title="Done Task", status=TaskStatus.done)
    store.add_task(done_task)
    all_tasks = store.list_tasks()
    todo_tasks = store.list_tasks(status=TaskStatus.todo)
    done_tasks = store.list_tasks(status=TaskStatus.done)
    assert len(all_tasks) == 2
    assert len(todo_tasks) == 1 and todo_tasks[0].status == TaskStatus.todo
    assert len(done_tasks) == 1 and done_tasks[0].status == TaskStatus.done

def test_get_task_by_id_not_found():
    store = TaskStore()
    random_id = uuid4()
    with pytest.raises(KeyError):
        store.get_task_by_id(random_id)

def test_update_task_fields(sample_task):
    store = TaskStore()
    store.add_task(sample_task)
    new_title = "Updated Title"
    new_status = TaskStatus.in_progress
    before = store.get_task_by_id(sample_task.id).updated_at
    time.sleep(0.001)  # Ensure the clock advances (robust against granularity)
    store.update_task(sample_task.id, title=new_title, status=new_status)
    updated = store.get_task_by_id(sample_task.id)
    assert updated.title == new_title
    assert updated.status == new_status
    assert updated.updated_at > before

def test_update_task_invalid_field(sample_task):
    store = TaskStore()
    store.add_task(sample_task)
    with pytest.raises(ValueError):
        store.update_task(sample_task.id, not_a_field="fail")

def test_update_task_not_found():
    store = TaskStore()
    with pytest.raises(KeyError):
        store.update_task(uuid4(), title="nope")

def test_delete_task(sample_task):
    store = TaskStore()
    store.add_task(sample_task)
    store.delete_task(sample_task.id)
    assert store.list_tasks() == []

def test_delete_task_not_found():
    store = TaskStore()
    with pytest.raises(KeyError):
        store.delete_task(uuid4())

def test_get_task_by_id_accepts_str_and_uuid(sample_task):
    store = TaskStore()
    store.add_task(sample_task)
    # As UUID
    fetched1 = store.get_task_by_id(sample_task.id)
    # As string
    fetched2 = store.get_task_by_id(str(sample_task.id))
    assert fetched1.id == fetched2.id == sample_task.id

def test_update_task_accepts_str_and_uuid(sample_task):
    store = TaskStore()
    store.add_task(sample_task)
    new_title = "String Update"
    # As UUID
    store.update_task(sample_task.id, title=new_title)
    updated1 = store.get_task_by_id(sample_task.id)
    assert updated1.title == new_title
    # As string
    store.update_task(str(sample_task.id), title="String Update 2")
    updated2 = store.get_task_by_id(sample_task.id)
    assert updated2.title == "String Update 2"

def test_delete_task_accepts_str_and_uuid(sample_task):
    store = TaskStore()
    store.add_task(sample_task)
    # As string
    store.delete_task(str(sample_task.id))
    assert store.list_tasks() == []
    # Re-add and delete as UUID
    store.add_task(sample_task)
    store.delete_task(sample_task.id)
    assert store.list_tasks() == []

def test_invalid_uuid_string_raises_value_error(sample_task):
    store = TaskStore()
    store.add_task(sample_task)
    bad_id = "not-a-uuid"
    with pytest.raises(ValueError):
        store.get_task_by_id(bad_id)
    with pytest.raises(ValueError):
        store.update_task(bad_id, title="fail")
    with pytest.raises(ValueError):
        store.delete_task(bad_id) 