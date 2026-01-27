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

# 测试创建评论
def test_create_comment():
    token = get_access_token()
    
    # 先创建一篇文章
    create_post_response = client.post(
        "/api/posts/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Post for Comment",
            "content": "This post is for testing comments",
            "is_published": True,
            "tag_ids": []
        }
    )
    post_id = create_post_response.json()["id"]
    
    # 创建评论
    response = client.post(
        "/api/comments/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "content": "This is a test comment",
            "post_id": post_id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "This is a test comment"
    assert data["post_id"] == post_id

# 测试获取文章评论
def test_get_comments_by_post():
    token = get_access_token()
    
    # 先创建一篇文章
    create_post_response = client.post(
        "/api/posts/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Post for Comments List",
            "content": "This post is for testing comments list",
            "is_published": True,
            "tag_ids": []
        }
    )
    post_id = create_post_response.json()["id"]
    
    # 创建评论
    client.post(
        "/api/comments/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "content": "Test comment 1",
            "post_id": post_id
        }
    )
    
    # 获取评论列表
    response = client.get(f"/api/comments/post/{post_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
