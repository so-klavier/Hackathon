from fastapi import APIRouter
from app.models.schema import(Chatrequest,Chatresponse)
from app.services.ollama import(generate_response)
from app.services.state import(get_affection)
from app.services.delta_affection import(apply_affection_rules)

router = APIRouter()

@router.post("/chat",response_model=Chatresponse)
async def chat(request: Chatrequest):
    apply_affection_rules(request.message, "user")
    print(f"Current affection: {get_affection(user_id='user000', heroine_id='heroine01')}")
    print(request.message)
    response = await generate_response(request.message)
    apply_affection_rules(response, "ai")
    return Chatresponse(response=response)
