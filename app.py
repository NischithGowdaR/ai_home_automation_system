import streamlit as st
from groq import Groq
import json
import datetime
import random
import speech_recognition as sr
from io import BytesIO


# Load Groq API Key from .env or Streamlit secrets
from dotenv import load_dotenv
load_dotenv()
import os
groq_api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY") 

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SmartHome AI",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Root & Base ── */
html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background: #0a0e1a;
    color: #ffffff;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0f1629 !important;
    border-right: 1px solid #1e2d4a;
}
[data-testid="stSidebar"] * { color: #e0e0e0 !important; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #ffffff !important; }

/* ── Headers ── */
h1, h2, h3 {
    font-family: 'Space Mono', monospace !important;
    letter-spacing: -0.5px;
}

/* ── Device Cards ── */
.device-card {
    background: linear-gradient(135deg, #111827 0%, #1a2540 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 20px;
    margin: 8px 0;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.device-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px; height: 100%;
    background: #3b82f6;
    border-radius: 4px 0 0 4px;
}
.device-card.on::before { background: #10b981; }
.device-card.off::before { background: #374151; }

.device-icon { font-size: 2rem; margin-bottom: 8px; }
.device-name {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    color: #e0e0e0;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.device-status-on  { color: #10b981; font-weight: 600; font-size: 0.9rem; }
.device-status-off { color: #4b5563; font-weight: 600; font-size: 0.9rem; }

/* ── Command Box ── */
.command-section {
    background: linear-gradient(135deg, #0f172a, #1e1b4b);
    border: 1px solid #3730a3;
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 24px;
}
.command-hint {
    font-size: 0.8rem;
    color: #a5b4fc;
    font-family: 'Space Mono', monospace;
    margin-bottom: 12px;
}

/* ── Log Entries ── */
.log-entry {
    background: #111827;
    border-left: 3px solid #3b82f6;
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    margin: 6px 0;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    color: #e0e0e0;
}
.log-entry .log-time { color: #a5b4fc; }
.log-entry .log-action { color: #ffffff; }

/* ── Routine Cards ── */
.routine-card {
    background: #111827;
    border: 1px solid #1f2937;
    border-radius: 12px;
    padding: 16px;
    margin: 8px 0;
}
.routine-name {
    font-family: 'Space Mono', monospace;
    font-size: 0.9rem;
    color: #e0b4fc;
    font-weight: 700;
}
.routine-detail { font-size: 0.82rem; color: #b0b0b0; margin-top: 4px; }

/* ── Metric Cards ── */
.metric-card {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    border: 1px solid #1e3a5f;
    border-radius: 14px;
    padding: 18px;
    text-align: center;
}
.metric-value {
    font-family: 'Space Mono', monospace;
    font-size: 2rem;
    font-weight: 700;
    color: #38bdf8;
}
.metric-label { font-size: 0.8rem; color: #d0d0d0; margin-top: 4px; }

/* ── AI Response ── */
.ai-response {
    background: linear-gradient(135deg, #0c1a0c, #0a1a1f);
    border: 1px solid #166534;
    border-radius: 14px;
    padding: 20px;
    margin: 16px 0;
    font-size: 0.92rem;
    line-height: 1.6;
    color: #d1fae5;
}
.ai-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #10b981;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 8px;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #1d4ed8, #4338ca) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    padding: 0.5rem 1.4rem !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #2563eb, #4f46e5) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 15px rgba(99,102,241,0.4) !important;
}

/* ── Text Input ── */
.stTextInput input {
    background: #1a2540 !important;
    border: 1px solid #2d4a7a !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Selectbox / Toggle ── */
.stSelectbox select, .stSelectbox > div {
    background: #1a2540 !important;
    color: #e2e8f0 !important;
}

/* ── Section title ── */
.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 3px;
    color: #a0a0a0;
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid #1e293b;
}

/* ── Temp badge ── */
.temp-badge {
    display: inline-block;
    background: linear-gradient(135deg, #b45309, #d97706);
    color: white;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.8rem;
    font-weight: 700;
    font-family: 'Space Mono', monospace;
}

/* ── Scene Buttons ── */
.scene-btn {
    background: linear-gradient(135deg, #1e1b4b, #312e81);
    border: 1px solid #4338ca;
    border-radius: 12px;
    color: #a5b4fc;
    padding: 12px 16px;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
    cursor: pointer;
    text-align: center;
    transition: all 0.2s;
}
</style>
""", unsafe_allow_html=True)

# ── State Initialization ──────────────────────────────────────────────────────
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

if "devices" not in st.session_state:
    st.session_state.devices = {k: dict(v) for k, v in DEVICE_DEFAULTS.items()}

if "action_log" not in st.session_state:
    st.session_state.action_log = [
        {"time": "08:00", "action": "Morning Routine triggered", "device": "System", "type": "routine"},
        {"time": "08:01", "action": "Kitchen Light turned ON", "device": "Kitchen Light", "type": "device"},
        {"time": "08:02", "action": "Thermostat set to 22°C", "device": "Thermostat", "type": "device"},
        {"time": "08:05", "action": "Porch Light turned ON", "device": "Porch Light", "type": "device"},
    ]

if "routines" not in st.session_state:
    st.session_state.routines = [
        {"name": "Good Morning", "trigger": "07:00 AM daily", "actions": ["Turn on Kitchen Light", "Set Thermostat to 22°C", "Unlock Front Door"], "active": True},
        {"name": "Good Night",   "trigger": "11:00 PM daily", "actions": ["Turn off all lights", "Lock Front Door", "Set Thermostat to 18°C"], "active": True},
        {"name": "Away Mode",    "trigger": "Manual",         "actions": ["Turn off all devices", "Lock Front Door", "Enable Security Camera"], "active": False},
    ]

if "ai_response" not in st.session_state:
    st.session_state.ai_response = ""

if "last_command" not in st.session_state:
    st.session_state.last_command = ""

# ── Helper Functions ──────────────────────────────────────────────────────────
def log_action(action: str, device: str = "System", log_type: str = "device"):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.action_log.insert(0, {
        "time": now, "action": action, "device": device, "type": log_type
    })
    if len(st.session_state.action_log) > 50:
        st.session_state.action_log = st.session_state.action_log[:50]

def toggle_device(name: str):
    d = st.session_state.devices[name]
    d["on"] = not d["on"]
    status = "ON" if d["on"] else "OFF"
    log_action(f"{name} turned {status}", name)

def get_home_state() -> str:
    lines = []
    for name, d in st.session_state.devices.items():
        status = "ON" if d["on"] else "OFF"
        extra = ""
        if d["type"] == "thermostat": extra = f", temp={d.get('temp',22)}°C"
        elif d["type"] == "light":    extra = f", brightness={d.get('brightness',100)}%"
        elif d["type"] == "lock":     extra = f", locked={d.get('locked', True)}"
        elif d["type"] == "fan":      extra = f", speed={d.get('speed',1)}/3"
        lines.append(f"- {name} ({d['room']}): {status}{extra}")
    return "\n".join(lines)

def apply_ai_commands(commands: list):
    """Apply structured commands returned by AI."""
    for cmd in commands:
        action = cmd.get("action", "").lower()
        target = cmd.get("target", "")
        value  = cmd.get("value", None)

        # Match target to device names
        matched = [n for n in st.session_state.devices if target.lower() in n.lower()]

        if action == "turn_on":
            for name in matched:
                st.session_state.devices[name]["on"] = True
                log_action(f"{name} turned ON via voice command", name)
            if not matched and "all light" in target.lower():
                for name, d in st.session_state.devices.items():
                    if d["type"] == "light":
                        d["on"] = True
                        log_action(f"{name} turned ON via voice command", name)

        elif action == "turn_off":
            for name in matched:
                st.session_state.devices[name]["on"] = False
                log_action(f"{name} turned OFF via voice command", name)
            if not matched and "all light" in target.lower():
                for name, d in st.session_state.devices.items():
                    if d["type"] == "light":
                        d["on"] = False
                        log_action(f"{name} turned OFF via voice command", name)

        elif action == "set_temp" and value:
            for name in matched:
                if st.session_state.devices[name]["type"] in ("thermostat", "ac"):
                    st.session_state.devices[name]["temp"] = int(value)
                    st.session_state.devices[name]["on"] = True
                    log_action(f"{name} set to {value}°C via voice command", name)

        elif action == "set_brightness" and value:
            for name in matched:
                if st.session_state.devices[name]["type"] == "light":
                    st.session_state.devices[name]["brightness"] = int(value)
                    st.session_state.devices[name]["on"] = True
                    log_action(f"{name} brightness set to {value}% via voice command", name)

        elif action == "lock":
            for name in matched:
                if st.session_state.devices[name]["type"] == "lock":
                    st.session_state.devices[name]["locked"] = True
                    st.session_state.devices[name]["on"] = True
                    log_action(f"{name} locked via voice command", name)

        elif action == "unlock":
            for name in matched:
                if st.session_state.devices[name]["type"] == "lock":
                    st.session_state.devices[name]["locked"] = False
                    log_action(f"{name} unlocked via voice command", name)

def process_voice_command(command: str):
    """Send command to Groq and apply results."""
    client = Groq(api_key=groq_api_key)
    home_state = get_home_state()

    system_prompt = """You are an AI home automation assistant. The user gives voice-style natural language commands to control their smart home.

Your job:
1. Understand the command
2. Return a friendly confirmation message explaining what you did
3. Return structured commands to execute

Always respond in this exact JSON format:
{
  "message": "Friendly response to the user (1-2 sentences)",
  "commands": [
    {"action": "turn_on|turn_off|set_temp|set_brightness|lock|unlock", "target": "device name or type", "value": null_or_number}
  ]
}

Supported actions: turn_on, turn_off, set_temp (°C), set_brightness (0-100%), lock, unlock
Device types: light, thermostat, fan, tv, lock, camera, garage, sprinkler, ac

Return ONLY valid JSON, no markdown."""

    user_prompt = f"""Current home state:
{home_state}

User command: "{command}"

Execute the appropriate actions and respond in JSON format."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=600,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    raw = response.choices[0].message.content.strip()
    # Strip JSON fences if present
    raw = raw.replace("```json", "").replace("```", "").strip()
    result = json.loads(raw)

    ai_msg = result.get("message", "Done!")
    commands = result.get("commands", [])
    apply_ai_commands(commands)
    log_action(f'Voice command: "{command}"', "AI Agent", "voice")
    return ai_msg

def transcribe_audio(audio_file) -> str:
    """Transcribe audio file to text using speech_recognition."""
    try:
        recognizer = sr.Recognizer()
        
        # Handle Streamlit UploadedFile object
        if hasattr(audio_file, 'read'):
            audio_bytes = audio_file.read()
        else:
            audio_bytes = audio_file
        
        # Use AudioFile to handle audio properly
        from io import BytesIO
        audio_stream = BytesIO(audio_bytes)
        
        with sr.AudioFile(audio_stream) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand what you said. Please try again."
    except sr.RequestError as e:
        return f"Error with speech recognition service: {str(e)}"
    except Exception as e:
        return f"Error processing audio: {str(e)}"

def run_scene(scene: str):
    scenes = {
        "🌅 Morning":  [("Kitchen Light", True), ("Living Room Light", True), ("Porch Light", False)],
        "🎬 Movie":    [("Living Room Light", False), ("Smart TV", True), ("Living Room Fan", True)],
        "😴 Sleep":    [("Living Room Light", False), ("Bedroom Light", False), ("Front Door Lock", True)],
        "🏃 Away":     [("Living Room Light", False), ("Kitchen Light", False), ("Security Camera", True)],
    }
    actions = scenes.get(scene, [])
    for name, state in actions:
        if name in st.session_state.devices:
            st.session_state.devices[name]["on"] = state
            log_action(f"[{scene} scene] {name} {'ON' if state else 'OFF'}", name, "scene")
    log_action(f"Scene activated: {scene}", "System", "scene")

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🏠 SmartHome AI")
    st.markdown("---")

    # Stats
    devices   = st.session_state.devices
    total     = len(devices)
    on_count  = sum(1 for d in devices.values() if d["on"])
    lights_on = sum(1 for d in devices.values() if d["type"] == "light" and d["on"])
    thermo    = next((d for d in devices.values() if d["type"] == "thermostat"), {})
    temp_val  = thermo.get("temp", 22)

    st.markdown(f"""
    <div class="metric-card" style="margin-bottom:10px;">
        <div class="metric-value">{on_count}/{total}</div>
        <div class="metric-label">Devices Active</div>
    </div>
    <div class="metric-card" style="margin-bottom:10px;">
        <div class="metric-value">{lights_on}</div>
        <div class="metric-label">Lights On</div>
    </div>
    <div class="metric-card" style="margin-bottom:24px;">
        <div class="metric-value">{temp_val}°C</div>
        <div class="metric-label">Thermostat</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">Quick Scenes</div>', unsafe_allow_html=True)
    for scene in ["🌅 Morning", "🎬 Movie", "😴 Sleep", "🏃 Away"]:
        if st.button(scene, key=f"scene_{scene}", use_container_width=True):
            run_scene(scene)
            st.rerun()

    st.markdown("---")
    st.markdown('<div class="section-title">System</div>', unsafe_allow_html=True)

    if st.button("🔄 Reset Devices", use_container_width=True):
        st.session_state.devices = {k: dict(v) for k, v in DEVICE_DEFAULTS.items()}
        log_action("All devices reset to defaults", "System", "system")
        st.rerun()

    if st.button("🗑️ Clear Log", use_container_width=True):
        st.session_state.action_log = []
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("# 🏠 SmartHome AI Dashboard")
st.markdown('<p style="color:#c0c0c0; font-family:\'DM Sans\'; margin-top:-8px;">AI-powered home automation • Voice commands • Smart routines</p>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["🎙️ Voice Control", "📱 Devices", "⚡ Routines", "📋 Action Log"])

# ── TAB 1 : VOICE CONTROL ─────────────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-title">AI Voice Command Center</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="command-section">
        <div class="command-hint">// SPEAK TO YOUR HOME</div>
        <p style="color:#e0e0e0; font-size:0.9rem; margin-bottom:0;">
            Type natural commands like you'd speak them. The AI will interpret your intent and control your devices automatically.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Example commands
    example_cmds = [
        "Turn on all the lights",
        "Set thermostat to 24°C",
        "Good night mode — lock up and turn off everything",
        "Dim the living room light to 40%",
        "Turn on the bedroom AC at 19°C",
        "Unlock the front door",
    ]

    st.markdown("**💡 Try these commands:**")
    cols = st.columns(3)
    for i, ex in enumerate(example_cmds):
        with cols[i % 3]:
            if st.button(f'"{ex}"', key=f"ex_{i}", use_container_width=True):
                st.session_state.last_command = ex

    st.markdown("---")

    # 🎤 VOICE INPUT SECTION
    st.markdown('<div class="section-title">🎤 Voice Input</div>', unsafe_allow_html=True)
    
    audio_bytes = st.audio_input("Click the microphone to record your command", key="voice_recording")
    
    if audio_bytes:
        st.info("🔄 Transcribing your voice command...")
        transcribed_text = transcribe_audio(audio_bytes)
        
        if transcribed_text and not any(err in transcribed_text.lower() for err in ["error", "couldn't understand"]):
            st.session_state.last_command = transcribed_text
            st.success(f"✅ Heard: *{transcribed_text}*")
            
            with st.spinner("🤖 AI processing your command..."):
                try:
                    response_msg = process_voice_command(transcribed_text)
                    st.session_state.ai_response = response_msg
                except Exception as e:
                    st.session_state.ai_response = f"⚠️ Error: {str(e)}"
            st.rerun()
        else:
            st.warning(f"⚠️ {transcribed_text}")

    st.markdown("---")
    st.markdown('<div class="section-title">📝 Or Type Your Command</div>', unsafe_allow_html=True)

    command = st.text_input(
        "🎙️ Your Command",
        value=st.session_state.last_command,
        placeholder='e.g. "Turn off kitchen light and set thermostat to 20°C"',
        key="voice_input"
    )

    col_send, col_clear = st.columns([1, 4])
    with col_send:
        send = st.button("▶ Execute", use_container_width=True)

    if send and command.strip():
        with st.spinner("🤖 AI processing your command..."):
            try:
                response_msg = process_voice_command(command.strip())
                st.session_state.ai_response = response_msg
                st.session_state.last_command = ""
            except Exception as e:
                st.session_state.ai_response = f"⚠️ Error: {str(e)}"
        st.rerun()

    if st.session_state.ai_response:
        st.markdown(f"""
        <div class="ai-response">
            <div class="ai-label">🤖 AI Response</div>
            {st.session_state.ai_response}
        </div>
        """, unsafe_allow_html=True)

    # Quick toggles
    st.markdown("---")
    st.markdown('<div class="section-title">Quick Toggles</div>', unsafe_allow_html=True)
    qcols = st.columns(4)
    quick = ["Living Room Light", "Kitchen Light", "Smart TV", "Living Room Fan"]
    for i, name in enumerate(quick):
        d = st.session_state.devices[name]
        with qcols[i]:
            status = "🟢 ON" if d["on"] else "⚫ OFF"
            if st.button(f"{d['icon']} {name.split()[0]}\n{status}", key=f"q_{name}", use_container_width=True):
                toggle_device(name)
                st.rerun()

# ── TAB 2 : DEVICES ──────────────────────────────────────────────────────────
with tab2:
    st.markdown('<div class="section-title">Device Control Panel</div>', unsafe_allow_html=True)

    # Filter by room
    rooms = sorted(set(d["room"] for d in st.session_state.devices.values()))
    rooms.insert(0, "All Rooms")
    selected_room = st.selectbox("Filter by Room", rooms, key="room_filter")

    filtered = {
        k: v for k, v in st.session_state.devices.items()
        if selected_room == "All Rooms" or v["room"] == selected_room
    }

    device_names = list(filtered.keys())
    cols_per_row = 3
    for i in range(0, len(device_names), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, name in enumerate(device_names[i:i+cols_per_row]):
            d = st.session_state.devices[name]
            css_class = "on" if d["on"] else "off"
            status_class = "device-status-on" if d["on"] else "device-status-off"
            status_text = "● ON" if d["on"] else "○ OFF"

            # Extra info
            extra_html = ""
            if d["type"] in ("thermostat", "ac"):
                extra_html = f'<br><span class="temp-badge">{d.get("temp",22)}°C</span>'
            elif d["type"] == "light":
                bri = d.get("brightness", 100)
                extra_html = f'<br><small style="color:#c0c0c0;">Brightness: {bri}%</small>'
            elif d["type"] == "lock":
                locked = d.get("locked", True)
                extra_html = f'<br><small style="color:{"#10b981" if locked else "#ef4444"};">{"🔒 Locked" if locked else "🔓 Unlocked"}</small>'

            with cols[j]:
                st.markdown(f"""
                <div class="device-card {css_class}">
                    <div class="device-icon">{d['icon']}</div>
                    <div class="device-name">{name}</div>
                    <div class="{status_class}">{status_text}</div>
                    <small style="color:#b0b0b0;">{d['room']}</small>
                    {extra_html}
                </div>
                """, unsafe_allow_html=True)

                if st.button("Toggle", key=f"tog_{name}", use_container_width=True):
                    toggle_device(name)
                    st.rerun()

                # Extra controls
                if d["type"] in ("thermostat", "ac") and d["on"]:
                    new_temp = st.slider(f"Temp", 16, 30, d.get("temp", 22), key=f"temp_{name}")
                    if new_temp != d.get("temp"):
                        st.session_state.devices[name]["temp"] = new_temp
                        log_action(f"{name} set to {new_temp}°C", name)

                elif d["type"] == "light" and d["on"]:
                    new_bri = st.slider("Brightness", 10, 100, d.get("brightness", 100), key=f"bri_{name}")
                    if new_bri != d.get("brightness"):
                        st.session_state.devices[name]["brightness"] = new_bri
                        log_action(f"{name} brightness → {new_bri}%", name)

                elif d["type"] == "fan" and d["on"]:
                    new_speed = st.slider("Speed", 1, 3, d.get("speed", 1), key=f"spd_{name}")
                    if new_speed != d.get("speed"):
                        st.session_state.devices[name]["speed"] = new_speed
                        log_action(f"{name} speed → {new_speed}/3", name)

# ── TAB 3 : ROUTINES ─────────────────────────────────────────────────────────
with tab3:
    st.markdown('<div class="section-title">Automation Routines</div>', unsafe_allow_html=True)

    # Existing routines
    st.markdown("### 📌 Saved Routines")
    for i, r in enumerate(st.session_state.routines):
        actions_str = " → ".join(r["actions"][:2]) + ("..." if len(r["actions"]) > 2 else "")
        status_color = "#10b981" if r["active"] else "#4b5563"
        status_text  = "Active" if r["active"] else "Inactive"
        st.markdown(f"""
        <div class="routine-card">
            <div class="routine-name">⚡ {r['name']}</div>
            <div class="routine-detail">🕒 {r['trigger']}</div>
            <div class="routine-detail">Actions: {actions_str}</div>
            <div class="routine-detail" style="color:{status_color}; margin-top:6px;">● {status_text}</div>
        </div>
        """, unsafe_allow_html=True)

        rcol1, rcol2, rcol3 = st.columns([1, 1, 3])
        with rcol1:
            if st.button("▶ Run", key=f"run_r_{i}", use_container_width=True):
                log_action(f"Routine '{r['name']}' executed manually", "System", "routine")
                # Simulate running actions
                for act in r["actions"]:
                    log_action(f"[{r['name']}] {act}", "Routine", "routine")
                st.success(f"✅ Routine '{r['name']}' executed!")
        with rcol2:
            toggle_label = "Disable" if r["active"] else "Enable"
            if st.button(toggle_label, key=f"tog_r_{i}", use_container_width=True):
                st.session_state.routines[i]["active"] = not r["active"]
                st.rerun()

    # Create new routine
    st.markdown("---")
    st.markdown("### ➕ Create New Routine")

    with st.expander("Build a new automation routine"):
        r_name    = st.text_input("Routine Name", placeholder="e.g. Weekend Morning")
        r_trigger = st.text_input("Trigger", placeholder="e.g. Saturday 08:00 AM")
        r_actions = st.text_area("Actions (one per line)", placeholder="Turn on Kitchen Light\nSet Thermostat to 22°C\nUnlock Front Door")

        if st.button("💾 Save Routine"):
            if r_name and r_trigger and r_actions:
                actions_list = [a.strip() for a in r_actions.strip().split("\n") if a.strip()]
                st.session_state.routines.append({
                    "name": r_name, "trigger": r_trigger,
                    "actions": actions_list, "active": True
                })
                log_action(f"New routine created: '{r_name}'", "System", "routine")
                st.success(f"✅ Routine '{r_name}' saved!")
                st.rerun()
            else:
                st.warning("Please fill in all fields.")

# ── TAB 4 : ACTION LOG ────────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-title">Action Log</div>', unsafe_allow_html=True)

    type_colors = {
        "device":  "#3b82f6",
        "voice":   "#8b5cf6",
        "routine": "#f59e0b",
        "scene":   "#ec4899",
        "system":  "#6b7280",
    }

    if not st.session_state.action_log:
        st.info("No actions logged yet.")
    else:
        for entry in st.session_state.action_log:
            color = type_colors.get(entry.get("type", "device"), "#3b82f6")
            badge = entry.get("type", "device").upper()
            st.markdown(f"""
            <div class="log-entry" style="border-left-color:{color}">
                <span class="log-time">{entry['time']}</span>
                &nbsp;·&nbsp;
                <span style="color:{color}; font-size:0.7rem; text-transform:uppercase; letter-spacing:1px;">[{badge}]</span>
                &nbsp;
                <span class="log-action">{entry['action']}</span>
            </div>
            """, unsafe_allow_html=True)

    # Export log
    if st.session_state.action_log:
        log_text = "\n".join(
            f"[{e['time']}] [{e.get('type','').upper()}] {e['action']}"
            for e in st.session_state.action_log
        )
        st.download_button(
            "⬇️ Export Log as .txt",
            data=log_text,
            file_name=f"smarthome_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain"
        )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; padding:40px 0 20px; color:#1e293b; font-family:'Space Mono', monospace; font-size:0.7rem;">
    SMARTHOME AI · POWERED BY CLAUDE · PROJECT 20
</div>
""", unsafe_allow_html=True)