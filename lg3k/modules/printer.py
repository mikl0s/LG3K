"""Printer log generator module for LG3K.

This module generates realistic printer logs including print jobs,
supply levels, and printer status events.
"""

import random

from ..utils.timestamp import get_timestamp


def generate_log():
    """Generate a single printer log entry.

    Returns:
        str: A formatted log string in the format "[timestamp] [level] [component] message"
    """
    timestamp = get_timestamp()
    job_types = ["document", "photo", "label", "report"]
    statuses = ["completed", "pending", "error", "cancelled"]
    supplies = ["black", "cyan", "magenta", "yellow"]

    job = random.choice(job_types)
    status = random.choice(statuses)
    supply = random.choice(supplies)
    pages = random.randint(1, 50)
    level = random.randint(0, 100)

    # Create log components
    level_str = "ERROR" if status == "error" else "INFO"
    message = f"Print job ({job}, {pages} pages) {status} - {supply} at {level}%"

    # Return formatted string instead of dictionary
    return f"[{timestamp}] [{level_str}] [Printer] {message}"
