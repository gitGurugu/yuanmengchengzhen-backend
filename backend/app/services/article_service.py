from typing import List,Optional
from sqlalchemy.orm import Session
from app.models.article import Article 
from app.schemas.article import ArticleCreate,ArticleUpdate

def get_article(db:Session,id:int)->Optional[Article]:
    return db.query(Article).filter(Article.id==id).first()

def get_articles(db:Session,skip:int=0,limit:int=10)->List[Article]:
    return db.query(Article).offset(skip).limit(limit).all()


def create_article(db:Session,article:ArticleCreate,author_id:int)->Article:
    db_article=Article(**article.dict(),author_id=author_id)#先转成字典然后解包，将参数传入
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article



def update_article(db:Session,article_id:int,article_update:ArticleUpdate)->Optional[Article]:
    db_article=get_article(db,article_id)#在数据库中查询存在的文章
    if db_article:
        for key,value in article_update.dict(exclude_unset=True).items():
            setattr(db_article,key,value)
        db.commit()
        db.refresh(db_article)
    return db_article


def delete_article(db:Session,article_id:int)->bool:
    db_article=get_article(db,article_id)
    if db_article:
        db.delete(db_article)
        db.commit()
        return True
    return False







