from fastapi import APIRouter, WebSocket, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import json

from app.utils.deps import get_current_user, get_db
from app.services.chat_service import ChatService
from app.models.user import User

router = APIRouter()
chat_service = ChatService()

@router.websocket("/ws/{user_id}")
async def chat_websocket(
    websocket: WebSocket,
    user_id: int,
    db: Session = Depends(get_db)
):
    await chat_service.manager.connect(user_id, websocket)
    # 通过 chat_service.manager.connect 方法将 WebSocket 连接与用户 ID 关联起来
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            # 将 JSON 格式的字符串加载（解析）为 Python 对象。
            # loads 是 "load string" 的缩写
            
            # 保存消息到数据库
            chat_service.save_message(
                db,
                sender_id=user_id,
                receiver_id=message_data["receiver_id"],
                content=message_data["content"]
            )
            
            # 发送消息给接收者
            await chat_service.manager.send_personal_message(
                message_data["content"],
                message_data["receiver_id"]
            )
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        chat_service.manager.disconnect(user_id)

@router.get("/messages", response_model=List[dict])
async def get_messages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """获取用户的所有消息"""
    messages = chat_service.get_user_messages(db, current_user.id)
    return messages