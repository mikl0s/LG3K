"""Smart home device log generation module."""

import json
import random
from datetime import datetime

# Locations for devices
LOCATIONS = [
    "living_room",
    "kitchen",
    "bedroom",
    "bathroom",
    "garage",
    "hallway",
    "front_door",
    "back_door",
    "driveway",
    "backyard",
    "side_gate",
]

# Smart home device types and their possible states
HOME_DEVICES = {
    "thermostat": {
        "states": ["heating", "cooling", "idle", "fan_only"],
    },
    "light": {
        "states": ["on", "off", "dimmed"],
    },
    "motion_sensor": {
        "states": ["motion_detected", "clear", "tamper"],
    },
    "door_lock": {
        "states": ["locked", "unlocked", "jammed"],
    },
}

# ESP device types and their operations
ESP_DEVICES = {
    "ESP32": {
        "operations": ["Deep sleep", "ADC reading", "MQTT publish", "OTA update"],
        "cores": [0, 1],
        "freq_range": (80, 240),
        "temp_range": (20, 85),
        "voltage_range": (2.3, 3.6),
    },
    "ESP8266": {
        "operations": ["Deep sleep", "ADC reading", "MQTT publish", "OTA update"],
        "cores": [0],
        "freq_range": (80, 160),
        "temp_range": (20, 85),
        "voltage_range": (2.5, 3.6),
    },
}

# Wireless device types and their events
WIRELESS_DEVICES = {
    "zigbee": {
        "coordinator": {
            "events": ["device_join", "device_leave", "network_scan", "channel_change"]
        },
        "end_device": {"events": ["data_send", "sleep", "wake", "battery_report"]},
        "router": {
            "events": ["route_update", "neighbor_table", "child_join", "child_leave"]
        },
    },
    "zwave": {
        "controller": {"events": ["inclusion", "exclusion", "heal", "network_update"]},
        "slave": {"events": ["command", "report", "sleep", "wake"]},
        "routing_slave": {
            "events": ["route_update", "neighbor_table", "forward", "ack"]
        },
    },
}

# Camera types and their events
CAMERAS = {
    "ip_camera": ["rtsp", "onvif", "http"],
    "doorbell": ["battery", "wired"],
    "ptz_camera": ["indoor", "outdoor"],
}

CAMERA_EVENTS = {
    "motion_detected": ["person", "vehicle", "animal", "package"],
    "recording": ["continuous", "motion", "scheduled"],
    "system": ["startup", "shutdown", "error"],
}


def generate_log():
    """Generate a random smart home device log entry."""
    timestamp = datetime.now()
    category = random.choice(["home", "esp", "wireless", "camera"])

    if category == "home":
        return generate_home_device_log(timestamp)
    elif category == "esp":
        return generate_esp_log(timestamp)
    elif category == "wireless":
        return generate_wireless_log(timestamp)
    else:  # camera
        return generate_camera_log(timestamp)


def generate_home_device_log(timestamp):
    """Generate a log entry for a smart home device."""
    device_type = random.choice(list(HOME_DEVICES.keys()))
    device_info = HOME_DEVICES[device_type]
    state = random.choice(device_info["states"])
    location = random.choice(LOCATIONS)

    msg = {
        "timestamp": timestamp.isoformat(),
        "type": device_type,
        "location": location,
        "state": state,
        "device_id": f"{device_type}_{random.randint(1, 100)}",
    }

    # Add device-specific data
    if device_type == "thermostat":
        msg.update(
            {
                "temperature": round(random.uniform(18.0, 25.0), 1),
                "humidity": random.randint(30, 70),
            }
        )
    elif device_type == "light" and state == "dimmed":
        msg["brightness"] = random.randint(10, 90)
    elif device_type in ["motion_sensor", "door_lock"]:
        msg["battery_level"] = random.randint(10, 100)

    return f"SmartHome: {json.dumps(msg)}"


def generate_esp_log(timestamp):
    """Generate a log entry for an ESP device."""
    device_type = random.choice(list(ESP_DEVICES.keys()))
    device_info = ESP_DEVICES[device_type]
    operation = random.choice(device_info["operations"])
    core = random.choice(device_info["cores"])

    msg = {
        "timestamp": timestamp.isoformat(),
        "type": device_type,
        "operation": operation,
        "core": core,
        "device_id": f"{device_type}_{random.randint(1, 100)}",
        "cpu_freq": random.randint(*device_info["freq_range"]),
        "temperature": round(random.uniform(*device_info["temp_range"]), 1),
        "voltage": round(random.uniform(*device_info["voltage_range"]), 2),
        "free_heap": random.randint(20000, 200000),
        "wifi_rssi": random.randint(-90, -30),
    }

    # Add operation-specific data
    if operation == "Deep sleep":
        msg["sleep_duration"] = random.randint(1, 3600)
    elif operation == "ADC reading":
        msg["adc_value"] = random.randint(0, 4095)
    elif operation == "MQTT publish":
        msg.update(
            {"topic": f"sensor/{device_type.lower()}/data", "qos": random.randint(0, 2)}
        )
    elif operation == "OTA update":
        msg["firmware_version"] = f"{random.randint(1, 5)}.{random.randint(0, 9)}"

    return f"SmartHome: {json.dumps(msg)}"


def generate_wireless_log(timestamp):
    """Generate a log entry for a wireless device."""
    protocol = random.choice(list(WIRELESS_DEVICES.keys()))
    device_type = random.choice(list(WIRELESS_DEVICES[protocol].keys()))
    device_info = WIRELESS_DEVICES[protocol][device_type]
    event = random.choice(device_info["events"])

    msg = {
        "timestamp": timestamp.isoformat(),
        "protocol": protocol,
        "type": device_type,
        "event": event,
        "device_id": f"{protocol}_{device_type}_{random.randint(1, 100)}",
    }

    # Add protocol-specific data
    if protocol == "zigbee":
        msg["pan_id"] = f"{random.randint(0, 65535):04x}"
        if device_type == "coordinator":
            msg["channel"] = random.randint(11, 26)
            if event == "device_join":
                msg["new_device"] = f"device_{random.randint(1, 100)}"
        elif device_type == "end_device":
            msg.update(
                {
                    "cluster": f"0x{random.randint(0, 65535):04x}",
                    "battery": random.randint(0, 100),
                }
            )
        elif device_type == "router":
            msg["children"] = random.randint(0, 20)
    else:  # zwave
        msg["home_id"] = f"{random.randint(0, 0xFFFFFFFF):08x}"
        if device_type == "controller":
            msg["channel"] = random.randint(1, 50)
            if event == "inclusion":
                msg["new_node_id"] = random.randint(1, 232)
        elif device_type == "slave":
            msg.update(
                {
                    "command_class": f"0x{random.randint(0, 255):02x}",
                    "battery": random.randint(0, 100),
                }
            )
        elif device_type == "routing_slave":
            msg["routes"] = random.randint(1, 10)

    return f"SmartHome: {json.dumps(msg)}"


def generate_camera_log(timestamp):
    """Generate a log entry for a security camera."""
    camera_type = random.choice(list(CAMERAS.keys()))
    event_type = random.choice(list(CAMERA_EVENTS.keys()))
    event_details = random.choice(CAMERA_EVENTS[event_type])
    location = random.choice(LOCATIONS)

    msg = {
        "timestamp": timestamp.isoformat(),
        "type": camera_type,
        "camera_id": f"{camera_type}_{random.randint(1, 100)}",
        "location": location,
        "event": event_type,
        "event_details": event_details,
        "resolution": random.choice(["720p", "1080p", "2K", "4K"]),
        "fps": random.randint(15, 60),
    }

    # Add camera-specific data
    if camera_type == "ip_camera":
        msg.update(
            {
                "protocol": random.choice(CAMERAS["ip_camera"]),
                "codec": random.choice(["H.264", "H.265"]),
                "bitrate": f"{random.randint(1, 8)}Mbps",
            }
        )
    elif camera_type == "doorbell":
        msg["battery_level"] = random.randint(10, 100)
        if event_type == "motion_detected":
            msg["detection_zone"] = random.choice(["entry", "street", "porch"])
    elif camera_type == "ptz_camera":
        if event_type != "system":
            movement = random.choice(["pan", "tilt", "zoom", "preset"])
            msg["movement"] = movement
            if movement == "preset":
                msg["preset_number"] = random.randint(1, 10)
            else:
                msg["position"] = (
                    random.randint(-180, 180)
                    if movement != "zoom"
                    else random.randint(1, 20)
                )

    # Add event-specific data
    if event_type == "motion_detected":
        msg.update(
            {
                "confidence": random.randint(50, 100),
                "detection_area": random.choice(["left", "center", "right"]),
            }
        )
    elif event_type == "recording":
        msg.update(
            {
                "duration": random.randint(10, 300),
                "file_size": f"{random.randint(1, 100)}MB",
            }
        )
    elif event_type == "system" and event_details == "error":
        msg["error"] = random.choice(["network_timeout", "storage_full", "auth_failed"])

    return f"SmartHome: {json.dumps(msg)}"
