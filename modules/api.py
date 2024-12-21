
import random
from utils.timestamp import generate_timestamp

def generate_log():
    timestamp = generate_timestamp()
    level = random.choice(["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"])
    api_service = random.choice(["Cloudflare", "AmazonS3", "Stripe", "Twilio", "SendGrid"])
    status = random.choice(["200 OK", "401 Unauthorized", "500 Internal Server Error"])
    if "200" in status:
        message = f"API {api_service} responded with {status}."
    else:
        message = f"API {api_service} error: {status}."
    return {
        "timestamp": timestamp,
        "level": level,
        "component": api_service,
        "message": message,
    }
