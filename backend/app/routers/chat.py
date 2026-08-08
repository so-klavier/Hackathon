from fastapi import APIRouter
from app.models.schema import(Chatrequest,Chatresponse)
from app.services.ollama import(generate_response)
from app.services.state import(Relationship_Manager)
from app.services.delta_affection import(apply_affection_rules)

router = APIRouter()
manager = Relationship_Manager()



@router.post("/chat",response_model=Chatresponse)
async def chat(request: Chatrequest):
    apply_affection_rules(request.message, "user")
    print(f"Current affection: {manager.get_value('user000', 'heroine02', 'affection', 0)}")
    response = await generate_response(request.message)
    apply_affection_rules(response["message"], "ai")
    return Chatresponse(
        response=response["message"],
        event=response["event"]
    )
