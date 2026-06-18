from app.services.state import(
    update_affection,
    get_affection
)

def apply_affection_rules(message: str):
    if "うれしい" in message:
        update_affection(3)
    elif "好き" in message:
        update_affection(5)
    elif "嫌い" in message:
        update_affection(-5)   
