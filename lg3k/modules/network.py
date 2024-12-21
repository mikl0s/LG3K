"""Network log generator module for LG3K.

This module generates realistic network logs including connectivity events,
bandwidth usage, and network device status.
"""

import random

from ..utils.timestamp import get_timestamp


def generate_log():
    """Generate a single network log entry.

    Returns:
        str: A formatted log string in the format "[timestamp] [level] [component] message"
    """
    timestamp = get_timestamp()
    devices = ["Router", "Switch", "WAP", "Gateway"]
    events = ["UP", "DOWN", "DEGRADED", "CONGESTED"]
    metrics = ["latency", "bandwidth", "packet_loss", "jitter"]

    device = random.choice(devices)
    event = random.choice(events)
    metric = random.choice(metrics)
    value = round(random.uniform(0, 100), 2)

    level = "INFO" if event == "UP" else "WARNING"
    message = f"{device} status {event} - {metric}: {value}%"

    return f"[{timestamp}] [{level}] [Network] {message}"
