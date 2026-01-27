from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from datetime import datetime
from app.utils.database import get_db
from app.utils.auth import get_current_active_user, get_current_admin_user
from app.utils.redis import RedisCache, CacheKeys
from app.models.user import User
from app.models.post import Post
from app.models.tag import Tag
from app.schemas.post import Post as PostSchema, PostCreate, PostUpdate

router = APIRouter()


@router.post("/", response_model=PostSchema)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """创建新文章"""
    # 创建文章
    db_post = Post(
        title=post.title,
        content=post.content,
        summary=post.summary,
        author_id=current_user.id,
        is_published=post.is_published,
    )

    # 添加标签
    if post.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(post.tag_ids)).all()
        db_post.tags = tags

    # 如果发布，设置发布时间
    if post.is_published:
        db_post.published_at = datetime.utcnow()

    db.add(db_post)
    db.commit()
    db.refresh(db_post)

    # 清除相关缓存
    if post.is_published:
        # 清除文章列表缓存
        RedisCache.delete_pattern("post:list:*")

    return db_post


@router.get("/", response_model=List[PostSchema])
def get_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    tag_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """获取文章列表"""
    # 生成缓存键
    cache_key = CacheKeys.post_list(skip, limit, tag_id, search)

    # 尝试从缓存获取
    cached_posts = RedisCache.get(cache_key)
    if cached_posts:
        return cached_posts

    # 缓存未命中，从数据库查询
    query = db.query(Post).filter(Post.is_published == True)

    # 按标签筛选
    if tag_id:
        query = query.join(Post.tags).filter(Tag.id == tag_id)

    # 搜索
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(Post.title.ilike(search_term), Post.content.ilike(search_term), Post.summary.ilike(search_term))
        )

    # 排序并分页
    posts = query.order_by(Post.created_at.desc()).offset(skip).limit(limit).all()

    # 将结果转换为可序列化的格式
    posts_data = []
    for post in posts:
        post_dict = {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "summary": post.summary,
            "author_id": post.author_id,
            "created_at": post.created_at.isoformat() if post.created_at else None,
            "updated_at": post.updated_at.isoformat() if post.updated_at else None,
            "published_at": post.published_at.isoformat() if post.published_at else None,
            "is_published": post.is_published,
            "author": {
                "id": post.author.id,
                "username": post.author.username,
                "email": post.author.email,
                "full_name": post.author.full_name,
                "is_active": post.author.is_active,
                "is_admin": post.author.is_admin,
                "created_at": post.author.created_at.isoformat() if post.author.created_at else None,
                "updated_at": post.author.updated_at.isoformat() if post.author.updated_at else None,
            },
            "tags": [
                {
                    "id": tag.id,
                    "name": tag.name,
                    "description": tag.description,
                    "created_at": tag.created_at.isoformat() if tag.created_at else None,
                }
                for tag in post.tags
            ],
        }
        posts_data.append(post_dict)

    # 存入缓存
    RedisCache.set(cache_key, posts_data, expire=300)  # 5分钟过期

    return posts


@router.get("/me", response_model=List[PostSchema])
def get_my_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取当前用户的文章列表"""
    posts = (
        db.query(Post)
        .filter(Post.author_id == current_user.id)
        .order_by(Post.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return posts


@router.get("/{post_id}", response_model=PostSchema)
def get_post(
    post_id: int, db: Session = Depends(get_db), current_user: Optional[User] = Depends(get_current_active_user)
):
    """获取指定文章"""
    # 生成缓存键
    cache_key = CacheKeys.post_detail(post_id)

    # 尝试从缓存获取
    cached_post = RedisCache.get(cache_key)
    if cached_post:
        return cached_post

    # 缓存未命中，从数据库查询
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # 检查权限：如果文章未发布，只有作者可以查看
    if not post.is_published and post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    # 将结果转换为可序列化的格式
    post_data = {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "summary": post.summary,
        "author_id": post.author_id,
        "created_at": post.created_at.isoformat() if post.created_at else None,
        "updated_at": post.updated_at.isoformat() if post.updated_at else None,
        "published_at": post.published_at.isoformat() if post.published_at else None,
        "is_published": post.is_published,
        "author": {
            "id": post.author.id,
            "username": post.author.username,
            "email": post.author.email,
            "full_name": post.author.full_name,
            "is_active": post.author.is_active,
            "is_admin": post.author.is_admin,
            "created_at": post.author.created_at.isoformat() if post.author.created_at else None,
            "updated_at": post.author.updated_at.isoformat() if post.author.updated_at else None,
        },
        "tags": [
            {
                "id": tag.id,
                "name": tag.name,
                "description": tag.description,
                "created_at": tag.created_at.isoformat() if tag.created_at else None,
            }
            for tag in post.tags
        ],
    }

    # 存入缓存
    RedisCache.set(cache_key, post_data, expire=600)  # 10分钟过期

    return post


@router.put("/{post_id}", response_model=PostSchema)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """更新文章"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # 检查权限：只有作者或管理员可以更新
    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    # 更新文章信息
    if post_update.title is not None:
        post.title = post_update.title
    if post_update.content is not None:
        post.content = post_update.content
    if post_update.summary is not None:
        post.summary = post_update.summary
    if post_update.is_published is not None:
        post.is_published = post_update.is_published
        # 如果从未发布过，现在发布，设置发布时间
        if post.is_published and not post.published_at:
            post.published_at = datetime.utcnow()

    # 更新标签
    if post_update.tag_ids is not None:
        tags = db.query(Tag).filter(Tag.id.in_(post_update.tag_ids)).all()
        post.tags = tags

    db.commit()
    db.refresh(post)

    # 清除相关缓存
    # 清除文章详情缓存
    RedisCache.delete(CacheKeys.post_detail(post_id))
    # 清除文章列表缓存
    RedisCache.delete_pattern("post:list:*")

    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)):
    """删除文章"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # 检查权限：只有作者或管理员可以删除
    if post.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    db.delete(post)
    db.commit()

    # 清除相关缓存
    # 清除文章详情缓存
    RedisCache.delete(CacheKeys.post_detail(post_id))
    # 清除文章列表缓存
    RedisCache.delete_pattern("post:list:*")

    return None
