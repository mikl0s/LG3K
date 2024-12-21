
import random
from utils.timestamp import generate_timestamp

def generate_log():
    timestamp = generate_timestamp()
    level = random.choice(["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"])
    device = random.choice(["Unifi", "Netgear", "MikroTik", "Cisco"])
    if level in ["ERROR", "CRITICAL"]:
        message = f"{device} detected packet loss."
    else:
        message = f"{device} network performance is normal."
    return {
        "timestamp": timestamp,
        "level": level,
        "component": device,
        "message": message,
    }
