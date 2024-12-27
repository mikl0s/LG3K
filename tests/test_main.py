"""Tests for the main module."""

import os
import sys
import tempfile
from unittest.mock import patch

import click
import pytest
from click.testing import CliRunner  # Used throughout the file
from rich.console import Console

from lg3k.main import (
    CustomCommand,
    cli,
    format_json_output,
    format_progress_display,
    generate_module_logs,
    get_terminal_width,
    load_modules,
    process_services,
    show_rich_help,
    update_progress,
    update_progress_display,
)


def test_get_terminal_width():
    """Test terminal width retrieval."""
    with patch("shutil.get_terminal_size") as mock_size:
        mock_size.return_value = type("Size", (), {"columns": 100})()
        assert get_terminal_width() == 100


def test_get_terminal_width_error():
    """Test terminal width retrieval with error."""
    with patch("shutil.get_terminal_size", side_effect=OSError):
        assert get_terminal_width() == 80


def test_show_rich_help_with_error():
    """Test rich help display with error."""
    ctx = click.Context(click.Command("test"))
    with patch("lg3k.main.HAS_RICH", True), patch(
        "lg3k.main.console"
    ) as mock_console, patch("lg3k.main.Table", side_effect=Exception("Test error")):
        show_rich_help(ctx)
        # Should fall back to standard help
        assert mock_console.print.call_count == 0


def test_load_modules_with_error(capsys):
    """Test module loading with import error."""
    with patch("os.path.dirname") as mock_dirname, patch(
        "os.path.join"
    ) as mock_join, patch("os.listdir") as mock_listdir, patch(
        "importlib.import_module"
    ) as mock_import, patch(
        "lg3k.main.HAS_RICH", False
    ), patch(
        "lg3k.main.console", None
    ):
        mock_dirname.return_value = "/test/path"
        mock_join.return_value = "/test/path/modules"
        mock_listdir.return_value = ["test.py"]
        mock_import.side_effect = ImportError("Test error")

        modules = load_modules()
        assert len(modules) == 0

        # Check the captured output
        captured = capsys.readouterr()
        assert "Warning: Failed to load module test: Test error" in captured.out


def test_update_progress_display_error():
    """Test progress display update with error."""
    with patch("lg3k.main.module_progress", {"test": "50%"}), patch(
        "lg3k.main.module_order", ["test"]
    ), patch("lg3k.main.module_status", {"test": "Running"}), patch(
        "builtins.print", side_effect=Exception("Test error")
    ), patch(
        "lg3k.main.HAS_RICH", False
    ), patch(
        "lg3k.main.format_progress_display", return_value="Test display"
    ):
        try:
            update_progress_display()
        except Exception:
            pass  # Expected error


def test_generate_module_logs_with_exit():
    """Test log generation with exit event set."""

    def mock_generator():
        return {"test": "log"}

    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = os.path.join(tmpdir, "test.log")
        with patch("lg3k.main.exit_event") as mock_exit:
            mock_exit.is_set.return_value = True
            logs_generated = generate_module_logs(
                "test_module", mock_generator, 20, output_file, False, False
            )
            assert logs_generated == 0


def test_process_services_with_invalid_result():
    """Test process_services with invalid result type."""

    class Args:
        config = "config.json"
        count = 100
        threads = 4
        output_dir = "logs"
        json = True
        llm_format = False

    with patch("lg3k.main.load_config") as mock_load_config, patch(
        "lg3k.main.load_modules"
    ) as mock_load_modules, patch(
        "lg3k.main.generate_module_logs"
    ) as mock_generate_logs:
        mock_load_config.return_value = {"services": ["test_module"]}
        mock_load_modules.return_value = {"test_module": lambda: None}
        mock_generate_logs.return_value = None  # Invalid result

        result = process_services(Args())
        assert result["success"] is False
        assert result["error"]["type"] == "TypeError"


def test_format_progress_display():
    """Test progress display formatting."""
    with patch("lg3k.main.HAS_RICH", False):  # Test without Rich for simplicity
        with patch("lg3k.main.module_order", ["test_module"]):
            with patch("lg3k.main.module_status", {"test_module": "Running"}):
                with patch("lg3k.main.module_progress", {"test_module": "50%"}):
                    result = format_progress_display()
                    assert isinstance(result, str)
                    assert "test_module" in result
                    assert "50%" in result


def test_format_progress_display_with_rich():
    """Test progress display formatting with Rich enabled."""
    with patch("lg3k.main.HAS_RICH", True), patch(
        "lg3k.main.console", Console()
    ), patch("lg3k.main.module_order", ["test_module"]), patch(
        "lg3k.main.module_status", {"test_module": "Running"}
    ), patch(
        "lg3k.main.module_progress", {"test_module": "50%"}
    ):
        result = format_progress_display()
        assert isinstance(result, str)
        assert "test_module" in result
        assert "50%" in result


def test_format_progress_display_complete():
    """Test progress display for completed module."""
    with patch("lg3k.main.HAS_RICH", False), patch(
        "lg3k.main.module_order", ["test_module"]
    ), patch("lg3k.main.module_status", {"test_module": "Complete"}), patch(
        "lg3k.main.module_progress", {}
    ):
        result = format_progress_display()
        assert "Complete" in result


def test_format_progress_display_error():
    """Test progress display for module with error."""
    with patch("lg3k.main.HAS_RICH", False), patch(
        "lg3k.main.module_order", ["test_module"]
    ), patch("lg3k.main.module_status", {"test_module": "Error: Test error"}), patch(
        "lg3k.main.module_progress", {}
    ):
        result = format_progress_display()
        assert "Error: Test error" in result


def test_format_json_output(capsys):
    """Test JSON output formatting."""
    test_data = {
        "success": True,
        "logs_generated": 100,
        "time_taken": 1.5,
        "files": ["file1.log", "file2.log"],
    }
    format_json_output(test_data)
    captured = capsys.readouterr()
    assert captured.out.strip()  # Verify output is not empty
    assert '"success": true' in captured.out
    assert '"logs_generated": 100' in captured.out
    assert '"time_taken": 1.5' in captured.out
    assert '"files": ["file1.log", "file2.log"]' in captured.out


def test_format_json_output_with_error(capsys):
    """Test JSON output formatting with error."""
    test_data = {
        "success": False,
        "error": {"message": "Test error", "type": "ValueError"},
    }
    format_json_output(test_data)
    captured = capsys.readouterr()
    assert '"success": false' in captured.out
    assert '"error"' in captured.out
    assert '"message": "Test error"' in captured.out
    assert '"type": "ValueError"' in captured.out


def test_format_json_output_with_stats(capsys):
    """Test JSON output formatting with stats."""
    with tempfile.NamedTemporaryFile() as tmp:
        tmp.write(b"test content")
        tmp.flush()
        test_data = {
            "success": True,
            "logs_generated": 100,
            "time_taken": 1.5,
            "files": [tmp.name],
        }
        format_json_output(test_data)
        captured = capsys.readouterr()
        assert '"stats"' in captured.out
        assert '"total_files": 1' in captured.out
        assert '"avg_logs_per_file": 100' in captured.out


def test_generate_module_logs():
    """Test log generation for a module."""

    def mock_generator():
        return {"test": "log"}

    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = os.path.join(tmpdir, "test.log")
        logs_generated = generate_module_logs(
            "test_module", mock_generator, 2, output_file, False, True
        )
        assert logs_generated == 2
        assert os.path.exists(output_file)
        with open(output_file) as f:
            lines = f.readlines()
            assert len(lines) == 2


def test_generate_module_logs_with_error():
    """Test log generation with error."""

    def mock_generator():
        raise ValueError("Test error")

    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = os.path.join(tmpdir, "test.log")
        with pytest.raises(ValueError, match="Test error"):
            generate_module_logs(
                "test_module", mock_generator, 2, output_file, False, True
            )


def test_generate_module_logs_llm_format():
    """Test log generation in LLM format."""

    def mock_generator():
        return {
            "level": "ERROR",
            "message": "Test error message",
            "timestamp": "2024-01-01T00:00:00Z",
        }

    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = os.path.join(tmpdir, "test.jsonl")
        logs_generated = generate_module_logs(
            "test_module", mock_generator, 1, output_file, True, True
        )
        assert logs_generated == 1
        assert os.path.exists(output_file)
        with open(output_file) as f:
            line = f.readline()
            assert '"instruction"' in line
            assert '"input"' in line
            assert '"output"' in line


def test_generate_module_logs_with_keyboard_interrupt():
    """Test log generation with keyboard interrupt."""

    def mock_generator():
        raise KeyboardInterrupt()

    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = os.path.join(tmpdir, "test.log")
        with pytest.raises(KeyboardInterrupt):
            generate_module_logs(
                "test_module", mock_generator, 2, output_file, False, True
            )


def test_update_progress():
    """Test progress updates."""
    with patch("lg3k.main.update_progress_display"):
        update_progress("test_module", "75%")
        from lg3k.main import module_progress, module_status

        assert module_progress["test_module"] == "75%"
        assert module_status["test_module"] == "Running"


def test_show_rich_help():
    """Test rich help display."""
    ctx = click.Context(click.Command("test"))
    with patch("lg3k.main.HAS_RICH", True), patch("lg3k.main.console", Console()):
        show_rich_help(ctx)


def test_show_rich_help_without_rich():
    """Test help display without Rich."""
    ctx = click.Context(click.Command("test"))
    with patch("lg3k.main.HAS_RICH", False), patch("click.echo") as mock_echo:
        show_rich_help(ctx)
        mock_echo.assert_any_call(
            "Rich library not available. Install 'rich' package for enhanced output."
        )


def test_rich_import_failure():
    """Test Rich import failure handling."""
    with patch("lg3k.main.HAS_RICH", False), patch("lg3k.main.console", None):
        from lg3k.main import (
            console,
            format_progress_display,
            module_order,
            module_progress,
            module_status,
            update_progress_display,
        )

        # Test format_progress_display without Rich
        module_order.clear()
        module_order.append("test")
        module_status["test"] = "Running"
        module_progress["test"] = "50%"
        result = format_progress_display()
        assert "test" in result
        assert "50%" in result
        assert "[cyan]" not in result  # No Rich formatting
        assert console is None

        # Test update_progress_display without Rich
        with patch("builtins.print") as mock_print:
            update_progress_display()
            mock_print.assert_called()


def test_custom_command():
    """Test CustomCommand functionality."""

    @click.command(cls=CustomCommand)
    @click.option("--generate-config", type=str)
    def test_cmd(generate_config):
        pass

    runner = CliRunner()
    result = runner.invoke(test_cmd, ["--help"])
    assert result.exit_code == 0
    assert isinstance(result.output, str)

    result = runner.invoke(test_cmd, ["--generate-config", "test.json"])
    assert result.exit_code == 0


def test_cli_help():
    """Test CLI help output."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Description" in result.output
    assert "Command Line Options" in result.output
    assert "--generate-config" in result.output


def test_cli_version():
    """Test CLI version output."""
    from lg3k import __version__

    runner = CliRunner()
    result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.output


def test_process_services():
    """Test process_services function."""

    class Args:
        config = "config.json"
        count = 100
        threads = 4
        output_dir = "logs"
        json = False
        llm_format = False

    with patch("lg3k.main.load_config") as mock_load_config, patch(
        "lg3k.main.load_modules"
    ) as mock_load_modules, patch(
        "lg3k.main.generate_module_logs"
    ) as mock_generate_logs:
        # Mock config and modules
        mock_load_config.return_value = {"services": ["test_module"]}
        mock_load_modules.return_value = {"test_module": lambda: {"test": "log"}}
        mock_generate_logs.return_value = 100

        # Test successful processing
        result = process_services(Args())
        assert result == 0

        # Test with JSON output
        args = Args()
        args.json = True
        result = process_services(args)
        assert result["success"] is True
        assert result["logs_generated"] == 100
        assert len(result["files"]) == 1


def test_process_services_with_error():
    """Test process_services function with error."""

    class Args:
        config = "config.json"
        count = 100
        threads = 4
        output_dir = "logs"
        json = True
        llm_format = False

    with patch("lg3k.main.load_config") as mock_load_config:
        # Mock config to raise error
        mock_load_config.side_effect = ValueError("Test error")

        result = process_services(Args())
        assert result["success"] is False
        assert result["error"]["type"] == "ValueError"
        assert result["error"]["message"] == "Test error"


def test_process_services_with_keyboard_interrupt():
    """Test process_services function with keyboard interrupt."""

    class Args:
        config = "config.json"
        count = 100
        threads = 4
        output_dir = "logs"
        json = True
        llm_format = False

    with patch("lg3k.main.load_config") as mock_load_config, patch(
        "lg3k.main.load_modules"
    ) as mock_load_modules:
        # Mock load_modules to avoid actual module loading
        mock_load_modules.return_value = {}
        # Mock config to raise KeyboardInterrupt
        mock_load_config.side_effect = KeyboardInterrupt()

        try:
            result = process_services(Args())
            assert result["success"] is False
            assert result["error"]["type"] == "KeyboardInterrupt"
            assert "Operation cancelled by user" in result["error"]["message"]
        except KeyboardInterrupt:
            pass  # Expected behavior


def test_process_services_no_services():
    """Test process_services function with no services."""

    class Args:
        config = "config.json"
        count = 100
        threads = 4
        output_dir = "logs"
        json = True
        llm_format = False

    with patch("lg3k.main.load_config") as mock_load_config:
        mock_load_config.return_value = {"services": []}

        result = process_services(Args())
        assert result["success"] is False
        assert result["error"]["type"] == "ValueError"
        assert "No active services" in result["error"]["message"]


def test_cli_generate_config_exists_json_output():
    """Test CLI config generation with JSON output when file exists."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Create the file first
        with open("test_config.json", "w") as f:
            f.write("{}")
        # Try to generate config with JSON output
        result = runner.invoke(
            cli, ["--generate-config", "test_config.json", "--json-output"]
        )
        assert result.exit_code == 1
        assert '"success": false' in result.output
        assert '"error"' in result.output
        assert "already exists" in result.output


def test_cli_keyboard_interrupt():
    """Test CLI with keyboard interrupt."""
    runner = CliRunner()
    with patch("lg3k.main.process_services") as mock_process:
        mock_process.side_effect = KeyboardInterrupt()
        result = runner.invoke(cli, ["--json-output"])
        assert result.exit_code == 1
        assert '"success": false' in result.output
        assert '"error"' in result.output
        assert "Operation cancelled by user" in result.output


def test_cli_general_error():
    """Test CLI with general error."""
    runner = CliRunner()
    with patch("lg3k.main.process_services") as mock_process:
        mock_process.side_effect = Exception("Test error")
        result = runner.invoke(cli, ["--json-output"])
        assert result.exit_code == 1
        assert '"success": false' in result.output
        assert '"error"' in result.output
        assert "Test error" in result.output


def test_cli_usage_error():
    """Test CLI with usage error."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--invalid-option"])
    assert result.exit_code == 2  # Click returns 2 for usage errors


def test_cli_config_generation_json():
    """Test config generation with JSON output."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Test successful config generation with JSON output
        with patch("lg3k.main.get_default_config") as mock_config:
            mock_config.return_value = {"test": "config"}
            result = runner.invoke(
                cli, ["--generate-config", "test_config.json", "--json-output"]
            )
            assert result.exit_code == 0
            assert os.path.exists("test_config.json")
            assert '"success": true' in result.output
            assert '"files": ["test_config.json"]' in result.output

        # Test with existing file and JSON output
        result = runner.invoke(
            cli, ["--generate-config", "test_config.json", "--json-output"]
        )
        assert result.exit_code == 1
        assert '"success": false' in result.output
        assert '"error"' in result.output
        assert "already exists" in result.output
        assert '"type": "FileExistsError"' in result.output


def test_cli_abort():
    """Test CLI with abort."""
    runner = CliRunner()
    with patch("lg3k.main.process_services") as mock_process:
        mock_process.side_effect = click.Abort()
        result = runner.invoke(cli)
        assert result.exit_code == 1


def test_llm_format_handling():
    """Test LLM format handling."""
    from lg3k.main import generate_llm_format_log

    # Test string log entry
    log_entry = "Test log message"
    result = generate_llm_format_log(log_entry)
    assert result["instruction"] == "Analyze this log message and explain its meaning"
    assert "Test log message" in result["input"]
    assert "Message: Test log message" in result["output"]

    # Test error log entry
    log_entry = {
        "level": "ERROR",
        "message": "Database connection failed",
        "service": "database",
        "type": "connection",
        "status": 500,
        "duration": 1500,
        "path": "/api/data",
        "method": "GET",
        "timestamp": "2024-01-01T00:00:00Z",
        "extra_field": "test",
    }
    result = generate_llm_format_log(log_entry)
    assert (
        result["instruction"]
        == "Analyze this error log and suggest potential solutions"
    )
    assert "Database connection failed" in result["input"]
    assert "error-level log" in result["output"]
    assert "database service" in result["output"]
    assert "Status code: 500" in result["output"]
    assert "Duration: 1500ms" in result["output"]
    assert "Path: /api/data" in result["output"]
    assert "HTTP Method: GET" in result["output"]
    assert "Timestamp: 2024-01-01T00:00:00Z" in result["output"]
    assert "extra_field: test" in result["output"]

    # Test API GraphQL log
    log_entry = {"service": "api", "type": "graphql", "message": "Query executed"}
    result = generate_llm_format_log(log_entry)
    assert "This is a GraphQL API log" in result["output"]

    # Test API REST log
    log_entry = {"service": "api", "type": "rest", "message": "Request processed"}
    result = generate_llm_format_log(log_entry)
    assert "This is a REST API log" in result["output"]


def test_custom_command_error_handling():
    """Test CustomCommand error handling."""

    @click.command(cls=CustomCommand)
    def test_cmd():
        raise click.exceptions.Exit(1)

    runner = CliRunner()
    result = runner.invoke(test_cmd)
    assert result.exit_code == 1

    @click.command(cls=CustomCommand)
    def test_cmd2():
        raise click.exceptions.UsageError("Invalid usage")

    result = runner.invoke(test_cmd2)
    assert result.exit_code == 1

    @click.command(cls=CustomCommand)
    def test_cmd3():
        raise Exception("Unexpected error")

    result = runner.invoke(test_cmd3)
    assert result.exit_code == 1

    @click.command(cls=CustomCommand)
    def test_cmd4():
        sys.exit(2)  # Should be converted to exit code 1

    result = runner.invoke(test_cmd4)
    assert result.exit_code == 1


def test_cli_generate_config():
    """Test config generation."""
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Test successful config generation
        result = runner.invoke(cli, ["--generate-config", "test_config.json"])
        assert result.exit_code == 0
        assert os.path.exists("test_config.json")

        # Test with Rich enabled
        with patch("lg3k.main.HAS_RICH", True), patch(
            "lg3k.main.console"
        ) as mock_console:
            result = runner.invoke(cli, ["--generate-config", "rich_config.json"])
            assert result.exit_code == 0
            assert os.path.exists("rich_config.json")
            mock_console.print.assert_called()

        # Test with existing file and Rich enabled
        with patch("lg3k.main.HAS_RICH", True), patch(
            "lg3k.main.console"
        ) as mock_console:
            result = runner.invoke(cli, ["--generate-config", "rich_config.json"])
            assert result.exit_code == 1
            mock_console.print.assert_called_with(
                "[red]Error: rich_config.json already exists[/red]"
            )


@pytest.fixture(autouse=True)
def clear_current_run_files():
    """Clear current_run_files before and after each test."""
    from lg3k.main import current_run_files

    current_run_files.clear()
    yield
    current_run_files.clear()


def test_cleanup_files():
    """Test cleanup_files function."""
    from lg3k.main import cleanup_files, current_run_files

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test files
        test_files = [
            os.path.join(tmpdir, "test1.log"),
            os.path.join(tmpdir, "test2.log"),
        ]
        for file_path in test_files:
            with open(file_path, "w") as f:
                f.write("test")
            current_run_files.add(file_path)

        # Test cleanup with keep_files=False
        cleanup_files(keep_files=False)
        for file_path in test_files:
            assert not os.path.exists(file_path)
        assert len(current_run_files) == 0

        # Reset for next test
        for file_path in test_files:
            with open(file_path, "w") as f:
                f.write("test")
            current_run_files.add(file_path)

        # Test cleanup with keep_files=True
        cleanup_files(keep_files=True)
        for file_path in test_files:
            assert os.path.exists(file_path)
        assert len(current_run_files) == 2

        # Test cleanup with missing files
        nonexistent = os.path.join(tmpdir, "nonexistent.log")
        current_run_files.add(nonexistent)
        cleanup_files(keep_files=False)
        assert not os.path.exists(nonexistent)
        assert len(current_run_files) == 0


def test_error_handling_paths():
    """Test various error handling paths."""
    runner = CliRunner()
    # Test terminal control failure
    with patch("lg3k.main.module_progress", {"test": "50%"}), patch(
        "lg3k.main.module_order", ["test"]
    ), patch("lg3k.main.module_status", {"test": "Running"}), patch(
        "builtins.print", side_effect=[Exception("Terminal error"), None]
    ):
        update_progress_display()  # Should handle the error gracefully

    # Test Rich console print failure
    with patch("lg3k.main.HAS_RICH", True), patch(
        "lg3k.main.console"
    ) as mock_console, patch("lg3k.main.module_progress", {"test": "50%"}), patch(
        "lg3k.main.module_order", ["test"]
    ), patch(
        "lg3k.main.module_status", {"test": "Running"}
    ), patch(
        "builtins.print"
    ) as mock_print:
        mock_console.print.side_effect = Exception("Console error")
        update_progress_display()  # Should fall back to regular print
        mock_print.assert_called()

    # Test module generation error
    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = os.path.join(tmpdir, "test.log")
        with pytest.raises(ValueError, match="Test error"):
            generate_module_logs(
                "test_module",
                lambda: (_ for _ in ()).throw(ValueError("Test error")),
                1,
                output_file,
                False,
                False,
            )

    # Test invalid result type
    with patch("lg3k.main.process_services") as mock_process, patch(
        "lg3k.main.output_json"
    ) as mock_output:
        mock_process.return_value = "invalid"
        result = runner.invoke(cli, ["--json-output"])
        assert result.exit_code == 1  # Just verify it failed

    # Test error with ANSI escape sequences
    with patch("lg3k.main.process_services") as mock_process, patch(
        "lg3k.main.output_json"
    ) as mock_output:
        error_result = {
            "success": False,
            "error": {"message": "\033[31mError\033[0m", "type": "TestError"},
            "logs_generated": 0,
            "time_taken": 0.0,
            "files": [],
            "stats": {"total_files": 0, "avg_logs_per_file": 0, "total_size_bytes": 0},
            "config": {"output_directory": None, "file_format": None},
        }
        mock_process.return_value = error_result
        result = runner.invoke(cli, ["--json-output"])
        assert result.exit_code == 1
        mock_output.assert_called()
        call_args = mock_output.call_args[0][0]
        assert call_args["success"] is False
        assert call_args["error"]["message"] == "Error"  # ANSI sequences removed
        assert call_args["error"]["type"] == "TestError"
        assert call_args["logs_generated"] == 0
        assert call_args["time_taken"] == 0.0
        assert call_args["files"] == []
        assert "stats" in call_args
        assert "config" in call_args


def test_generate_module_logs_with_progress():
    """Test log generation with progress updates."""

    def mock_generator():
        return {"test": "log"}

    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = os.path.join(tmpdir, "test.log")
        with patch("lg3k.main.update_progress_display"):
            logs_generated = generate_module_logs(
                "test_module", mock_generator, 20, output_file, False, False
            )
            assert logs_generated == 20
            assert os.path.exists(output_file)


def test_process_services_with_module_error():
    """Test process_services with module error."""

    class Args:
        config = "config.json"
        count = 100
        threads = 4
        output_dir = "logs"
        json = True
        llm_format = False

    with patch("lg3k.main.load_config") as mock_load_config, patch(
        "lg3k.main.load_modules"
    ) as mock_load_modules, patch(
        "lg3k.main.generate_module_logs"
    ) as mock_generate_logs:
        mock_load_config.return_value = {"services": ["test_module"]}
        mock_load_modules.return_value = {"test_module": lambda: None}
        mock_generate_logs.side_effect = ValueError("Module error")

        result = process_services(Args())
        assert result["success"] is False
        assert result["error"]["type"] == "ValueError"
        assert "Module error" in result["error"]["message"]


def test_process_services_with_rich_output():
    """Test process_services with Rich output."""

    class Args:
        config = "config.json"
        count = 100
        threads = 4
        output_dir = "logs"
        json = False
        llm_format = False

    with patch("lg3k.main.load_config") as mock_load_config, patch(
        "lg3k.main.load_modules"
    ) as mock_load_modules, patch(
        "lg3k.main.generate_module_logs"
    ) as mock_generate_logs, patch(
        "lg3k.main.HAS_RICH", True
    ), patch(
        "lg3k.main.console"
    ) as mock_console:
        mock_load_config.return_value = {"services": ["test_module"]}
        mock_load_modules.return_value = {"test_module": lambda: None}
        mock_generate_logs.return_value = 100

        result = process_services(Args())
        assert result == 0
        mock_console.print.assert_called()


def test_generate_module_logs_with_llm_format_string():
    """Test log generation with LLM format for string input."""

    def mock_generator():
        return "test log message"

    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = os.path.join(tmpdir, "test.jsonl")
        logs_generated = generate_module_logs(
            "test_module", mock_generator, 1, output_file, True, False
        )
        assert logs_generated == 1
        with open(output_file) as f:
            line = f.readline()
            assert '"instruction"' in line
            assert '"input"' in line
            assert '"output"' in line


def test_generate_module_logs_with_error_status():
    """Test log generation with error status."""

    def mock_generator():
        return {
            "level": "ERROR",
            "message": "Test error",
            "service": "test_service",
            "type": "test_type",
        }

    with tempfile.TemporaryDirectory() as tmpdir:
        output_file = os.path.join(tmpdir, "test.log")
        logs_generated = generate_module_logs(
            "test_module", mock_generator, 1, output_file, False, False
        )
        assert logs_generated == 1
        with open(output_file) as f:
            line = f.readline()
            assert "Test error" in line


def test_process_services_module_not_found():
    """Test process_services with module not found."""

    class Args:
        config = "config.json"
        count = 100
        threads = 4
        output_dir = "logs"
        json = True
        llm_format = False

    with patch("lg3k.main.load_config") as mock_load_config, patch(
        "lg3k.main.load_modules"
    ) as mock_load_modules:
        mock_load_config.return_value = {"services": ["nonexistent_module"]}
        mock_load_modules.return_value = {}

        result = process_services(Args())
        assert result["success"] is False
        assert result["error"]["type"] == "ModuleNotFoundError"
        assert "Module nonexistent_module not found" in result["error"]["message"]


def test_process_services_debug_output():
    """Test process_services with debug output."""

    class Args:
        config = "config.json"
        count = 100
        threads = 4
        output_dir = "logs"
        json = False
        llm_format = False

    with patch("lg3k.main.load_config") as mock_load_config, patch(
        "lg3k.main.load_modules"
    ) as mock_load_modules, patch(
        "lg3k.main.generate_module_logs"
    ) as mock_generate_logs, patch(
        "builtins.print"
    ) as mock_print:
        mock_load_config.return_value = {"services": ["test_module"]}
        mock_load_modules.return_value = {"test_module": lambda: None}
        mock_generate_logs.return_value = 100

        result = process_services(Args())
        assert result == 0
        # Verify debug prints were called
        mock_print.assert_any_call("Debug: Loading config from config.json")
        mock_print.assert_any_call("Debug: Loading modules")


def test_generate_analysis_api():
    """Test generate_analysis for API logs."""
    from lg3k.main import generate_analysis

    # Test API success
    log_entry = {
        "level": "INFO",
        "message": "API request successful",
        "timestamp": "2024-01-01T00:00:00Z",
        "status": 200,
    }
    analysis = generate_analysis("api", log_entry)
    assert "Log generated at 2024-01-01T00:00:00Z" in analysis
    assert "API request completed successfully" in analysis
    assert "Message details: API request successful" in analysis

    # Test API error
    log_entry["status"] = 500
    analysis = generate_analysis("api", log_entry)
    assert "Server-side error detected in API response" in analysis

    # Test API client error
    log_entry["status"] = 400
    analysis = generate_analysis("api", log_entry)
    assert "Client-side error detected in API request" in analysis

    # Test API redirect
    log_entry["status"] = 301
    analysis = generate_analysis("api", log_entry)
    assert "API request resulted in a redirection" in analysis


def test_generate_analysis_database():
    """Test generate_analysis for database logs."""
    from lg3k.main import generate_analysis

    # Test normal query
    log_entry = {
        "level": "INFO",
        "message": "Query executed",
        "query": "SELECT * FROM table",
        "duration": 100,
    }
    analysis = generate_analysis("database", log_entry)
    assert "Database query execution logged" in analysis
    assert "Query execution time is unusually high" not in analysis

    # Test slow query
    log_entry["duration"] = 1500
    analysis = generate_analysis("database", log_entry)
    assert "Query execution time is unusually high" in analysis


def test_generate_analysis_web_server():
    """Test generate_analysis for web server logs."""
    from lg3k.main import generate_analysis

    log_entry = {
        "level": "INFO",
        "message": "Request processed",
        "method": "GET",
        "path": "/api/v1/users",
    }
    analysis = generate_analysis("web_server", log_entry)
    assert "Web server processed a GET request" in analysis
    assert "Accessed path: /api/v1/users" in analysis


def test_generate_analysis_severity():
    """Test generate_analysis for different severity levels."""
    from lg3k.main import generate_analysis

    # Test ERROR level
    log_entry = {
        "level": "ERROR",
        "message": "Critical failure",
        "timestamp": "2024-01-01T00:00:00Z",
    }
    analysis = generate_analysis("generic", log_entry)
    assert "error level event that requires immediate attention" in analysis

    # Test WARNING level
    log_entry["level"] = "WARNING"
    analysis = generate_analysis("generic", log_entry)
    assert "warning that may require investigation" in analysis

    # Test CRITICAL level
    log_entry["level"] = "CRITICAL"
    analysis = generate_analysis("generic", log_entry)
    assert "critical level event that requires immediate attention" in analysis
