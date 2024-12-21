
import random
from utils.timestamp import generate_timestamp

def generate_log():
    timestamp = generate_timestamp()
    level = random.choice(["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"])
    firewall = random.choice(["pfSense", "OPNsense", "iptables", "CiscoASA"])
    if level in ["WARNING", "ERROR", "CRITICAL"]:
        message = f"{firewall} detected unusual traffic."
    else:
        message = f"{firewall} is operating normally."
    return {
        "timestamp": timestamp,
        "level": level,
        "component": firewall,
        "message": message,
    }
