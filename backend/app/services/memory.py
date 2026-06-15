MAX_HISTORY = 20

conversation_history=[]

def add_user_message(message: str):
    conversation_history.append({
            "role": "user",
            "content": message
        })

def add_assistant_message(message: str):
    conversation_history.append({
            "role": "assistant",
            "content": message
        })
    if len(conversation_history) > MAX_HISTORY:
        del conversation_history[:2]

def get_history():
    return conversation_history