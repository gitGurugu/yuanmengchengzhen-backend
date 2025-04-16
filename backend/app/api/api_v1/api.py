from fastapi import APIRouter
from app.api.api_v1.endpoints import health, login, users, ai, article,chat

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"]) 
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(article.router, prefix="/article", tags=["articles"])
# api_router.include_router(gesture.router, prefix="/gesture", tags=["gesture"])
api_router.include_router(chat.router,prefix="/chat",tags=["chat"])




