
import random
from utils.timestamp import generate_timestamp

def generate_log():
    timestamp = generate_timestamp()
    level = random.choice(["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"])
    printer = random.choice(["HP", "Brother", "Canon", "Epson"])
    if level in ["ERROR", "CRITICAL"]:
        message = f"{printer} printer is out of toner."
    else:
        message = f"{printer} printed successfully."
    return {
        "timestamp": timestamp,
        "level": level,
        "component": printer,
        "message": message,
    }
