"""Tests for the main module."""

import json
from unittest.mock import patch

import pytest

from lg3k.main import generate_log, load_modules, main


def test_load_modules():
    """Test that modules can be loaded."""
    modules = load_modules()
    assert len(modules) > 0


def test_generate_log():
    """Test that logs can be generated."""
    log = generate_log()
    assert isinstance(log, str)
    assert len(log) > 0


def test_generate_log_no_modules():
    """Test generate_log with no modules available."""
    with patch("lg3k.main.load_modules", return_value={}):
        with pytest.raises(RuntimeError, match="No log generation modules found"):
            generate_log()


def test_main_with_config(tmp_path):
    """Test main function with config file."""
    config_path = tmp_path / "config.json"
    config = {
        "services": ["web_server", "api"],
        "total_logs": 10,
        "split_size": 5,
        "max_threads": 2,
    }
    with open(config_path, "w") as f:
        json.dump(config, f)

    with patch("lg3k.main.load_config") as mock_load_config:
        mock_load_config.return_value = config
        with patch("lg3k.main.update_progress") as mock_update:
            main()
            mock_update.assert_called_once()


def test_main_no_active_modules():
    """Test main function with no active modules."""
    with patch("lg3k.main.load_config") as mock_load_config:
        mock_load_config.return_value = {"services": []}
        with patch("builtins.print") as mock_print:
            main()
            mock_print.assert_called_once_with(
                "No active modules found. Check your configuration."
            )
