"""Tests for utility functions."""

import json
from datetime import datetime
from unittest.mock import patch

import pytest

from lg3k.utils.config import get_default_config, load_config
from lg3k.utils.progress import update_progress
from lg3k.utils.timestamp import get_timestamp


def test_get_default_config():
    """Test getting default configuration."""
    config = get_default_config()
    assert isinstance(config, dict)
    assert "count" in config
    assert "threads" in config
    assert "output_dir" in config
    assert "log_levels" in config
    assert "components" in config
    assert "services" in config
    assert "api" in config
    assert "database" in config
    assert "network" in config
    # Verify specific values
    assert config["output_dir"] == "logs"
    assert config["count"] == 100
    assert isinstance(config["threads"], int)
    assert len(config["services"]) == 8  # All services included
    assert len(config["log_levels"]) == 5  # All log levels included


def test_load_config():
    """Test configuration loading with no file."""
    config = load_config()
    assert isinstance(config, dict)
    assert "log_levels" in config
    assert "components" in config
    assert "services" in config
    assert "count" in config
    assert "threads" in config
    assert "output_dir" in config
    # Verify default values
    assert config["output_dir"] == "logs"
    assert config["count"] == 100
    assert isinstance(config["threads"], int)


def test_load_config_from_file(tmp_path):
    """Test loading configuration from file."""
    config_path = tmp_path / "config.json"
    test_config = {
        "services": ["web_server"],
        "count": 200,
        "threads": 4,
        "output_dir": "custom_logs",
    }
    with open(config_path, "w") as f:
        json.dump(test_config, f)

    config = load_config(str(config_path))
    assert config == test_config
    assert config["count"] == 200
    assert config["threads"] == 4
    assert config["output_dir"] == "custom_logs"


def test_load_config_invalid_file():
    """Test loading configuration from non-existent file."""
    config = load_config("nonexistent.json")
    assert isinstance(config, dict)
    assert config["output_dir"] == "logs"  # Default value
    assert config["count"] == 100  # Default value


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


def test_create_progress_bar_full():
    """Test progress bar creation at 100%."""
    from lg3k.utils.progress import create_progress_bar

    bar = create_progress_bar(100.0)
    assert bar == "[====================]"


def test_create_progress_bar_custom_width():
    """Test progress bar creation with custom width."""
    from lg3k.utils.progress import create_progress_bar

    bar = create_progress_bar(50.0, width=10)
    assert bar == "[=====>    ]"


def test_create_progress_bar_zero():
    """Test progress bar creation at 0%."""
    from lg3k.utils.progress import create_progress_bar

    bar = create_progress_bar(0.0)
    assert bar == "[>                   ]"


def test_update_progress_edge_cases():
    """Test update_progress with edge cases."""
    from lg3k.utils.progress import update_progress

    # Test 0%
    assert "0.0%" in update_progress(0, 100)
    # Test 100%
    assert "100.0%" in update_progress(100, 100)
    # Test intermediate value
    assert "50.0%" in update_progress(50, 100)
