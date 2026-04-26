import json
import os
from groq import Groq
from dotenv import load_dotenv
import speech_recognition as sr
from io import BytesIO
import state

# Load .env from the parent directory
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path=env_path)
groq_api_key = os.getenv("GROQ_API_KEY") or os.getenv("Groq_API_Key")

def apply_ai_commands(commands: list):
    for cmd in commands:
        action = cmd.get("action", "").lower()
        target = cmd.get("target", "")
        value  = cmd.get("value", None)

        matched = [n for n in state.devices if target.lower() in n.lower()]

        if action == "turn_on":
            for name in matched:
                state.devices[name]["on"] = True
                state.log_action(f"{name} turned ON via voice command", name)
            if not matched and "all light" in target.lower():
                for name, d in state.devices.items():
                    if d["type"] == "light":
                        d["on"] = True
                        state.log_action(f"{name} turned ON via voice command", name)

        elif action == "turn_off":
            for name in matched:
                state.devices[name]["on"] = False
                state.log_action(f"{name} turned OFF via voice command", name)
            if not matched and "all light" in target.lower():
                for name, d in state.devices.items():
                    if d["type"] == "light":
                        d["on"] = False
                        state.log_action(f"{name} turned OFF via voice command", name)

        elif action == "set_temp" and value:
            for name in matched:
                if state.devices[name]["type"] in ("thermostat", "ac"):
                    state.devices[name]["temp"] = int(value)
                    state.devices[name]["on"] = True
                    state.log_action(f"{name} set to {value}°C via voice command", name)

        elif action == "set_brightness" and value:
            for name in matched:
                if state.devices[name]["type"] == "light":
                    state.devices[name]["brightness"] = int(value)
                    state.devices[name]["on"] = True
                    state.log_action(f"{name} brightness set to {value}% via voice command", name)

        elif action == "lock":
            for name in matched:
                if state.devices[name]["type"] == "lock":
                    state.devices[name]["locked"] = True
                    state.devices[name]["on"] = True
                    state.log_action(f"{name} locked via voice command", name)

        elif action == "unlock":
            for name in matched:
                if state.devices[name]["type"] == "lock":
                    state.devices[name]["locked"] = False
                    state.log_action(f"{name} unlocked via voice command", name)


def process_command(command: str) -> str:
    """Send command to Groq and apply results."""
    home_state_str = state.get_home_state_string()

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
{home_state_str}

User command: "{command}"

Execute the appropriate actions and respond in JSON format."""

    try:
        client = Groq(api_key=groq_api_key)
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            max_tokens=600,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        raw = response.choices[0].message.content.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        result = json.loads(raw)
        ai_msg = result.get("message", "Done!")
        commands = result.get("commands", [])
        apply_ai_commands(commands)
        state.log_action(f'Command: "{command}"', "AI Agent", "voice")
        return ai_msg
    except Exception as e:
        return f"Error communicating with AI: {str(e)}"

def transcribe_audio(audio_bytes: bytes) -> str:
    """Transcribe audio bytes to text using Groq's Whisper model."""
    try:
        client = Groq(api_key=groq_api_key)
        transcription = client.audio.transcriptions.create(
            file=("command.webm", audio_bytes),
            model="whisper-large-v3"
        )
        return transcription.text
    except Exception as e:
        return f"Error processing audio: {str(e)}"
