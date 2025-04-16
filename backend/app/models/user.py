from sqlalchemy import Boolean, Column, Integer, String

from app.models.base import Base

from sqlalchemy.orm import relationship
class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False) 


    # 关联文章模型
    articles=relationship("Article",back_populates="author")

    # 添加消息关系
    sent_messages = relationship("Message", foreign_keys="[Message.sender_id]", back_populates="sender")
    received_messages = relationship("Message", foreign_keys="[Message.receiver_id]", back_populates="receiver")

