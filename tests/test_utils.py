"""Tests for utility functions."""

from datetime import datetime

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
    try:
        datetime.fromisoformat(timestamp)
    except ValueError:
        pytest.fail("Invalid timestamp format")
