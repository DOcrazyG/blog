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

# 测试创建文章
def test_create_post():
    token = get_access_token()
    response = client.post(
        "/api/posts/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Post",
            "content": "This is a test post",
            "summary": "Test post summary",
            "is_published": True,
            "tag_ids": []
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["content"] == "This is a test post"
    assert data["is_published"] == True

# 测试获取文章列表
def test_get_posts():
    response = client.get("/api/posts/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# 测试获取文章详情
def test_get_post():
    # 先创建一篇文章
    token = get_access_token()
    create_response = client.post(
        "/api/posts/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Test Post for Detail",
            "content": "This is a test post for detail",
            "is_published": True,
            "tag_ids": []
        }
    )
    post_id = create_response.json()["id"]
    
    # 获取文章详情
    response = client.get(f"/api/posts/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == post_id
    assert data["title"] == "Test Post for Detail"
