from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import ALGORITHM
from app.db.session import SessionLocal
from app.models.user import User
from app.schemas.token import TokenPayload
from app.services import user_service

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_db() -> Generator:
    """
    生成器函数
    获取数据库会话
    """
    try:
        db = SessionLocal()
        yield db
        # 这行代码将数据库会话对象 db 返回给调用者。
        # 当生成器执行到这一行时，它会暂停执行，并将控制权返回给调用者。
        # 调用者可以使用这个会话对象来执行数据库操作。

    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    # 数据库里面的user的model
    """
    获取当前用户
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无法验证凭据",
        )
    # 验证凭证，提取用户唯一标识符
    user = user_service.get_user(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    获取当前活跃用户
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="用户未激活")
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    获取当前活跃的超级用户
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="用户没有足够的权限"
        )
    return current_user 