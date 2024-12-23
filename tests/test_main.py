"""Tests for the main module."""

import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from lg3k.main import (
    format_json_output,
    format_progress_display,
    generate_logs,
    get_module_id,
    handle_error,
    update_progress,
)


def test_show_rich_help():
    """Test showing rich help."""
    with patch("lg3k.main.HAS_RICH", True):
        with patch("lg3k.main.Console") as mock_console_class:
            result = format_progress_display()
            assert isinstance(result, str)
