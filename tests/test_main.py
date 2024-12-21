"""Tests for the main module."""

from lg3k.main import generate_log, load_modules


def test_load_modules():
    """Test that modules can be loaded."""
    modules = load_modules()
    assert len(modules) > 0


def test_generate_log():
    """Test that logs can be generated."""
    log = generate_log()
    assert isinstance(log, str)
    assert len(log) > 0
