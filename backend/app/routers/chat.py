from fastapi import APIRouter
from app.models.schema import(Chatrequest,Chatresponse)
from app.services.ollama import(generate_response)
from app.services.state import(get_affection)
from app.services.delta_affection import(apply_affection_rules)

router = APIRouter()

@router.post("/chat",response_model=Chatresponse)
async def chat(request: Chatrequest):
    apply_affection_rules(request.message)
    print(f"Current affection: {get_affection()}")
    print(request.message)
    response = await generate_response(request.message)
    return Chatresponse(response=response)
