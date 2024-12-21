"""Database log generator module for LG3K.

This module generates realistic database operation logs including queries,
transactions, and performance metrics.
"""

import random

from ..utils.timestamp import get_timestamp


def generate_log():
    """Generate a single database log entry.

    Returns:
        str: A formatted log string in the format "[timestamp] [level] [component] message"
    """
    timestamp = get_timestamp()
    operations = ["SELECT", "INSERT", "UPDATE", "DELETE", "TRANSACTION"]
    tables = ["users", "posts", "comments", "settings", "logs"]

    operation = random.choice(operations)
    table = random.choice(tables)
    duration = round(random.uniform(0.001, 2.000), 3)

    # Create log components
    level = "INFO"
    component = "Database"
    message = f"DB {operation} on {table} - Duration: {duration}s"

    # Return formatted string instead of dictionary
    return f"[{timestamp}] [{level}] [{component}] {message}"
