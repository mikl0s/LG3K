"""Tests for utility functions."""

import json
from datetime import datetime
from unittest.mock import patch

import pytest

from lg3k.utils.config import load_config
from lg3k.utils.progress import update_progress
from lg3k.utils.timestamp import get_timestamp


def test_load_config():
    """Test configuration loading."""
    config = load_config()
    assert isinstance(config, dict)
    assert "log_levels" in config
    assert "components" in config


def test_load_config_from_file(tmp_path):
    """Test loading configuration from file."""
    config_path = tmp_path / "config.json"
    test_config = {"services": ["web_server"], "total_logs": 100}
    with open(config_path, "w") as f:
        json.dump(test_config, f)

    config = load_config(str(config_path))
    assert config == test_config


def test_update_progress():
    """Test progress bar updates."""
    result = update_progress(50, 100)
    assert isinstance(result, str)
    assert "%" in result


def test_get_timestamp():
    """Test timestamp generation."""
    timestamp = get_timestamp()
    assert isinstance(timestamp, str)
    # Verify timestamp format
    dt = datetime.fromisoformat(timestamp)
    assert isinstance(dt, datetime)
    # Verify it's a recent timestamp
    now = datetime.now()
    diff = now - dt
    assert diff.total_seconds() < 1  # Less than 1 second difference


def test_get_timestamp_error():
    """Test timestamp generation with error."""
    with patch("lg3k.utils.timestamp.datetime") as mock_dt:
        mock_dt.now.side_effect = ValueError("Test error")
        with pytest.raises(ValueError):
            get_timestamp()
