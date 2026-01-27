from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.utils.database import Base

# 使用内存数据库进行测试
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 创建测试数据库表
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# 初始化测试数据库
def init_test_db():
    Base.metadata.create_all(bind=engine)


# 清理测试数据库
def clear_test_db():
    Base.metadata.drop_all(bind=engine)
