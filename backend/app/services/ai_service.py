from openai import OpenAI
from app.core.config import settings
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AIAssistant:
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        logger.debug("OpenAI client initialized")
    
    def get_response(self, message: str) -> str:
        try:
            logger.debug(f"发送消息到 OpenAI: {message}")
            # 正确的 API 调用方式
            completion = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "你是一个手语助手，帮助我来学习手语的相关知识。"
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            logger.debug("收到 OpenAI 响应")
            # 正确获取响应内容
            response_text = completion.choices[0].message.content
            logger.debug(f"AI 响应内容: {response_text}")
            return response_text
            
        except Exception as e:
            logger.error(f"AI 服务错误: {str(e)}", exc_info=True)
            return f"AI助手出现错误: {str(e)}"



