"""Test suite for utility modules."""

import json
from datetime import datetime
from unittest.mock import MagicMock, mock_open, patch

import pytest

from utils.config import load_config
from utils.progress import run_with_progress
from utils.timestamp import generate_timestamp


def test_generate_timestamp():
    """Test the timestamp generation function."""
    timestamp = generate_timestamp()
    assert isinstance(timestamp, str)
    # Verify it's a valid ISO format timestamp
    try:
        datetime.fromisoformat(timestamp)
    except ValueError:
        pytest.fail("Invalid timestamp format")


def test_load_config_existing_file():
    """Test loading configuration from an existing file."""
    test_config = {
        "services": ["test_service"],
        "total_logs": 500,
        "split_size": 50,
        "max_threads": 2,
    }
    mock_file = mock_open(read_data=json.dumps(test_config))

    with patch("builtins.open", mock_file), patch("os.path.exists", return_value=True):
        config = load_config("test_config.json")
        assert config == test_config


def test_load_config_default():
    """Test loading default configuration when file doesn't exist."""
    with patch("os.path.exists", return_value=False):
        config = load_config("nonexistent.json")
        assert isinstance(config, dict)
        assert "services" in config
        assert "total_logs" in config
        assert "split_size" in config
        assert "max_threads" in config


def test_run_with_progress():
    """Test the progress tracking function."""
    mock_callback = MagicMock(return_value={"test": "data"})
    total = 5

    results = run_with_progress(total, mock_callback)

    assert len(results) == total
    assert mock_callback.call_count == total
    assert all(isinstance(r, dict) for r in results)
