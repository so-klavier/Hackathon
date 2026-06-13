from ollama import chat

async def generate_response(message:str)->str:
    response = chat(
        model="qwen3:4b",
        messages=[
            {
            "role": "user",
            "content": message    
            }
        ]
    )
    return response.message.content