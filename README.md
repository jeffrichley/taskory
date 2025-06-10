# Taskory Project Structure

This project is organized as follows:

- `src/taskory/` - Main source code for the Taskory CLI and backend.
  - `cli.py` - Entry point for the CLI.
  - `schemas.py` - Pydantic models and JSON schema generation.
  - `llm_interface.py` - Abstraction for cloud/self-hosted LLM calls.
  - `commands/` - Handlers for CLI commands: parse, list, next, show, update, expand, analyze.
- `.taskory/` - Generated data and cache.
  - `complexity_report.json` - Output from the analyze command.
  - `llm_cache/` - Cache for LLM responses.
- `planning.json`, `tasks.json`, `ideas.json`, `taskory.config.json` - Project data and configuration files (root).
- `tests/` - Unit tests, mirroring the main app structure.

See the PRD.md for more details on architecture and features.

## 🖥 Taskory CLI Usage

Taskory provides a command-line interface (CLI) for managing your tasks. The CLI uses [Typer](https://typer.tiangolo.com/) and loads tasks from `tasks.json` in the project root.

### Basic Commands

- **Create a new task:**
  ```sh
  python -m taskory.cli new "My new task"
  ```

- **List all tasks:**
  ```sh
  python -m taskory.cli list
  ```

- **List tasks by status:**
  ```sh
  python -m taskory.cli list --status done
  ```

- **Update a task's status:**
  ```sh
  python -m taskory.cli update <task_id> --status in_progress
  ```

- **Create a new task (shorthand):**
  ```sh
  taskory new "My new task"
  ```

- **List all tasks (shorthand):**
  ```sh
  taskory list
  ```

- **List tasks by status (shorthand):**
  ```sh
  taskory list --status done
  ```

- **Update a task's status (shorthand):**
  ```sh
  taskory update <task_id> --status in_progress
  ```

- **Delete a task:**
  ```sh
  python -m taskory.cli delete <task_id>
  ```

- **Delete a task (shorthand):**
  ```sh
  taskory delete <task_id>
  ```

### Notes
- All changes are saved to `