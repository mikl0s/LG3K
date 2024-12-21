"""Timestamp utility module for LG3K.

This module provides functionality for generating consistent timestamps
for log entries, supporting various timestamp formats.
"""

from datetime import datetime


def generate_timestamp():
    """Generate a timestamp in ISO format.

    Returns:
        str: Current timestamp in ISO format (YYYY-MM-DD HH:MM:SS.mmmmmm+HH:MM).
    """
    return datetime.now().isoformat()
