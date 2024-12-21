"""Configuration loading utilities."""

import json
import os
from typing import Dict


def load_config(config_file: str = "config.json") -> Dict:
    """Load configuration from file or return defaults.

    Args:
        config_file: Path to config file (default: config.json)

    Returns:
        Configuration dictionary
    """
    if os.path.exists(config_file):
        with open(config_file) as f:
            return json.load(f)

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
    }
