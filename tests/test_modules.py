"""Tests for the log generation modules."""

from lg3k.modules import api, database, firewall, nas, network, os, printer, web_server


def test_api_log():
    """Test API log generation."""
    log = api.generate_log()
    assert isinstance(log, str)
    assert len(log) > 0


def test_database_log():
    """Test database log generation."""
    log = database.generate_log()
    assert isinstance(log, str)
    assert len(log) > 0


def test_firewall_log():
    """Test firewall log generation."""
    log = firewall.generate_log()
    assert isinstance(log, str)
    assert len(log) > 0


def test_nas_log():
    """Test NAS log generation."""
    log = nas.generate_log()
    assert isinstance(log, str)
    assert len(log) > 0


def test_network_log():
    """Test network log generation."""
    log = network.generate_log()
    assert isinstance(log, str)
    assert len(log) > 0


def test_os_log():
    """Test OS log generation."""
    log = os.generate_log()
    assert isinstance(log, str)
    assert len(log) > 0


def test_printer_log():
    """Test printer log generation."""
    log = printer.generate_log()
    assert isinstance(log, str)
    assert len(log) > 0


def test_web_server_log():
    """Test web server log generation."""
    log = web_server.generate_log()
    assert isinstance(log, str)
    assert len(log) > 0
