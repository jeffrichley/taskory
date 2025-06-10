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