"""Web server log generator module for LG3K.

This module generates realistic web server logs including HTTP requests,
response codes, and performance metrics.
"""

import random

from ..utils.timestamp import get_timestamp


def generate_log():
    """Generate a single web server log entry.

    Returns:
        str: A formatted log string in the format "[timestamp] [level] [component] message"
    """
    timestamp = get_timestamp()
    methods = ["GET", "POST", "PUT", "DELETE"]
    paths = ["/", "/about", "/contact", "/api/v1", "/docs"]
    codes = [200, 201, 301, 304, 400, 401, 403, 404, 500]

    method = random.choice(methods)
    path = random.choice(paths)
    code = random.choice(codes)
    ip = (
        f"{random.randint(1, 255)}.{random.randint(0, 255)}."
        f"{random.randint(0, 255)}.{random.randint(0, 255)}"
    )

    level = "INFO" if code < 400 else "ERROR"
    message = f"{ip} - {method} {path} - {code}"

    return f"[{timestamp}] [{level}] [WebServer] {message}"
