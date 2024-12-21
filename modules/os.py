
import random
from utils.timestamp import generate_timestamp

def generate_log():
    timestamp = generate_timestamp()
    level = random.choice(["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"])
    os_type = random.choice(["Linux", "Windows", "FreeBSD", "OpenBSD"])
    if level in ["ERROR", "CRITICAL"]:
        message = f"{os_type} system encountered a kernel panic."
    else:
        message = f"{os_type} system uptime is normal."
    return {
        "timestamp": timestamp,
        "level": level,
        "component": os_type,
        "message": message,
    }
