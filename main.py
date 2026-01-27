from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, posts, comments, tags
from app.utils.database import engine, Base
from app.utils.error_handler import global_exception_handler, custom_exception_handler, CustomException

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title="Blog API", description="A personal blog backend API built with FastAPI and PostgreSQL", version="0.1.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册异常处理器
app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(CustomException, custom_exception_handler)

# 注册路由
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])
app.include_router(comments.router, prefix="/api/comments", tags=["comments"])
app.include_router(tags.router, prefix="/api/tags", tags=["tags"])


@app.get("/")
def read_root():
    return {"message": "Welcome to Blog API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
