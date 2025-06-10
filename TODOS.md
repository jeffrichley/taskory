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

- [ ] Define a `TaskStore` class
- [ ] Implement `add_task(task)`
- [ ] Implement `list_tasks(status=None)`
- [ ] Implement `get_task_by_id(id)`
- [ ] Implement `update_task(id, **kwargs)`
- [ ] Implement `delete_task(id)`
- [ ] Write unit tests for add/list/get/update/delete

---

## 💾 Add Persistent JSON File Storage

- [ ] Decide on storage format (`tasks.json`)
- [ ] Implement `save_to_file(path)` in `TaskStore`
- [ ] Implement `load_from_file(path)` in `TaskStore`
- [ ] Handle serialization/deserialization of `datetime` and `Enum`
- [ ] Add automatic saving after task changes
- [ ] Write a test for save → load round-trip

---

## 🖥 Build CLI for Managing Tasks

- [ ] Set up CLI using `argparse` or `typer`
- [ ] Add `taskory new "Task title"` to create a task
- [ ] Add `taskory list` to list all tasks
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
