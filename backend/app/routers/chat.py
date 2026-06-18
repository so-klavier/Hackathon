from fastapi import APIRouter
from app.models.schema import(Chatrequest,Chatresponse)
from app.services.ollama import(generate_response)

router = APIRouter()

@router.post("/chat",response_model=Chatresponse)
async def chat(request: Chatrequest):
    print(request.message)
    response = await generate_response(request.message)
    return Chatresponse(response=response)
