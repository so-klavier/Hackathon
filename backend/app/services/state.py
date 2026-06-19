import json
from pathlib import Path

RELATIONSHIP_DATA_PATH = Path(__file__).resolve().parents[3] / "backend" / "data" / "relationships"

def get_relationship_data(user_id:str, heroine_id:str) -> dict:
    file_path = RELATIONSHIP_DATA_PATH / f"{user_id}_{heroine_id}.json"
    with open(file_path, "r", encoding="utf-8") as f:
        relationship_data = json.load(f)
    return relationship_data

def get_affection(user_id:str, heroine_id:str):
    relationship_data = get_relationship_data(user_id, heroine_id)
    return relationship_data["relationship"]["affection"]


def get_relationship(user_id:str, heroine_id:str) -> str:
    affection = get_affection(user_id, heroine_id)
    if affection < 0:
        return "ユーザーを嫌っている"
    elif affection < 20:
        return "まだ警戒している"
    elif affection < 50:
        return "友達として接している"
    elif affection < 80:
        return "好意を持っている"
    return "かなり好意を持っている"

def save_relationship_data(user_id:str, heroine_id:str, relationship_data: dict):
    file_path = RELATIONSHIP_DATA_PATH / f"{user_id}_{heroine_id}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(relationship_data, f, ensure_ascii=False, indent=4)

def update_affection(user_id:str, heroine_id:str, delta: int):
    relationship = get_relationship_data(user_id, heroine_id)
    relationship["relationship"]["affection"] += delta
    save_relationship_data(user_id, heroine_id, relationship)
