import json
from pathlib import Path
from app.services.state import Relationship_Manager
manager = Relationship_Manager()

EVENT_DATA_PATH = Path(__file__).resolve().parents[3] / "backend" / "data" / "events"

def load_events()->list:
    events = []
    for file in EVENT_DATA_PATH.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            events.append(json.load(f))
    return events

def check_event_conditions(event: dict, user_id: str, heroine_id: str)->bool:
    conditions = event["conditions"]
    affection = manager.get_value(user_id, heroine_id, "affection", 0)
    if affection < conditions["required_affection"]:
        return False
    for flag in event["conditions"]["required_flags"]:
        if not manager.has_flag(user_id, heroine_id, flag):
            return False
    return True

def get_available_events(user_id:str, heroine_id:str)->dict | None:
    events = load_events()
    events.sort(key=lambda e: e.get("priority", 0), reverse=True)
    for event in events:
        if check_event_conditions(event, user_id, heroine_id):
            return event
    return None

