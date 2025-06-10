import sys
from pathlib import Path
import pytest
from typer.testing import CliRunner
import tempfile
from unittest.mock import patch

# Add /src to sys.path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "src"))

from taskory import cli

runner = CliRunner()

def test_cli_with_tempfile():
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_tasks_dir = Path(tmpdir)
        temp_tasks_file = temp_tasks_dir / "tasks.json"
        # Patch the CLI's TASKS_FILE and TASKS_DIR for the duration of the test
        with patch.object(cli, "TASKS_DIR", temp_tasks_dir), patch.object(cli, "TASKS_FILE", temp_tasks_file):
            # Ensure the temp dir exists
            temp_tasks_dir.mkdir(parents=True, exist_ok=True)
            # Now run the tests as before
            result = runner.invoke(cli.app, ["list"])
            assert result.exit_code == 0
            assert "No tasks found." in result.output

            result = runner.invoke(cli.app, ["new", "Test Task"])
            assert result.exit_code == 0
            assert "Task created:" in result.output
            result = runner.invoke(cli.app, ["list"])
            assert result.exit_code == 0
            assert "Test Task" in result.output

            result = runner.invoke(cli.app, ["list", "--status", "not_a_status"])
            assert result.exit_code != 0
            assert "Invalid status" in result.output

def test_update_command():
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_tasks_dir = Path(tmpdir)
        temp_tasks_file = temp_tasks_dir / "tasks.json"
        with patch.object(cli, "TASKS_DIR", temp_tasks_dir), patch.object(cli, "TASKS_FILE", temp_tasks_file):
            temp_tasks_dir.mkdir(parents=True, exist_ok=True)
            # Create a new task
            result = runner.invoke(cli.app, ["new", "Update Me"])
            assert result.exit_code == 0
            assert "Task created:" in result.output
            # Get the task ID
            result = runner.invoke(cli.app, ["list"])
            assert result.exit_code == 0
            lines = result.output.strip().split("\n")
            task_line = lines[-1]
            task_id = task_line.split("|")[0].strip()
            # Update the task status to in_progress
            result = runner.invoke(cli.app, ["update", task_id, "--status", "in_progress"])
            assert result.exit_code == 0
            assert "Task updated:" in result.output
            assert "in_progress" in result.output
            # Try updating with an invalid status
            result = runner.invoke(cli.app, ["update", task_id, "--status", "not_a_status"])
            assert result.exit_code != 0
            assert "Invalid status" in result.output
            # Try updating with an invalid ID
            result = runner.invoke(cli.app, ["update", "bad-id", "--status", "in_progress"])
            assert result.exit_code != 0
            assert "Invalid UUID string" in result.output or "not found" in result.output 