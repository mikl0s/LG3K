"""Tests for the log generation modules."""

import json
from datetime import datetime

from lg3k.modules import api, database, firewall, nas, network, os, printer, web_server


def test_api_log():
    """Test API log generation."""
    log = api.generate_log()
    assert isinstance(log, str)
    assert len(log) > 0


def test_database_log():
    """Test database log generation."""
    log = database.generate_log()
    assert isinstance(log, str)
    assert len(log) > 0


def test_firewall_log():
    """Test firewall log generation."""
    log = firewall.generate_log()
    assert isinstance(log, str)
    assert len(log) > 0


def test_nas_log():
    """Test NAS log generation."""
    log = nas.generate_log()
    assert isinstance(log, str)
    assert len(log) > 0


def test_network_log():
    """Test network log generation."""
    log = network.generate_log()
    assert isinstance(log, str)
    assert len(log) > 0


def test_os_log():
    """Test OS log generation."""
    log = os.generate_log()
    assert isinstance(log, str)
    assert len(log) > 0


def test_printer_log():
    """Test printer log generation."""
    log = printer.generate_log()
    assert isinstance(log, str)
    assert len(log) > 0


def test_web_server_log():
    """Test web server log generation."""
    log = web_server.generate_log()
    assert isinstance(log, str)
    assert len(log) > 0


def test_smarthome_log():
    """Test smart home log generation."""
    from lg3k.modules.smarthome import generate_log

    # Test multiple times to cover different device types
    for _ in range(50):  # Test enough times to likely hit all device types
        log_entry = generate_log()
        assert isinstance(log_entry, str)
        assert datetime.fromisoformat(
            json.loads(log_entry.split(": ", 1)[1])["timestamp"]
        )


def test_smarthome_home_device_log():
    """Test home device log generation."""
    from datetime import datetime

    from lg3k.modules.smarthome import generate_home_device_log

    timestamp = datetime.now()
    log_entry = generate_home_device_log(timestamp)
    assert isinstance(log_entry, str)
    data = json.loads(log_entry.split(": ", 1)[1])
    assert data["timestamp"] == timestamp.isoformat()
    assert data["type"] in ["thermostat", "light", "motion_sensor", "door_lock"]
    assert data["location"] in [
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


def test_smarthome_esp_log():
    """Test ESP device log generation."""
    from datetime import datetime

    from lg3k.modules.smarthome import generate_esp_log

    timestamp = datetime.now()
    log_entry = generate_esp_log(timestamp)
    assert isinstance(log_entry, str)
    data = json.loads(log_entry.split(": ", 1)[1])
    assert data["timestamp"] == timestamp.isoformat()
    assert data["type"] in ["ESP32", "ESP8266"]
    assert isinstance(data["cpu_freq"], int)
    assert isinstance(data["temperature"], float)
    assert isinstance(data["voltage"], float)
    assert isinstance(data["free_heap"], int)
    assert isinstance(data["wifi_rssi"], int)


def test_smarthome_wireless_log():
    """Test wireless device log generation."""
    from datetime import datetime

    from lg3k.modules.smarthome import generate_wireless_log

    timestamp = datetime.now()
    log_entry = generate_wireless_log(timestamp)
    assert isinstance(log_entry, str)
    data = json.loads(log_entry.split(": ", 1)[1])
    assert data["timestamp"] == timestamp.isoformat()
    assert data["protocol"] in ["zigbee", "zwave"]
    assert isinstance(data["network_id"], str)
    assert isinstance(data["rssi"], int)
    assert isinstance(data["lqi"], int)


def test_smarthome_camera_log():
    """Test camera log generation."""
    from datetime import datetime

    from lg3k.modules.smarthome import generate_camera_log

    timestamp = datetime.now()
    log_entry = generate_camera_log(timestamp)
    assert isinstance(log_entry, str)
    data = json.loads(log_entry.split(": ", 1)[1])
    assert data["timestamp"] == timestamp.isoformat()
    assert data["type"] in ["ip_camera", "doorbell", "ptz_camera"]
    assert data["location"] in [
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
    assert data["resolution"] in ["720p", "1080p", "2K", "4K"]
    assert isinstance(data["fps"], int)


def test_smarthome_home_device_log_all_types():
    """Test home device log generation for all device types and states."""
    from datetime import datetime

    from lg3k.modules.smarthome import HOME_DEVICES, generate_home_device_log

    timestamp = datetime.now()

    # Test each device type
    for device_type, info in HOME_DEVICES.items():
        for _ in range(10):  # Multiple attempts to hit different states
            log_entry = generate_home_device_log(timestamp)
            data = json.loads(log_entry.split(": ", 1)[1])

            if device_type == data["type"]:
                assert data["state"] in info["states"]
                if device_type == "thermostat":
                    assert "temperature" in data
                    assert "humidity" in data
                elif device_type == "light" and data["state"] == "dimmed":
                    assert "brightness" in data
                elif device_type in ["motion_sensor", "door_lock"]:
                    assert "battery_level" in data


def test_smarthome_esp_log_all_operations():
    """Test ESP log generation for all operations."""
    from datetime import datetime

    from lg3k.modules.smarthome import ESP_DEVICES, generate_esp_log

    timestamp = datetime.now()

    # Test each ESP type and operation
    for esp_type, info in ESP_DEVICES.items():
        for operation in info["operations"]:
            for _ in range(5):  # Multiple attempts to hit different combinations
                log_entry = generate_esp_log(timestamp)
                data = json.loads(log_entry.split(": ", 1)[1])

                if data["type"] == esp_type and data["operation"] == operation:
                    if operation == "Deep sleep":
                        assert "sleep_duration" in data
                    elif operation == "ADC reading":
                        assert "adc_value" in data
                    elif operation == "MQTT publish":
                        assert "topic" in data
                        assert "qos" in data
                    elif operation == "OTA update":
                        assert "firmware_version" in data


def test_smarthome_wireless_log_all_types():
    """Test wireless log generation for all protocols and device types."""
    from datetime import datetime

    from lg3k.modules.smarthome import WIRELESS_DEVICES, generate_wireless_log

    timestamp = datetime.now()

    # Test each protocol and device type
    for protocol, devices in WIRELESS_DEVICES.items():
        for device_type, info in devices.items():
            for _ in range(10):  # Multiple attempts to hit different events
                log_entry = generate_wireless_log(timestamp)
                data = json.loads(log_entry.split(": ", 1)[1])

                if data["protocol"] == protocol and data["type"] == device_type:
                    assert data["event"] in info["events"]
                    if protocol == "zigbee":
                        assert "pan_id" in data
                        if device_type == "coordinator":
                            assert isinstance(data.get("channel"), int)
                            if data["event"] == "device_join":
                                assert "new_device" in data
                        elif device_type == "end_device":
                            assert "cluster" in data
                            assert "battery" in data
                        elif device_type == "router":
                            assert "children" in data
                    else:  # zwave
                        assert "home_id" in data
                        if device_type == "controller":
                            assert isinstance(data.get("channel"), int)
                            if data["event"] == "inclusion":
                                assert "new_node_id" in data
                        elif device_type == "slave":
                            assert "command_class" in data
                            assert "battery" in data
                        elif device_type == "routing_slave":
                            assert "routes" in data


def test_smarthome_camera_log_all_types():
    """Test camera log generation for all types and events."""
    from datetime import datetime

    from lg3k.modules.smarthome import CAMERA_EVENTS, CAMERAS, generate_camera_log

    timestamp = datetime.now()

    # Test each camera type and event
    for camera_type in CAMERAS.keys():
        for event_type in CAMERA_EVENTS.keys():
            for _ in range(10):  # Multiple attempts to hit different combinations
                log_entry = generate_camera_log(timestamp)
                data = json.loads(log_entry.split(": ", 1)[1])

                if data["type"] == camera_type and data["event"] == event_type:
                    if camera_type == "ip_camera":
                        assert "protocol" in data
                        assert "codec" in data
                        assert "bitrate" in data
                    elif camera_type == "doorbell":
                        assert "battery_level" in data
                        if event_type == "motion_detected":
                            assert "detection_zone" in data
                    elif camera_type == "ptz_camera":
                        if event_type != "system":
                            assert "movement" in data
                            if data["movement"] == "preset":
                                assert "preset_number" in data
                            else:
                                assert "position" in data

                    if event_type == "motion_detected":
                        assert "confidence" in data
                        assert "detection_area" in data
                    elif event_type == "recording":
                        assert "duration" in data
                        assert "file_size" in data
                    elif event_type == "system" and data["event_details"] == "error":
                        assert "error" in data
                        assert data["error"] in [
                            "network_timeout",
                            "storage_full",
                            "auth_failed",
                        ]


def test_smarthome_log_all_categories():
    """Test smart home log generation for all categories."""
    from lg3k.modules.smarthome import generate_log

    # Test each category multiple times
    categories = {"home": 0, "esp": 0, "wireless": 0, "camera": 0}

    # Run enough times to hit all categories
    for _ in range(100):
        log_entry = generate_log()
        data = json.loads(log_entry.split(": ", 1)[1])

        # Determine category from the log data
        if "state" in data:  # home device
            categories["home"] += 1
        elif "operation" in data:  # esp device
            categories["esp"] += 1
        elif "protocol" in data:  # wireless device
            categories["wireless"] += 1
        elif "camera_id" in data:  # camera device
            categories["camera"] += 1

    # Verify all categories were hit
    assert all(
        count > 0 for count in categories.values()
    ), f"Not all categories were hit: {categories}"
