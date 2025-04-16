import logging

from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import engine  # 只导入 engine
from app.models.base import Base  # 从 models.base 导入 Base
from app.schemas.user import UserCreate
from app.services import user_service

logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    """
    初始化数据库
    """
    # 创建表
    Base.metadata.create_all(bind=engine)
    
    # 创建超级用户
    user = user_service.get_user_by_email(db, email="admin@silentrhythm.com")
    if not user:
        user_in = UserCreate(
            email="admin@silentrhythm.com",
            username="admin",
            password="admin",
            is_superuser=True,
        )
        user = user_service.create_user(db, obj_in=user_in)
        logger.info("超级用户已创建")
    else:
        logger.info("超级用户已存在") 