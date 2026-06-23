import json
from pathlib import Path
from app.services.state import (get_relationship)

EVENT_DATA_PATH = Path(__file__).resolve().parents[3] / "backend" / "data" / "events"

def load_events():
    events = []
    for file in EVENT_DATA_PATH.glob("*.json"):
        with open(file, "r", encoding="utf-8") as f:
            events.append(json.load(f))
    return events

def check_event_conditions(event, relationship):
    conditions = event["conditions"]
    if relationship["affection"] < conditions["required_affection"]:
        return False
    for flag, expected in conditions["required_flags"].items():
        actual = relationship["flags"].get(flag, False)
        if actual != expected:
            return False
    return True

def get_available_events(user_id:str, heroine_id:str):
    relationship = get_relationship(user_id, heroine_id)
    events = load_events()
    events.sort(key=lambda e: e.get("priority", 0), reverse=True)
    for event in events:
        if check_event_conditions(event, relationship):
            return event
    return None

