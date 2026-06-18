from ollama import chat
from app.services.memory import(
    add_user_message,
    add_assistant_message,
    get_history
)
from app.services.prompt_loader import(
    load_system_prompt,
    load_heroine
)
from app.services.state import(
    get_relationship,
    get_affection
)


async def generate_response(message: str)->str:
    system_prompt = load_system_prompt()
    heroine = load_heroine()
    relationship = get_relationship()
    affection = get_affection()
    character_prompt = f"""
名前: {heroine["name"]}
年齢: {heroine["age"]}
職業: {heroine["occupation"]}
性格: {", ".join(heroine["personality"])}
話し方: {", ".join(heroine["speech_style"])}
"""
    relationship_prompt = f"""
    好感度: {affection}
    現在の関係性: {relationship}

    この好感度と関係性を踏まえた自然な会話をしなさい。
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
        model="gemma4:12b",
        messages=messages
    )
    answer = response.message.content
    add_assistant_message(answer)

    return answer