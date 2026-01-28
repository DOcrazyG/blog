from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
from app.utils.database import get_db
from app.models.user import User

# 加载环境变量
load_dotenv()

# 获取配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# 密码加密上下文
pwd_hash = PasswordHash.recommended()

# OAuth2密码承载令牌
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# 可选的令牌提取依赖
def get_token_optional(request: Request) -> Optional[str]:
    """从请求头中提取令牌（可选）"""
    authorization: str = request.headers.get("Authorization")
    if not authorization:
        return None
    scheme, _, param = authorization.partition(" ")
    if scheme.lower() != "bearer":
        return None
    return param


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_hash.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """获取密码哈希值"""
    return pwd_hash.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """获取当前活跃用户"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    """获取当前管理员用户"""
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user


def get_current_user_optional(
    token: Optional[str] = Depends(get_token_optional), db: Session = Depends(get_db)
) -> Optional[User]:
    """获取当前用户（可选）"""
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            return None
        if not user.is_active:
            return None
        return user
    except JWTError:
        return None
