import logging
import traceback
from fastapi import Request, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

async def global_exception_handler(request: Request, exc: Exception):
    """全局异常处理器"""
    # 记录异常信息
    logger.error(f"Unhandled exception: {exc}")
    logger.error(traceback.format_exc())
    
    # 根据异常类型返回不同的响应
    if isinstance(exc, SQLAlchemyError):
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Database error occurred"}
        )
    
    # 默认返回500错误
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

class CustomException(Exception):
    """自定义异常类"""
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

async def custom_exception_handler(request: Request, exc: CustomException):
    """自定义异常处理器"""
    logger.error(f"Custom exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
