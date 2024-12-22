"""Configuration loading utilities."""

import json
import multiprocessing
import os
from typing import Dict


def get_default_config() -> Dict:
    """Get a full-featured default configuration.

    Returns:
        Configuration dictionary with all available options
    """
    return {
        # Log generation settings
        "count": 100,  # Number of logs per module
        "threads": multiprocessing.cpu_count(),  # Default to system CPU count
        "output_dir": "logs",  # Default output directory
        # Log content configuration
        "log_levels": ["INFO", "WARNING", "ERROR", "CRITICAL", "DEBUG"],
        "components": [
            "API",
            "Database",
            "Firewall",
            "NAS",
            "Network",
            "OS",
            "Printer",
            "WebServer",
        ],
        # Active services (comment out or remove services you don't want)
        "services": [
            "api",  # API endpoint logs
            "database",  # Database operation logs
            "firewall",  # Firewall event logs
            "nas",  # Network storage logs
            "network",  # Network traffic logs
            "os",  # Operating system logs
            "printer",  # Printer activity logs
            "web_server",  # Web server access logs
        ],
        # Module-specific settings
        "api": {
            "endpoints": ["/api/v1/users", "/api/v1/posts", "/api/v1/auth"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "status_codes": [200, 201, 400, 401, 403, 404, 500],
        },
        "database": {
            "operations": ["SELECT", "INSERT", "UPDATE", "DELETE"],
            "tables": ["users", "posts", "comments", "sessions"],
        },
        "network": {"ports": [80, 443, 22, 3306], "protocols": ["TCP", "UDP"]},
    }


def load_config(config_file: str = "config.json") -> Dict:
    """Load configuration from file or return defaults.

    Args:
        config_file: Path to config file (default: config.json)

    Returns:
        Configuration dictionary
    """
    # Try to load from current directory first
    if os.path.exists(config_file):
        with open(config_file) as f:
            return json.load(f)

    # If no config file found, return minimal defaults
    return {
        "log_levels": ["INFO", "WARNING", "ERROR", "CRITICAL", "DEBUG"],
        "components": [
            "API",
            "Database",
            "Firewall",
            "NAS",
            "Network",
            "OS",
            "Printer",
            "WebServer",
        ],
        "services": [
            "api",
            "database",
            "firewall",
            "nas",
            "network",
            "os",
            "printer",
            "web_server",
        ],
        "count": 100,  # Default number of logs per module
        "threads": multiprocessing.cpu_count(),  # Default to system CPU count
        "output_dir": "logs",  # Default output directory
    }
