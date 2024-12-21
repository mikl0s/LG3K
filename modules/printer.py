"""Printer log generator module for LG3K.

This module generates realistic printer logs including print jobs,
supply levels, and printer status events.
"""

import random

from utils.timestamp import generate_timestamp


def generate_log():
    """Generate a single printer log entry.

    Returns:
        dict: A log entry containing timestamp, level, component, and printer-specific details.
    """
    timestamp = generate_timestamp()
    job_types = ["document", "photo", "label", "report"]
    statuses = ["completed", "pending", "error", "cancelled"]
    supplies = ["black", "cyan", "magenta", "yellow"]

    job = random.choice(job_types)
    status = random.choice(statuses)
    supply = random.choice(supplies)
    pages = random.randint(1, 50)
    level = random.randint(0, 100)

    return {
        "timestamp": timestamp,
        "level": "ERROR" if status == "error" else "INFO",
        "component": "Printer",
        "message": f"Print job ({job}, {pages} pages) {status} - {supply} at {level}%",
    }
