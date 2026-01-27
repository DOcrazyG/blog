from fastapi.testclient import TestClient
from app.main import app

# 创建测试客户端
client = TestClient(app)

# 获取访问令牌
def get_access_token():
    response = client.post(
        "/api/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    return response.json()["access_token"]

# 测试获取标签列表
def test_get_tags():
    response = client.get("/api/tags/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
