from pydantic import BaseModel

class Chatrequest(BaseModel):
    message: str

class Chatresponse(BaseModel):
    response: str
    event: str | None
