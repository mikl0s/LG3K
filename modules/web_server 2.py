
import random
from utils.timestamp import generate_timestamp

def generate_log():
    timestamp = generate_timestamp()
    level = random.choice(["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"])
    return {
        "timestamp": timestamp,
        "level": level,
        "component": "WebServer",
        "message": "Web server processed request successfully."
        if level != "ERROR"
        else "Web server encountered an error.",
    }
