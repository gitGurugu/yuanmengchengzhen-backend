from datetime import datetime
from typing import Optional
from pydantic import BaseModel

# 用于创建文章的基础模型
class ArticleBase(BaseModel):
    title: str
    content: str

# 用于创建文章的请求模型
class ArticleCreate(ArticleBase):
    pass

# 用于更新文章的请求模型
class ArticleUpdate(ArticleBase):
    title: Optional[str] = None
    content: Optional[str] = None

# 用于响应的文章模型
class Article(ArticleBase):
    id: int
    created_at: datetime
    updated_at: datetime
    author_id: int

    class Config:
        orm_mode = True  # 允许从 ORM 模型创建
