from app.models.base import Base
from sqlalchemy import Column, INTEGER, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


class Article(Base):
    __tablename__ = "articles"  # 添加表名

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)  # 添加创建时间
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    author_id = Column(INTEGER, ForeignKey("user.id"))  # 修正外键约束

    # 关联用户模型
    author = relationship("User", back_populates="articles")

