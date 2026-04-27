import os
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import (
    ToggleRequest, SetDeviceRequest, TextCommandRequest, 
    SceneRequest, AddRoutineRequest, ToggleRoutineRequest, AuthRequest
)
import state
import ai_service
import uvicorn
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from passlib.context import CryptContext

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

MONGODB_URL = os.getenv("MONGODB_URL", "")

app = FastAPI(title="SmartHome AI Backend")

# MongoDB setup
client = MongoClient(MONGODB_URL, serverSelectionTimeoutMS=5000)
db = client["smarthome"]
users_collection = db["users"]

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/state")
def get_state():
    return {
        "devices": state.devices,
        "action_log": state.action_log,
        "routines": state.routines
    }

@app.post("/api/auth/login")
def login(req: AuthRequest):
    try:
        user = users_collection.find_one({"username": req.username})
        if not user or not pwd_context.verify(req.password, user["password"]):
            raise HTTPException(status_code=401, detail="Invalid username or password")
        return {"status": "success", "message": "Login successful"}
    except ServerSelectionTimeoutError:
        raise HTTPException(status_code=500, detail="Could not connect to database")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/auth/signup")
def signup(req: AuthRequest):
    try:
        if users_collection.find_one({"username": req.username}):
            raise HTTPException(status_code=400, detail="Username already exists")
        
        hashed_password = pwd_context.hash(req.password)
        users_collection.insert_one({"username": req.username, "password": hashed_password})
        
        return {"status": "success", "message": "Signup successful. Please login."}
    except ServerSelectionTimeoutError:
        raise HTTPException(status_code=500, detail="Could not connect to database")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/device/toggle")
def toggle_device(req: ToggleRequest):
    if req.device_name not in state.devices:
        raise HTTPException(status_code=404, detail="Device not found")
    
    d = state.devices[req.device_name]
    d["on"] = not d["on"]
    status = "ON" if d["on"] else "OFF"
    state.log_action(f"{req.device_name} turned {status}", req.device_name)
    return {"status": "success", "device": state.devices[req.device_name]}

@app.post("/api/device/set")
def set_device_property(req: SetDeviceRequest):
    if req.device_name not in state.devices:
        raise HTTPException(status_code=404, detail="Device not found")
    
    d = state.devices[req.device_name]
    if req.property in d:
        d[req.property] = req.value
        state.log_action(f"{req.device_name} {req.property} set to {req.value}", req.device_name)
        return {"status": "success", "device": d}
    raise HTTPException(status_code=400, detail="Invalid property")

@app.post("/api/command/text")
def execute_text_command(req: TextCommandRequest):
    response = ai_service.process_command(req.command)
    return {"message": response}

@app.post("/api/command/voice")
async def execute_voice_command(file: UploadFile = File(...)):
    contents = await file.read()
    transcribed_text = ai_service.transcribe_audio(contents)
    
    if "Error" in transcribed_text or "Sorry" in transcribed_text:
        return {"transcription": transcribed_text, "message": transcribed_text}
    
    response = ai_service.process_command(transcribed_text)
    return {"transcription": transcribed_text, "message": response}

@app.post("/api/scene/run")
def run_scene(req: SceneRequest):
    scenes = {
        "🌅 Morning":  [("Kitchen Light", True), ("Living Room Light", True), ("Porch Light", False)],
        "🎬 Movie":    [("Living Room Light", False), ("Smart TV", True), ("Living Room Fan", True)],
        "😴 Sleep":    [("Living Room Light", False), ("Bedroom Light", False), ("Front Door Lock", True)],
        "🏃 Away":     [("Living Room Light", False), ("Kitchen Light", False), ("Security Camera", True)],
    }
    
    if req.scene_name not in scenes:
        raise HTTPException(status_code=404, detail="Scene not found")
        
    actions = scenes[req.scene_name]
    for name, s in actions:
        if name in state.devices:
            state.devices[name]["on"] = s
            state.log_action(f"[{req.scene_name} scene] {name} {'ON' if s else 'OFF'}", name, "scene")
    state.log_action(f"Scene activated: {req.scene_name}", "System", "scene")
    return {"status": "success"}

@app.post("/api/routine/add")
def add_routine(req: AddRoutineRequest):
    state.routines.append({
        "name": req.name,
        "trigger": req.trigger,
        "actions": req.actions,
        "active": True
    })
    state.log_action(f"New routine created: '{req.name}'", "System", "routine")
    return {"status": "success"}

@app.post("/api/routine/toggle")
def toggle_routine(req: ToggleRoutineRequest):
    if 0 <= req.index < len(state.routines):
        state.routines[req.index]["active"] = not state.routines[req.index]["active"]
        return {"status": "success"}
    raise HTTPException(status_code=400, detail="Invalid routine index")

@app.post("/api/system/reset")
def reset_system():
    state.reset_devices()
    return {"status": "success"}

@app.post("/api/system/clear_log")
def clear_log():
    state.clear_log()
    return {"status": "success"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
