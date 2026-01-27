from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app.utils.database import get_db
from app.utils.auth import get_current_active_user
from app.utils.redis import RedisCache, CacheKeys
from app.models.user import User
from app.models.comment import Comment
from app.models.post import Post
from app.schemas.comment import Comment as CommentSchema, CommentCreate, CommentUpdate

router = APIRouter()


@router.post("/", response_model=CommentSchema)
def create_comment(
    comment: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)
):
    """创建新评论"""
    # 检查文章是否存在
    post = db.query(Post).filter(Post.id == comment.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # 创建评论
    db_comment = Comment(content=comment.content, author_id=current_user.id, post_id=comment.post_id)

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)

    # 清除相关缓存
    # 清除该文章的评论缓存
    RedisCache.delete_pattern(f"comments:{db_comment.post_id}:*")

    return db_comment


@router.get("/post/{post_id}", response_model=List[CommentSchema])
def get_comments_by_post(
    post_id: int, skip: int = Query(0, ge=0), limit: int = Query(50, ge=1, le=100), db: Session = Depends(get_db)
):
    """获取指定文章的评论"""
    # 检查文章是否存在
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    # 生成缓存键
    cache_key = CacheKeys.comments(post_id, skip, limit)

    # 尝试从缓存获取
    cached_comments = RedisCache.get(cache_key)
    if cached_comments:
        return cached_comments

    # 缓存未命中，从数据库查询
    comments = (
        db.query(Comment)
        .filter(Comment.post_id == post_id, Comment.is_active == True)
        .order_by(Comment.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

    # 将结果转换为可序列化的格式
    comments_data = []
    for comment in comments:
        comment_dict = {
            "id": comment.id,
            "content": comment.content,
            "author_id": comment.author_id,
            "post_id": comment.post_id,
            "created_at": comment.created_at.isoformat() if comment.created_at else None,
            "updated_at": comment.updated_at.isoformat() if comment.updated_at else None,
            "is_active": comment.is_active,
            "author": {
                "id": comment.author.id,
                "username": comment.author.username,
                "email": comment.author.email,
                "full_name": comment.author.full_name,
                "is_active": comment.author.is_active,
                "is_admin": comment.author.is_admin,
                "created_at": comment.author.created_at.isoformat() if comment.author.created_at else None,
                "updated_at": comment.author.updated_at.isoformat() if comment.author.updated_at else None,
            },
        }
        comments_data.append(comment_dict)

    # 存入缓存
    RedisCache.set(cache_key, comments_data, expire=300)  # 5分钟过期

    return comments


@router.put("/{comment_id}", response_model=CommentSchema)
def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """更新评论"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    # 检查权限：只有作者可以更新
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    # 更新评论
    comment.content = comment_update.content
    db.commit()
    db.refresh(comment)

    # 清除相关缓存
    # 清除该文章的评论缓存
    RedisCache.delete_pattern(f"comments:{comment.post_id}:*")

    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_active_user)
):
    """删除评论"""
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")

    # 检查权限：只有作者可以删除
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")

    # 软删除：将is_active设为False
    comment.is_active = False
    db.commit()

    # 清除相关缓存
    # 清除该文章的评论缓存
    RedisCache.delete_pattern(f"comments:{comment.post_id}:*")

    return None
