"""Firewall log generator module for LG3K.

This module generates realistic firewall logs including connection attempts,
blocked IPs, and security events.
"""

import random

from ..utils.timestamp import get_timestamp


def generate_log():
    """Generate a single firewall log entry.

    Returns:
        str: A formatted log string in the format "[timestamp] [level] [component] message"
    """
    timestamp = get_timestamp()
    actions = ["ALLOW", "BLOCK", "DROP"]
    protocols = ["TCP", "UDP", "ICMP"]
    ports = [22, 80, 443, 3306, 5432]

    action = random.choice(actions)
    protocol = random.choice(protocols)
    port = random.choice(ports)
    ip = (
        f"{random.randint(1, 255)}.{random.randint(0, 255)}."
        f"{random.randint(0, 255)}.{random.randint(0, 255)}"
    )

    level = "INFO" if action == "ALLOW" else "WARNING"
    message = f"{action} {protocol} from {ip} on port {port}"

    # Return formatted string instead of dictionary
    return f"[{timestamp}] [{level}] [Firewall] {message}"
