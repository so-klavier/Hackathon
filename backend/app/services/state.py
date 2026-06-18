game_state = {
    "heroine": {
        "affection": 90,
    },
    "flags": {}
}

def get_affection():
    return game_state["heroine"]["affection"]


def get_relationship():
    affection = game_state["heroine"]["affection"]
    if affection < 0:
        return "ユーザーを嫌っている"
    elif affection < 20:
        return "まだ警戒している"
    elif affection < 50:
        return "友達として接している"
    elif affection < 80:
        return "好意を持っている"
    return "かなり好意を持っている"


def update_affection(delta: int):
    game_state["heroine"]["affection"] += delta