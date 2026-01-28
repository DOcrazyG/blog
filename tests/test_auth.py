from fastapi.testclient import TestClient
from main import app
from app.utils.database import SessionLocal, engine, Base

# 创建测试客户端
client = TestClient(app)

# 测试注册功能
def test_register():
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert data["full_name"] == "Test User"

# 测试登录功能
def test_login():
    response = client.post(
        "/api/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
