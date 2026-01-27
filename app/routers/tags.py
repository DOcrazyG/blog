from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.utils.database import get_db
from app.utils.auth import get_current_active_user, get_current_admin_user
from app.utils.redis import RedisCache, CacheKeys
from app.models.user import User
from app.models.tag import Tag
from app.schemas.tag import Tag as TagSchema, TagCreate, TagUpdate

router = APIRouter()


@router.post("/", response_model=TagSchema)
def create_tag(tag: TagCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """创建新标签"""
    # 检查标签名是否已存在
    existing_tag = db.query(Tag).filter(Tag.name == tag.name).first()
    if existing_tag:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag name already exists")

    # 创建标签
    db_tag = Tag(name=tag.name, description=tag.description)

    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)

    # 清除标签列表缓存
    RedisCache.delete(CacheKeys.tag_list())

    return db_tag


@router.get("/", response_model=List[TagSchema])
def get_tags(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=100), db: Session = Depends(get_db)):
    """获取标签列表"""
    # 生成缓存键
    cache_key = CacheKeys.tag_list()

    # 尝试从缓存获取
    cached_tags = RedisCache.get(cache_key)
    if cached_tags:
        return cached_tags

    # 缓存未命中，从数据库查询
    tags = db.query(Tag).offset(skip).limit(limit).all()

    # 将结果转换为可序列化的格式
    tags_data = []
    for tag in tags:
        tag_dict = {
            "id": tag.id,
            "name": tag.name,
            "description": tag.description,
            "created_at": tag.created_at.isoformat() if tag.created_at else None,
        }
        tags_data.append(tag_dict)

    # 存入缓存
    RedisCache.set(cache_key, tags_data, expire=3600)  # 1小时过期

    return tags


@router.get("/{tag_id}", response_model=TagSchema)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    """获取指定标签详情"""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")
    return tag


@router.put("/{tag_id}", response_model=TagSchema)
def update_tag(
    tag_id: int,
    tag_update: TagUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin_user),
):
    """更新标签"""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")

    # 检查新标签名是否已被其他标签使用
    if tag_update.name and tag_update.name != tag.name:
        existing_tag = db.query(Tag).filter(Tag.name == tag_update.name).first()
        if existing_tag:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag name already exists")
        tag.name = tag_update.name

    if tag_update.description is not None:
        tag.description = tag_update.description

    db.commit()
    db.refresh(tag)

    # 清除标签列表缓存
    RedisCache.delete(CacheKeys.tag_list())
    # 清除文章列表缓存（因为标签变化可能影响文章列表）
    RedisCache.delete_pattern("post:list:*")

    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(tag_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_admin_user)):
    """删除标签"""
    tag = db.query(Tag).filter(Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")

    db.delete(tag)
    db.commit()

    # 清除标签列表缓存
    RedisCache.delete(CacheKeys.tag_list())
    # 清除文章列表缓存（因为标签变化可能影响文章列表）
    RedisCache.delete_pattern("post:list:*")

    return None
