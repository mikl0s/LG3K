"""Tests for the main module."""

import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from click.testing import CliRunner

import lg3k.main
from lg3k.main import (
    cli,
    format_progress_display,
    generate_module_logs,
    load_modules,
    main,
    show_rich_help,
    update_progress_display,
)


def test_load_modules():
    """Test that modules can be loaded."""
    modules = load_modules()
    assert len(modules) > 0


def test_generate_module_logs(tmp_path):
    """Test log generation for a single module."""

    def mock_generator():
        return "test log entry"

    output_dir = Path(tmp_path)
    generate_module_logs("test_module", mock_generator, 5, output_dir)

    # Find the generated log file
    log_files = list(output_dir.glob("test_module_*.log"))
    assert len(log_files) == 1

    # Check log content
    with open(log_files[0]) as f:
        lines = f.readlines()
        assert len(lines) == 5
        assert all(line.strip() == "test log entry" for line in lines)


@patch("lg3k.main.RICH_AVAILABLE", False)
def test_cli_help():
    """Test CLI help output."""
    result = CliRunner().invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Multi-threaded log generator" in result.output


@patch("lg3k.main.RICH_AVAILABLE", True)
@patch("lg3k.main.console")
def test_cli_help_with_rich(mock_console):
    """Test CLI help output with Rich formatting."""
    result = CliRunner().invoke(cli)
    assert result.exit_code == 0
    assert mock_console.print.called


def test_cli_generate_config(tmp_path):
    """Test config file generation."""
    config_path = tmp_path / "test_config.json"
    result = CliRunner().invoke(cli, ["--generate-config", str(config_path)])

    assert result.exit_code == 0
    assert config_path.exists()

    with open(config_path) as f:
        config = json.load(f)
        assert "services" in config
        assert "count" in config
        assert "threads" in config


@patch("lg3k.main.RICH_AVAILABLE", False)
def test_cli_generate_logs(tmp_path):
    """Test log generation through CLI."""
    output_dir = tmp_path / "logs"

    with patch("lg3k.main.load_modules") as mock_load, patch(
        "lg3k.main.load_config"
    ) as mock_config:
        mock_load.return_value = {"test": lambda: "test log"}
        mock_config.return_value = {"services": ["test"], "count": 5, "threads": 1}
        result = CliRunner().invoke(
            cli, ["--count", "5", "--threads", "1", "--output-dir", str(output_dir)]
        )

    assert result.exit_code == 0
    assert output_dir.exists()
    log_files = list(output_dir.glob("*.log"))
    assert len(log_files) == 1


@patch("lg3k.main.RICH_AVAILABLE", True)
@patch("lg3k.main.console")
@patch("rich.panel.Panel")
def test_cli_generate_logs_with_rich(mock_panel, mock_console, tmp_path):
    """Test log generation with Rich formatting."""
    output_dir = tmp_path / "logs"

    mock_panel.fit.return_value = "Configuration Panel"

    with patch("lg3k.main.load_modules") as mock_load, patch(
        "lg3k.main.load_config"
    ) as mock_config, patch("lg3k.main.update_progress") as mock_progress, patch(
        "lg3k.main.generate_module_logs"
    ) as mock_generate:
        mock_load.return_value = {"test": lambda: "test log"}
        mock_config.return_value = {"services": ["test"], "count": 5, "threads": 1}
        mock_progress.return_value = "50%"

        result = CliRunner().invoke(
            cli, ["--count", "5", "--threads", "1", "--output-dir", str(output_dir)]
        )

    assert result.exit_code == 0
    assert mock_generate.called
    assert mock_console.print.called


@patch("lg3k.main.RICH_AVAILABLE", False)
def test_cli_no_active_modules():
    """Test CLI with no active modules."""
    with patch("lg3k.main.load_modules") as mock_load:
        mock_load.return_value = {}
        result = CliRunner().invoke(cli, ["--count", "5"])

    assert result.exit_code == 1
    assert "No modules found" in result.output


def test_cli_generate_existing_config(tmp_path):
    """Test generating config when file already exists."""
    config_path = tmp_path / "config.json"
    config_path.write_text("{}")

    result = CliRunner().invoke(cli, ["--generate-config", str(config_path)])

    assert result.exit_code == 0
    assert "already exists" in result.output


@patch("lg3k.main.RICH_AVAILABLE", True)
def test_cli_error_handling():
    """Test error handling with Rich formatting."""
    with patch("lg3k.main.load_config") as mock_config:
        mock_config.side_effect = Exception("Test error")
        result = CliRunner().invoke(cli, ["--count", "5"])

    assert result.exit_code == 1


@patch("lg3k.main.RICH_AVAILABLE", False)
def test_cli_error_handling_no_rich():
    """Test error handling without Rich formatting."""
    with patch("lg3k.main.load_config") as mock_config:
        mock_config.side_effect = Exception("Test error")
        result = CliRunner().invoke(cli, ["--count", "5"])

    assert result.exit_code == 1
    assert "Error: Test error" in result.output


@patch("lg3k.main.RICH_AVAILABLE", True)
def test_cli_no_active_services():
    """Test CLI with no active services in config."""
    with patch("lg3k.main.load_modules") as mock_load, patch(
        "lg3k.main.load_config"
    ) as mock_config:
        mock_load.return_value = {"test": lambda: "test log"}
        mock_config.return_value = {"services": []}
        result = CliRunner().invoke(cli, ["--count", "5"])

    assert result.exit_code == 1


@patch("lg3k.main.RICH_AVAILABLE", True)
def test_cli_module_load_error():
    """Test module loading error with Rich formatting."""
    with patch("lg3k.main.load_modules") as mock_load:
        mock_load.side_effect = ImportError("Test error")
        result = CliRunner().invoke(cli, ["--count", "5"])

    assert result.exit_code == 1


@patch("lg3k.main.RICH_AVAILABLE", True)
@patch("lg3k.main.console")
@patch("rich.panel.Panel")
def test_cli_progress_update(mock_panel, mock_console, tmp_path):
    """Test progress update with Rich formatting."""
    output_dir = tmp_path / "logs"

    mock_panel.fit.return_value = "Configuration Panel"

    with patch("lg3k.main.load_modules") as mock_load, patch(
        "lg3k.main.load_config"
    ) as mock_config, patch("lg3k.main.update_progress") as mock_progress, patch(
        "lg3k.main.generate_module_logs"
    ) as mock_generate:
        mock_load.return_value = {"test": lambda: "test log"}
        mock_config.return_value = {"services": ["test"], "count": 5, "threads": 1}
        mock_progress.return_value = "50%"

        result = CliRunner().invoke(
            cli, ["--count", "5", "--threads", "1", "--output-dir", str(output_dir)]
        )

    assert result.exit_code == 0
    assert mock_generate.called
    assert mock_console.print.called


def test_main():
    """Test main entry point."""
    with patch("lg3k.main.cli") as mock_cli:
        main()
        mock_cli.assert_called_once()


@patch("lg3k.main.RICH_AVAILABLE", True)
@patch("lg3k.main.console")
@patch("lg3k.main.Table")
def test_cli_help_table_with_rich(mock_table, mock_console):
    """Test help table display with Rich formatting."""
    mock_table_instance = MagicMock()
    mock_table.return_value = mock_table_instance

    result = CliRunner().invoke(cli)

    assert result.exit_code == 0
    assert mock_console.print.called
    assert mock_table_instance.add_column.called
    assert mock_table_instance.add_row.called


@patch("lg3k.main.RICH_AVAILABLE", True)
@patch("lg3k.main.console")
def test_cli_module_load_error_with_rich(mock_console):
    """Test module loading error with Rich formatting."""
    with patch("os.listdir") as mock_listdir:
        mock_listdir.return_value = ["test.py"]


@patch("lg3k.main.RICH_AVAILABLE", False)
def test_cli_json_output(tmp_path):
    """Test JSON output mode."""
    output_dir = tmp_path / "logs"

    with patch("lg3k.main.load_modules") as mock_load, patch(
        "lg3k.main.load_config"
    ) as mock_config:
        mock_load.return_value = {"test": lambda: "test log"}
        mock_config.return_value = {"services": ["test"], "count": 5, "threads": 1}
        result = CliRunner().invoke(
            cli,
            [
                "--count",
                "5",
                "--threads",
                "1",
                "--output-dir",
                str(output_dir),
                "--json-output",
            ],
        )

    assert result.exit_code == 0
    output = json.loads(result.output)

    # Basic fields
    assert output["success"] is True
    assert output["logs_generated"] == 5
    assert isinstance(output["time_taken"], float)
    assert len(output["files"]) == 1

    # Stats
    assert "stats" in output
    assert output["stats"]["total_files"] == 1
    assert output["stats"]["avg_logs_per_file"] == 5
    assert isinstance(output["stats"]["total_size_bytes"], int)
    assert output["stats"]["total_size_bytes"] > 0

    # Timing
    assert "timing" in output
    assert isinstance(output["timing"]["start_time"], str)
    assert isinstance(output["timing"]["duration_seconds"], float)
    assert isinstance(output["timing"]["logs_per_second"], float)

    # Config
    assert "config" in output
    assert output["config"]["output_directory"] == str(output_dir)
    assert output["config"]["file_format"] == ".log"


@patch("lg3k.main.RICH_AVAILABLE", False)
def test_cli_json_output_error():
    """Test JSON output mode with error."""
    with patch("lg3k.main.load_config") as mock_config:
        mock_config.side_effect = Exception("Test error")
        result = CliRunner().invoke(cli, ["--count", "5", "--json-output"])

    assert result.exit_code == 1
    output = json.loads(result.output)

    # Basic fields
    assert output["success"] is False
    assert output["logs_generated"] == 0
    assert output["time_taken"] == 0
    assert output["files"] == []

    # Error details
    assert "error" in output
    assert output["error"]["message"] == "Test error"
    assert output["error"]["type"] == "Exception"

    # Stats with no files
    assert output["stats"]["total_files"] == 0
    assert output["stats"]["avg_logs_per_file"] == 0
    assert output["stats"]["total_size_bytes"] == 0

    # Config with no files
    assert output["config"]["output_directory"] is None
    assert output["config"]["file_format"] is None


@patch("lg3k.main.RICH_AVAILABLE", False)
def test_cli_json_output_keyboard_interrupt(tmp_path):
    """Test JSON output mode with keyboard interrupt."""
    output_dir = tmp_path / "logs"

    with patch("lg3k.main.load_modules") as mock_load, patch(
        "lg3k.main.load_config"
    ) as mock_config, patch("lg3k.main.generate_module_logs") as mock_generate:
        mock_load.return_value = {"test": lambda: "test log"}
        mock_config.return_value = {"services": ["test"], "count": 5, "threads": 1}
        mock_generate.side_effect = KeyboardInterrupt()

        # Create a custom exit handler that raises SystemExit with the correct code
        def custom_exit(code=0):
            raise SystemExit(code)

        # Patch both Click's Context.exit and sys.exit
        with patch("click.Context.exit", side_effect=custom_exit), patch(
            "sys.exit", side_effect=custom_exit
        ):
            result = CliRunner(mix_stderr=False).invoke(
                cli,
                [
                    "--count",
                    "5",
                    "--threads",
                    "1",
                    "--output-dir",
                    str(output_dir),
                    "--json-output",
                ],
                catch_exceptions=True,
            )

    assert result.exit_code == 1
    # Get the output and clean it
    output_str = result.stdout.strip()
    output = json.loads(output_str)

    # Basic fields
    assert output["success"] is False
    assert output["logs_generated"] == 0
    assert isinstance(output["time_taken"], float)
    assert output["files"] == []

    # Error details
    assert "error" in output
    assert output["error"]["message"] == "Generation cancelled"
    assert output["error"]["type"] == "str"

    # Stats with no files
    assert output["stats"]["total_files"] == 0
    assert output["stats"]["avg_logs_per_file"] == 0
    assert output["stats"]["total_size_bytes"] == 0

    # Config with no files
    assert output["config"]["output_directory"] is None
    assert output["config"]["file_format"] is None


@patch("lg3k.main.RICH_AVAILABLE", False)
def test_cli_help_no_rich():
    """Test CLI help output without Rich, ensuring the import error message is shown."""
    with patch("builtins.print") as mock_print:
        # Re-import to trigger the ImportError handling
        with patch.dict(
            "sys.modules",
            {"rich.console": None, "rich.table": None, "rich.panel": None},
        ):
            import importlib

            importlib.reload(lg3k.main)
            assert mock_print.called
            assert "Install 'rich' package" in mock_print.call_args[0][0]


@patch("lg3k.main.RICH_AVAILABLE", True)
@patch("lg3k.main.console")
def test_cli_help_with_rich_no_table(mock_console):
    """Test CLI help output with Rich but without Table support."""
    with patch("lg3k.main.Table", None):
        with patch("lg3k.main.show_rich_help") as mock_help:
            result = CliRunner().invoke(cli)
            assert result.exit_code == 0
            assert mock_help.called

            # Call the actual show_rich_help function to test table fallback
            ctx = MagicMock()
            show_rich_help(ctx)

            # Verify basic help was shown without table
            help_calls = [call[0][0] for call in mock_console.print.call_args_list]
            print("\nHelp calls:")
            for call_text in help_calls:
                print(f"  {call_text}")
            assert any("Quick Start:" in call for call in help_calls)
            assert any("Modules:" in call for call in help_calls)
            # Table content should be shown in plain text
            assert any("Options:" in call for call in help_calls)
            assert any("--generate-config PATH" in call for call in help_calls)


@patch("lg3k.main.RICH_AVAILABLE", True)
@patch("lg3k.main.console")
def test_generate_module_logs_with_progress(mock_console, tmp_path):
    """Test log generation with progress updates."""
    output_dir = Path(tmp_path)

    def mock_generator():
        return "test log entry"

    with patch("builtins.print") as mock_print:
        # Clear any existing state
        from lg3k.main import module_order, module_progress, module_status

        module_order.clear()
        module_status.clear()
        module_progress.clear()

        # Generate enough logs to trigger progress update
        generate_module_logs("test_module", mock_generator, 150, output_dir)

        # Verify progress updates were printed
        progress_calls = [
            call
            for call in mock_print.call_args_list
            if isinstance(call[0][0], str)
            and (
                "\033[" in call[0][0]
                or any(  # ANSI escape codes
                    s in call[0][0] for s in ["Running", "Complete", "%"]
                )  # Status messages
            )
        ]
        assert len(progress_calls) > 0


@patch("lg3k.main.RICH_AVAILABLE", True)
@patch("lg3k.main.console")
def test_load_modules_import_error(mock_console, tmp_path):
    """Test module loading with import error."""
    with patch("importlib.import_module") as mock_import, patch(
        "os.listdir"
    ) as mock_listdir, patch("os.path.join") as mock_join:
        mock_listdir.return_value = ["test.py"]
        mock_join.return_value = str(tmp_path / "modules")
        mock_import.side_effect = ImportError("Test import error")

        modules = load_modules()
        assert len(modules) == 0
        assert mock_console.print.called
        # Verify warning was shown
        warning_calls = [
            call
            for call in mock_console.print.call_args_list
            if "Warning: Failed to load module" in str(call)
        ]
        assert len(warning_calls) > 0


@patch("lg3k.main.RICH_AVAILABLE", False)
def test_cli_help_no_rich_with_click():
    """Test CLI help output without Rich, ensuring click.echo is called."""
    with patch("click.echo") as mock_echo:
        ctx = MagicMock()
        show_rich_help(ctx)
        assert mock_echo.called
        assert ctx.get_help.called


@patch("lg3k.main.RICH_AVAILABLE", False)
def test_generate_module_logs_no_rich(tmp_path):
    """Test log generation progress display without Rich."""
    output_dir = Path(tmp_path)

    def mock_generator():
        return "test log entry"

    with patch("builtins.print") as mock_print:
        # Clear any existing state
        from lg3k.main import module_order, module_progress, module_status

        module_order.clear()
        module_status.clear()
        module_progress.clear()

        # Generate enough logs to trigger progress update
        generate_module_logs("test_module", mock_generator, 150, output_dir)

        # Verify progress updates were printed
        progress_calls = [
            call
            for call in mock_print.call_args_list
            if isinstance(call[0][0], str)
            and (
                "\033[" in call[0][0]
                or any(  # ANSI escape codes
                    s in call[0][0] for s in ["Running", "Complete", "%"]
                )  # Status messages
            )
        ]
        assert len(progress_calls) > 0


@patch("lg3k.main.RICH_AVAILABLE", False)
def test_load_modules_import_error_no_rich(tmp_path):
    """Test module loading with import error without Rich."""
    with patch("builtins.print") as mock_print, patch(
        "importlib.import_module"
    ) as mock_import, patch("os.listdir") as mock_listdir, patch(
        "os.path.join"
    ) as mock_join:
        mock_listdir.return_value = ["test.py"]
        mock_join.return_value = str(tmp_path / "modules")
        mock_import.side_effect = ImportError("Test import error")

        modules = load_modules()
        assert len(modules) == 0
        assert mock_print.called
        # Verify warning was shown
        warning_calls = [
            call
            for call in mock_print.call_args_list
            if "Warning: Failed to load module" in str(call)
        ]
        assert len(warning_calls) > 0


def test_format_progress_display():
    """Test progress display formatting."""
    from lg3k.main import module_order, module_progress, module_status

    # Clear any existing state
    module_order.clear()
    module_status.clear()
    module_progress.clear()

    # Add test modules
    module_order.extend(["test1", "test2"])
    module_status.update({"test1": "Running", "test2": "Complete"})
    module_progress.update({"test1": "50.0%", "test2": "100.0%"})

    display = format_progress_display()
    assert "test1" in display
    assert "test2" in display
    assert "50.0%" in display
    assert "Complete" in display


def test_update_progress_display():
    """Test progress display updating."""
    from lg3k.main import module_order, module_progress, module_status

    # Clear any existing state
    module_order.clear()
    module_status.clear()
    module_progress.clear()

    # Add test module
    module_order.append("test")
    module_status["test"] = "Running"
    module_progress["test"] = "50.0%"

    with patch("builtins.print") as mock_print:
        update_progress_display()
        assert mock_print.call_count >= 2  # At least clear and update calls


def test_cleanup_files_error():
    """Test cleanup_files with non-existent files."""
    from lg3k.main import cleanup_files, current_run_files

    # Clear existing files
    current_run_files.clear()
    # Add a non-existent file
    current_run_files.append("non_existent_file.log")
    cleanup_files()  # Should not raise an error
    assert len(current_run_files) == 1  # List is not cleared by cleanup


def test_generate_module_logs_error():
    """Test generate_module_logs with failing generator."""
    import tempfile
    from pathlib import Path

    from lg3k.main import generate_module_logs, module_status

    def failing_generator():
        raise Exception("Test error")

    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir)
        with pytest.raises(Exception):
            generate_module_logs("test_module", failing_generator, 10, output_dir)
        assert "Error" in module_status["test_module"]


def test_format_progress_display_all_states():
    """Test format_progress_display with all possible states."""
    from lg3k.main import (
        format_progress_display,
        module_order,
        module_progress,
        module_status,
    )

    # Clear existing state
    module_status.clear()
    module_progress.clear()
    module_order.clear()

    # Add test modules in different states
    module_order.extend(["test1", "test2", "test3"])
    module_status.update({"test1": "Running", "test2": "Complete", "test3": "Waiting"})
    module_progress["test1"] = "50.0%"

    display = format_progress_display()
    # Check for status strings instead of exact text
    assert any("test1" in line and "50.0%" in line for line in display.split("\n"))
    assert any("test2" in line and "Complete" in line for line in display.split("\n"))
    assert any("test3" in line and "Waiting" in line for line in display.split("\n"))


def test_update_progress_display_empty():
    """Test update_progress_display with no modules."""
    from lg3k.main import module_progress, update_progress_display

    # Clear existing progress
    module_progress.clear()

    # Should not raise any errors
    update_progress_display()


def test_get_terminal_width_error():
    """Test get_terminal_width when shutil.get_terminal_size fails."""
    import shutil

    from lg3k.main import get_terminal_width

    def mock_get_terminal_size():
        raise AttributeError()

    # Save original function
    original_get_terminal_size = shutil.get_terminal_size

    try:
        # Replace with mock
        shutil.get_terminal_size = mock_get_terminal_size
        assert get_terminal_width() == 80
    finally:
        # Restore original function
        shutil.get_terminal_size = original_get_terminal_size


def test_generate_module_logs_exit_event():
    """Test generate_module_logs with exit event set."""
    import tempfile
    from pathlib import Path

    from lg3k.main import (
        current_run_files,
        exit_event,
        generate_module_logs,
        module_order,
        module_progress,
        module_status,
    )

    def test_generator():
        return "test log entry"

    try:
        # Clear all module state
        module_status.clear()
        module_progress.clear()
        module_order.clear()
        current_run_files.clear()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            # Set the exit event
            exit_event.set()
            generate_module_logs("test_module", test_generator, 10, output_dir)
            assert module_status["test_module"] == "Cancelled"
    finally:
        # Clean up
        exit_event.clear()
        current_run_files.clear()
