from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.user import User, UserCreate, UserUpdate
from app.services import user_service

router = APIRouter()


@router.get("/", response_model=List[User], summary="获取所有用户")
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    获取所有用户
    """
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=User, summary="创建用户")
def create_user(
   
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    这里的 * 位于参数列表的中间，
     它表示一个特殊的语法，用于告诉 Python 解释器，
    * 之后的所有参数都是关键字参数（keyword-only arguments）。
    这意味着调用这个函数时，必须使用参数名来指定这些参数的值，
    而不能使用位置参数。
    """
    """
    创建新用户
    """
    user = user_service.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="该邮箱已被注册",
        )
    user = user_service.create_user(db, obj_in=user_in)
    return user


@router.get("/{user_id}", response_model=User, summary="获取用户详情")
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    根据ID获取用户详情
    """
    user = user_service.get_user(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在",
        )
    return user


@router.put("/{user_id}", response_model=User, summary="更新用户信息")
def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
) -> Any:
    """
    更新用户信息
    """
    user = user_service.get_user(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在",
        )
    user = user_service.update_user(db, db_obj=user, obj_in=user_in)
    return user


@router.delete("/{user_id}", response_model=User, summary="删除用户")
def delete_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
) -> Any:
    """
    删除用户
    """
    user = user_service.get_user(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="用户不存在",
        )
    user = user_service.delete_user(db, id=user_id)
    return user 