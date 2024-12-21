"""Operating System log generator module for LG3K.

This module generates realistic OS logs including system events,
resource usage, and service status changes.
"""

import random

from utils.timestamp import generate_timestamp


def generate_log():
    """Generate a single OS log entry.

    Returns:
        dict: A log entry containing timestamp, level, component, and OS-specific details.
    """
    timestamp = generate_timestamp()
    resources = ["CPU", "Memory", "Disk", "Swap"]
    services = ["sshd", "httpd", "mysqld", "nginx"]
    events = ["started", "stopped", "restarted", "failed"]

    resource = random.choice(resources)
    service = random.choice(services)
    event = random.choice(events)
    usage = round(random.uniform(0, 100), 1)

    return {
        "timestamp": timestamp,
        "level": "ERROR" if event == "failed" else "INFO",
        "component": "OS",
        "message": f"Service {service} {event} - {resource} usage: {usage}%",
    }
