
import random
from utils.timestamp import generate_timestamp

def generate_log():
    timestamp = generate_timestamp()
    level = random.choice(["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"])
    nas = random.choice(["TrueNAS", "QNAP", "Synology", "Unraid"])
    if level in ["ERROR", "CRITICAL"]:
        message = f"{nas} reported a disk failure."
    else:
        message = f"{nas} storage check passed."
    return {
        "timestamp": timestamp,
        "level": level,
        "component": nas,
        "message": message,
    }
