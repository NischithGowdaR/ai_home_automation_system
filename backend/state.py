import datetime

DEVICE_DEFAULTS = {
    "Living Room Light":  {"icon": "💡", "room": "Living Room",  "type": "light",       "on": True,  "brightness": 80},
    "Bedroom Light":      {"icon": "🛏️", "room": "Bedroom",      "type": "light",       "on": False, "brightness": 60},
    "Kitchen Light":      {"icon": "🍳", "room": "Kitchen",      "type": "light",       "on": True,  "brightness": 100},
    "Thermostat":         {"icon": "🌡️", "room": "Home",         "type": "thermostat",  "on": True,  "temp": 22},
    "Front Door Lock":    {"icon": "🔒", "room": "Entrance",     "type": "lock",        "on": True,  "locked": True},
    "Living Room Fan":    {"icon": "🌀", "room": "Living Room",  "type": "fan",         "on": False, "speed": 2},
    "Smart TV":           {"icon": "📺", "room": "Living Room",  "type": "tv",          "on": False, "channel": 5},
    "Security Camera":    {"icon": "📷", "room": "Entrance",     "type": "camera",      "on": True,  "recording": True},
    "Garage Door":        {"icon": "🚗", "room": "Garage",       "type": "garage",      "on": False, "open": False},
    "Garden Sprinkler":   {"icon": "💧", "room": "Garden",       "type": "sprinkler",   "on": False, "schedule": "06:00"},
    "Bedroom AC":         {"icon": "❄️", "room": "Bedroom",      "type": "ac",          "on": False, "temp": 20},
    "Porch Light":        {"icon": "🏮", "room": "Porch",        "type": "light",       "on": True,  "brightness": 50},
}

devices = {k: dict(v) for k, v in DEVICE_DEFAULTS.items()}

action_log = [
    {"time": "08:00", "action": "Morning Routine triggered", "device": "System", "type": "routine"},
    {"time": "08:01", "action": "Kitchen Light turned ON", "device": "Kitchen Light", "type": "device"},
    {"time": "08:02", "action": "Thermostat set to 22°C", "device": "Thermostat", "type": "device"},
    {"time": "08:05", "action": "Porch Light turned ON", "device": "Porch Light", "type": "device"},
]

routines = [
    {"name": "Good Morning", "trigger": "07:00 AM daily", "actions": ["Turn on Kitchen Light", "Set Thermostat to 22°C", "Unlock Front Door"], "active": True},
    {"name": "Good Night",   "trigger": "11:00 PM daily", "actions": ["Turn off all lights", "Lock Front Door", "Set Thermostat to 18°C"], "active": True},
    {"name": "Away Mode",    "trigger": "Manual",         "actions": ["Turn off all devices", "Lock Front Door", "Enable Security Camera"], "active": False},
]

def log_action(action: str, device: str = "System", log_type: str = "device"):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    action_log.insert(0, {
        "time": now, "action": action, "device": device, "type": log_type
    })
    if len(action_log) > 50:
        action_log[:] = action_log[:50]

def reset_devices():
    global devices
    devices.clear()
    devices.update({k: dict(v) for k, v in DEVICE_DEFAULTS.items()})
    log_action("All devices reset to defaults", "System", "system")

def clear_log():
    global action_log
    action_log.clear()

def get_home_state_string() -> str:
    lines = []
    for name, d in devices.items():
        status = "ON" if d["on"] else "OFF"
        extra = ""
        if d["type"] == "thermostat": extra = f", temp={d.get('temp',22)}°C"
        elif d["type"] == "light":    extra = f", brightness={d.get('brightness',100)}%"
        elif d["type"] == "lock":     extra = f", locked={d.get('locked', True)}"
        elif d["type"] == "fan":      extra = f", speed={d.get('speed',1)}/3"
        lines.append(f"- {name} ({d['room']}): {status}{extra}")
    return "\n".join(lines)
