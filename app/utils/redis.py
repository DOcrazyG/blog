import redis
import json
from typing import Optional, Any
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

# Redis配置
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# 创建Redis客户端
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

class RedisCache:
    """Redis缓存类"""
    
    @staticmethod
    def set(key: str, value: Any, expire: int = 3600) -> bool:
        """设置缓存"""
        try:
            if not isinstance(value, (str, int, float, bool)):
                value = json.dumps(value)
            redis_client.setex(key, expire, value)
            return True
        except Exception as e:
            print(f"Redis set error: {e}")
            return False
    
    @staticmethod
    def get(key: str) -> Optional[Any]:
        """获取缓存"""
        try:
            value = redis_client.get(key)
            if value:
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return None
        except Exception as e:
            print(f"Redis get error: {e}")
            return None
    
    @staticmethod
    def delete(key: str) -> bool:
        """删除缓存"""
        try:
            redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False
    
    @staticmethod
    def delete_pattern(pattern: str) -> bool:
        """删除匹配模式的缓存"""
        try:
            keys = redis_client.keys(pattern)
            if keys:
                redis_client.delete(*keys)
            return True
        except Exception as e:
            print(f"Redis delete pattern error: {e}")
            return False

# 缓存键生成器
class CacheKeys:
    """缓存键生成类"""
    
    @staticmethod
    def post_list(skip: int, limit: int, tag_id: Optional[int] = None, search: Optional[str] = None) -> str:
        """文章列表缓存键"""
        return f"post:list:{skip}:{limit}:{tag_id or 'all'}:{search or 'none'}"
    
    @staticmethod
    def post_detail(post_id: int) -> str:
        """文章详情缓存键"""
        return f"post:detail:{post_id}"
    
    @staticmethod
    def tag_list() -> str:
        """标签列表缓存键"""
        return "tag:list"
    
    @staticmethod
    def comments(post_id: int, skip: int, limit: int) -> str:
        """评论列表缓存键"""
        return f"comments:{post_id}:{skip}:{limit}"
