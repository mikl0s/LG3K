"""Tests for the main module."""

import os
import tempfile
from unittest.mock import patch

from lg3k.main import (
    format_json_output,
    format_progress_display,
    generate_module_logs,
    update_progress,
)


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


def test_update_progress():
    """Test progress updates."""
    with patch("lg3k.main.update_progress_display"):
        update_progress("test_module", "75%")
        from lg3k.main import module_progress, module_status

        assert module_progress["test_module"] == "75%"
        assert module_status["test_module"] == "Running"
