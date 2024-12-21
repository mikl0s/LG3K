"""API log generator module for LG3K.

This module generates realistic API request logs with various endpoints,
methods, and response codes.
"""

import random

from ..utils.timestamp import get_timestamp


def generate_log():
    """Generate a single API log entry.

    Returns:
        str: A formatted log string in the format "[timestamp] [level] [component] message"
    """
    timestamp = get_timestamp()
    endpoints = ["/api/v1/users", "/api/v1/posts", "/api/v1/comments", "/api/v1/auth"]
    methods = ["GET", "POST", "PUT", "DELETE"]
    status_codes = [200, 201, 400, 401, 403, 404, 500]

    endpoint = random.choice(endpoints)
    method = random.choice(methods)
    status = random.choice(status_codes)

    # Format message to stay within line length limit
    msg = f"API Request - {method} {endpoint} - Status: {status}"
    level = "INFO" if status < 400 else "ERROR"

    # Return formatted string instead of dictionary
    return f"[{timestamp}] [{level}] [API] {msg}"
