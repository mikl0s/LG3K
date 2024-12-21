"""Network Attached Storage (NAS) log generator module for LG3K.

This module generates realistic NAS logs including file operations,
storage metrics, and access events.
"""

import random

from ..utils.timestamp import get_timestamp


def generate_log():
    """Generate a single NAS log entry.

    Returns:
        str: A formatted log string in the format "[timestamp] [level] [component] message"
    """
    timestamp = get_timestamp()
    operations = ["READ", "WRITE", "DELETE", "MOVE", "COPY"]
    file_types = ["document", "image", "video", "backup", "archive"]
    shares = ["public", "private", "backup", "media"]

    operation = random.choice(operations)
    file_type = random.choice(file_types)
    share = random.choice(shares)
    size = round(random.uniform(0.1, 1000.0), 2)

    # Create log dictionary first
    log_entry = {
        "timestamp": timestamp,
        "level": "INFO",
        "component": "NAS",
        "message": f"{operation} {file_type} ({size}MB) on {share} share",
    }

    # Format and return as string
    return f"[{log_entry['timestamp']}] [{log_entry['level']}] [{log_entry['component']}] {log_entry['message']}"
