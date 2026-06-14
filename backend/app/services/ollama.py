from ollama import chat
from app.services.prompt_loader import(
    load_system_prompt,
    load_heroine
)

async def generate_response(message: str)->str:
    system_prompt = load_system_prompt()
    heroine = load_heroine()
    character_prompt = f"""
名前: {heroine["name"]}
年齢: {heroine["age"]}
職業: {heroine["occupation"]}
性格: {", ".join(heroine["personality"])}
話し方: {", ".join(heroine["speech_style"])}
好き: {", ".join(heroine["likes"])}
"""
    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "system",
                "content": character_prompt
            },
            {
                "role": "user",
                "content": message
            }
        ]
    )
    return response.message.content