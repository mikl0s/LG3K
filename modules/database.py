"""Database log generator module for LG3K.

This module generates realistic database operation logs including queries,
transactions, and performance metrics.
"""

import random

from utils.timestamp import generate_timestamp


def generate_log():
    """Generate a single database log entry.

    Returns:
        dict: A log entry containing timestamp, level, component, and database-specific details.
    """
    timestamp = generate_timestamp()
    operations = ["SELECT", "INSERT", "UPDATE", "DELETE", "TRANSACTION"]
    tables = ["users", "posts", "comments", "settings", "logs"]

    operation = random.choice(operations)
    table = random.choice(tables)
    duration = round(random.uniform(0.001, 2.000), 3)

    return {
        "timestamp": timestamp,
        "level": "INFO",
        "component": "Database",
        "message": f"DB {operation} on {table} - Duration: {duration}s",
    }
