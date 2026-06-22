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
from app.services.state import(
    get_relationship,
    get_affection
)

#今はuser_idとheroine_idは固定で"user000"と"heroine01"を使用しているが、将来的にはrequestから取得するように変更する予定。
async def generate_response(message: str)->str:
    system_prompt = load_system_prompt()
    heroine = load_heroine("heroine02")
    user = load_user("user000")
    relationship = get_relationship(user_id="user000", heroine_id="heroine02")
    affection = get_affection(user_id="user000", heroine_id="heroine02")
    character_prompt = f"""
名前: {heroine["name"]}
年齢: {heroine["age"]}
職業: {heroine["occupation"]}
性格: {", ".join(heroine["personality"])}
話し方: {", ".join(heroine["speech_style"])}
"""
    relationship_prompt = f"""
    "ユーザー": {user["name"]}({user["nickname"]})
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

    messages.extend(get_history())

    response = chat(
        model="gemma3:4B",
        messages=messages,
        think=False
    )
    answer = response.message.content
    add_assistant_message(answer)

    return answer