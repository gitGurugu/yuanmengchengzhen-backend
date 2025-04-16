from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter()


@router.get("/", summary="健康检查")
def health_check(db: Session = Depends(get_db)):
    """
    健康检查端点
    
    - **检查API是否正常运行**
    - **检查数据库连接是否正常**
    """
    # 尝试执行一个简单的数据库查询来检查数据库连接
    db.execute("SELECT 1")
    return {
        "status": "ok",
        "message": "服务正常运行"
    } 