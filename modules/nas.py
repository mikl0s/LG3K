"""Network Attached Storage (NAS) log generator module for LG3K.

This module generates realistic NAS logs including file operations,
storage metrics, and access events.
"""

import random

from utils.timestamp import generate_timestamp


def generate_log():
    """Generate a single NAS log entry.

    Returns:
        dict: A log entry containing timestamp, level, component, and NAS-specific details.
    """
    timestamp = generate_timestamp()
    operations = ["READ", "WRITE", "DELETE", "MOVE", "COPY"]
    file_types = ["document", "image", "video", "backup", "archive"]
    shares = ["public", "private", "backup", "media"]

    operation = random.choice(operations)
    file_type = random.choice(file_types)
    share = random.choice(shares)
    size = round(random.uniform(0.1, 1000.0), 2)

    return {
        "timestamp": timestamp,
        "level": "INFO",
        "component": "NAS",
        "message": f"{operation} {file_type} ({size}MB) on {share} share",
    }
