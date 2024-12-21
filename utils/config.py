"""Configuration utility module for LG3K.

This module handles loading and validating configuration settings from JSON files,
providing default values when needed.
"""

import json
import os


def load_config(config_file):
    """Load configuration from a JSON file.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        dict: Configuration settings with defaults applied if file doesn't exist.
    """
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return json.load(f)

    # Default configuration
    return {
        "services": ["web_server"],
        "total_logs": 1000,
        "split_size": 100,
        "max_threads": 4,
    }
