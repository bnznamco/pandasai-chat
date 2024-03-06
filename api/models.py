from pydantic import BaseModel

class OpenaiToken(BaseModel):
    token: str
    
class ChatMessage(BaseModel):
    message: str
