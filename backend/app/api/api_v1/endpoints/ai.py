from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_service import AIAssistant

router = APIRouter()
ai_assistant = AIAssistant()

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
def chat_with_ai(chat_message: ChatMessage):
    """
    与AI助手对话
    """
    response = ai_assistant.get_response(chat_message.message)
    return ChatResponse(response=response)
