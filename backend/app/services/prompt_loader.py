from pathlib import Path
import json

ROOT_DIR = Path(__file__).resolve().parents[3]

def load_system_prompt() -> str:
    path = ROOT_DIR/"prompts"/"system"/"system_prompt.txt"
    return path.read_text(encoding="utf-8")


def load_heroine() -> dict:
    path = ROOT_DIR/"backend"/"data"/"characters"/"heroine01.json"
    with open(path, encoding="utf-8")as f:
        return json.load(f)
    
def load_user(user_id: str) -> dict:
    path = ROOT_DIR/"backend"/"data"/"users"/f"{user_id}.json"
    with open(path, encoding="utf-8")as f:
        return json.load(f)