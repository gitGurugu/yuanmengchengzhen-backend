from typing import List, Dict
from fastapi import WebSocket
from sqlalchemy.orm import Session
from app.models.message import Message
from app.models.user import User
from datetime import datetime

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}
    # 初始化 active_connections 字典，用于存储活跃的 WebSocket 连接
    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket
    # 当用户建立 WebSocket 连接时调用。它接受用户 ID 和 WebSocket 对象，并将它们存储在 active_connections 字典中
    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
    # 当用户断开 WebSocket 连接时调用。它从 active_connections 字典中删除用户的连接。
    async def send_personal_message(self, message: str, recipient_id: int):
        if recipient_id in self.active_connections:
            await self.active_connections[recipient_id].send_json({
                "type": "message",
                "data": message
            })
    # 向特定用户发送消息。它检查用户是否在线（即是否有活跃的 WebSocket 连接），如果有，则发送消息。
    async def broadcast(self, message: str, exclude_user_id: int = None):
        for user_id, connection in self.active_connections.items():
            if user_id != exclude_user_id:
                await connection.send_json({
                    "type": "message",
                    "data": message
                })
                # 向所有在线用户广播消息，除非指定了 exclude_user_id

class ChatService:
    def __init__(self):
        self.manager = ConnectionManager()
    
    def save_message(self, db: Session, sender_id: int, receiver_id: int, content: str) -> Message:
        message = Message(
            content=content,
            sender_id=sender_id,
            receiver_id=receiver_id
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    
    def get_user_messages(self, db: Session, user_id: int) -> List[Message]:
        return db.query(Message).filter(
            (Message.sender_id == user_id) | (Message.receiver_id == user_id)
        ).order_by(Message.created_at.desc()).all()