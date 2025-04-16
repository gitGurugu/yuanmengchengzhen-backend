from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.utils.deps import get_current_user, get_db
from app.schemas.article import Article, ArticleCreate, ArticleUpdate
from app.services import article_service

router = APIRouter()

@router.get("/", response_model=List[Article])
def read_articles(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10
):
    """
    获取所有文章列表
    """
    articles = article_service.get_articles(db, skip=skip, limit=limit)
    return articles

@router.post("/", response_model=Article)
def create_article(
    article: ArticleCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    创建新文章
    """
    return article_service.create_article(
        db=db, article=article, author_id=current_user.id
    )

@router.get("/{article_id}", response_model=Article)
def read_article(article_id: int, db: Session = Depends(get_db)):
    """
    获取特定文章
    """
    article = article_service.get_article(db, article_id=article_id)
    if article is None:
        raise HTTPException(status_code=404, detail="文章未找到")
    return article

@router.put("/{article_id}", response_model=Article)
def update_article(
    article_id: int,
    article_update: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    更新文章
    """
    db_article = article_service.get_article(db, article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="文章未找到")
    if db_article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限修改此文章")
    return article_service.update_article(db, article_id, article_update)

@router.delete("/{article_id}")
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    删除文章
    """
    db_article = article_service.get_article(db, article_id)
    if db_article is None:
        raise HTTPException(status_code=404, detail="文章未找到")
    if db_article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="没有权限删除此文章")
    article_service.delete_article(db, article_id)
    return {"message": "文章已删除"}