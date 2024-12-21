"""Test suite for log generation modules."""

import re
from datetime import datetime

import pytest

from modules import api, database, firewall, nas, network
from modules import os as os_module
from modules import printer, web_server


def validate_log_structure(log):
    """Validate the basic structure of a log entry."""
    assert isinstance(log, dict)
    assert "timestamp" in log
    assert "level" in log
    assert "component" in log
    assert "message" in log
    # Verify timestamp format
    try:
        datetime.fromisoformat(log["timestamp"])
    except ValueError:
        pytest.fail("Invalid timestamp format")


def test_api_log():
    """Test API log generation."""
    log = api.generate_log()
    validate_log_structure(log)
    assert log["component"] == "API"
    assert "API Request" in log["message"]
    assert any(method in log["message"] for method in ["GET", "POST", "PUT", "DELETE"])


def test_database_log():
    """Test database log generation."""
    log = database.generate_log()
    validate_log_structure(log)
    assert log["component"] == "Database"
    assert any(op in log["message"] for op in ["SELECT", "INSERT", "UPDATE", "DELETE"])
    assert "Duration:" in log["message"]


def test_firewall_log():
    """Test firewall log generation."""
    log = firewall.generate_log()
    validate_log_structure(log)
    assert log["component"] == "Firewall"
    assert any(action in log["message"] for action in ["ALLOW", "BLOCK", "DROP"])
    # Verify IP address format
    ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    assert re.search(ip_pattern, log["message"])


def test_nas_log():
    """Test NAS log generation."""
    log = nas.generate_log()
    validate_log_structure(log)
    assert log["component"] == "NAS"
    assert any(
        op in log["message"] for op in ["READ", "WRITE", "DELETE", "MOVE", "COPY"]
    )
    assert "MB" in log["message"]


def test_network_log():
    """Test network log generation."""
    log = network.generate_log()
    validate_log_structure(log)
    assert log["component"] == "Network"
    assert any(
        device in log["message"] for device in ["Router", "Switch", "WAP", "Gateway"]
    )
    assert "%" in log["message"]


def test_os_log():
    """Test OS log generation."""
    log = os_module.generate_log()
    validate_log_structure(log)
    assert log["component"] == "OS"
    assert any(
        event in log["message"]
        for event in ["started", "stopped", "restarted", "failed"]
    )
    assert "%" in log["message"]


def test_printer_log():
    """Test printer log generation."""
    log = printer.generate_log()
    validate_log_structure(log)
    assert log["component"] == "Printer"
    assert any(
        status in log["message"]
        for status in ["completed", "pending", "error", "cancelled"]
    )
    assert "pages" in log["message"]


def test_web_server_log():
    """Test web server log generation."""
    log = web_server.generate_log()
    validate_log_structure(log)
    assert log["component"] == "WebServer"
    assert any(
        str(code) in log["message"]
        for code in [200, 201, 301, 304, 400, 401, 403, 404, 500]
    )
    # Verify IP address format
    ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
    assert re.search(ip_pattern, log["message"])
