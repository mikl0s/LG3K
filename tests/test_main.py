"""Test suite for the main module."""

from main import generate_log, load_modules


def test_generate_log():
    """Test the generate_log function."""
    log = generate_log()
    assert isinstance(log, dict)
    assert "timestamp" in log
    assert "level" in log
    assert "component" in log
    assert "message" in log
    assert log["component"] == "Main"


def test_load_modules():
    """Test the load_modules function."""
    modules = load_modules()
    assert isinstance(modules, dict)
    assert len(modules) > 0
    # Check if all expected modules are loaded
    expected_modules = [
        "api",
        "database",
        "firewall",
        "nas",
        "network",
        "os",
        "printer",
        "web_server",
    ]
    for module in expected_modules:
        assert module in modules
        assert callable(modules[module])
