# Taskory Bootstrap TODOs

This file is temporary and will be deleted once Taskory can manage its own tasks.

---

## 🧠 Create Task Object

- [x] Define a `Task` dataclass with fields:
  - `id`: str or UUID
  - `title`: str
  - `status`: Enum (`todo`, `in_progress`, `done`)
  - `created_at`: datetime
  - `updated_at`: datetime
  - `priority`: Optional[int] or Enum
  - `assignee`: Optional[str]
  - `tags`: Optional[List[str]]
- [x] Add logic to auto-assign `id`, `created_at`, and `updated_at`
- [x] Write a test to create and inspect a sample `Task` object

---

## 🗃 Create TaskStore for Managing Tasks in Memory

- [x] Define a `TaskStore` class
- [x] Implement `add_task(task)`
- [x] Implement `list_tasks(status=None)`
- [x] Implement `get_task_by_id(id)`
- [x] Implement `update_task(id, **kwargs)`
- [x] Implement `delete_task(id)`
- [x] Write unit tests for add/list/get/update/delete

---

## 💾 Add Persistent JSON File Storage

- [x] Decide on storage format (`tasks.json`)
- [x] Implement `save_to_file(path)` in `TaskStore`
- [x] Implement `load_from_file(path)` in `TaskStore`
- [x] Handle serialization/deserialization of `datetime` and `Enum`
- [x] Add automatic saving after task changes
- [x] Write a test for save → load round-trip

---

## 🖥 Build CLI for Managing Tasks

- [x] Set up CLI using `argparse` or `typer`
- [x] Add `taskory new "Task title"` to create a task
- [x] Add `taskory list` to list all tasks
- [ ] Add `taskory list --status done` (filter by status)
- [ ] Add `taskory update <id> --status in_progress`
- [ ] Add `taskory delete <id>`
- [ ] Add helpful error messages for bad input or missing IDs
- [ ] Connect CLI commands to `TaskStore` logic

---

## 🧭 Add Basic Planning Views

- [ ] Add `taskory plan` → show all tasks in progress
- [ ] Add `taskory focus` → show top 3 `todo` tasks
- [ ] Support `--limit` argument for number of tasks
- [ ] Sort output by creation date or priority
- [ ] Format output for clear readability
