from pydantic import BaseModel
from typing import List, Optional, Any, Dict

class DeviceState(BaseModel):
    icon: str
    room: str
    type: str
    on: bool
    brightness: Optional[int] = None
    temp: Optional[int] = None
    locked: Optional[bool] = None
    speed: Optional[int] = None
    channel: Optional[int] = None
    recording: Optional[bool] = None
    open: Optional[bool] = None
    schedule: Optional[str] = None

class ActionLogEntry(BaseModel):
    time: str
    action: str
    device: str
    type: str

class Routine(BaseModel):
    name: str
    trigger: str
    actions: List[str]
    active: bool

class ToggleRequest(BaseModel):
    device_name: str

class SetDeviceRequest(BaseModel):
    device_name: str
    property: str  # e.g., "temp", "brightness", "speed"
    value: Any

class TextCommandRequest(BaseModel):
    command: str

class SceneRequest(BaseModel):
    scene_name: str

class AddRoutineRequest(BaseModel):
    name: str
    trigger: str
    actions: List[str]

class ToggleRoutineRequest(BaseModel):
    index: int
