from ollama import chat
from app.services.memory import(
    add_user_message,
    add_assistant_message,
    get_history
)
from app.services.prompt_loader import(
    load_system_prompt,
    load_heroine,
    load_user
)
from app.services.state import(Relationship_Manager)
from app.services.events import(
    get_available_events
)

manager = Relationship_Manager()

#今はuser_idとheroine_idは固定で"user000"と"heroine02"を使用しているが、将来的にはrequestから取得するように変更する予定。
async def generate_response(message: str)->str:

    system_prompt = load_system_prompt()
    heroine = load_heroine("heroine02")
    user = load_user("user000")
    relationship = manager.get_relationship("user000", "heroine02")
    affection = manager.get_value("user000", "heroine02", "affection", 0)
    event = get_available_events("user000", "heroine02")

    character_prompt = f"""
名前: {heroine["name"]}
年齢: {heroine["age"]}
職業: {heroine["occupation"]}
性格: {", ".join(heroine["personality"])}
好きなもの: {", ".join(heroine["likes"])}
話し方: {", ".join(heroine["speech_style"])}
"""
    relationship_prompt = f"""
    "ユーザー": {user["user_data"]["name"]}({user["user_data"]["nickname"]})
    好感度: {affection}
    ユーザーとの現在の関係性: {relationship}

    この好感度とユーザーとの関係性を踏まえた自然な会話をユーザーとしなさい。
    決して数値は会話に含めてはいけない。
    関係性が高いほど親密に、低いほど距離感をもって接すること。

"""
    add_user_message(message)

    messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "system",
                "content": character_prompt
            },
            {
                "role": "system",
                "content": relationship_prompt
            }
        ]
    if event:
        event_prompt = f"""
        現在発生中のイベント: {event["name"]}
        {event["prompt"]}
        通常会話ではなくこのイベントに沿った会話をすること。
        """
        messages.append({
            "role": "system",
            "content": event_prompt
        })
        manager.add_flag("user000", "heroine02", event["event_id"])
    else:
        messages.append({
            "role": "system",
            "content": "現在発生中のイベントはありません。"
        })

    messages.extend(get_history())

    response = chat(
        model="gemma4:e4B",
        messages=messages,
        think=False
    )
    answer = response.message.content
    add_assistant_message(answer)

    return {
        "message": answer,
        "event": event["name"] if event else None
    }