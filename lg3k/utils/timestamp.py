"""Timestamp generation utilities."""

from datetime import datetime


def get_timestamp() -> str:
    """Get current timestamp in ISO format.

    Returns:
        ISO formatted timestamp string
    """
    return datetime.now().isoformat()
