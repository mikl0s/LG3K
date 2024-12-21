
import random
from utils.timestamp import generate_timestamp

def generate_log():
    timestamp = generate_timestamp()
    level = random.choice(["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"])
    db_type = random.choice(["PostgreSQL", "MySQL", "SQLServer"])
    if level in ["ERROR", "CRITICAL"]:
        error = random.choice([
            "Connection timeout",
            "Authentication failed",
            "Query syntax error",
            "Deadlock detected",
            "Disk I/O error",
            "Out of memory",
        ])
        message = f"{db_type} error: {error}"
    else:
        message = f"{db_type} query executed successfully."
    return {
        "timestamp": timestamp,
        "level": level,
        "component": db_type,
        "message": message,
    }
