#!/usr/bin/env python3
"""
测试认证相关功能
"""

import sys
from fastapi.testclient import TestClient
from main import app
from app.utils.auth import get_password_hash, verify_password

client = TestClient(app)


def test_password_hash():
    """测试密码哈希和验证功能"""
    # 测试密码哈希
    password = "testpassword"
    hashed = get_password_hash(password)
    print(f"原始密码: {password}")
    print(f"哈希密码: {hashed}")
    print(f"哈希长度: {len(hashed)}")

    # 测试密码验证
    is_valid = verify_password(password, hashed)
    print(f"密码验证结果: {is_valid}")
    assert is_valid

    # 测试错误密码验证
    wrong_password = "wrongpassword"
    is_valid_wrong = verify_password(wrong_password, hashed)
    print(f"错误密码验证结果: {is_valid_wrong}")
    assert not is_valid_wrong

    return True


def test_login():
    """测试登录功能"""
    # 测试使用表单数据登录
    login_data_form = {"username": "testuser", "password": "testpassword"}

    login_response_form = client.post("/api/auth/login", data=login_data_form)
    print(f"表单登录响应状态码: {login_response_form.status_code}")
    print(f"表单登录响应内容: {login_response_form.json()}")
    # 这里不做断言，只是查看响应

    # 测试使用JSON数据登录
    login_data_json = {"username": "testuser", "password": "testpassword"}

    login_response_json = client.post("/api/auth/login", json=login_data_json)
    print(f"JSON登录响应状态码: {login_response_json.status_code}")
    print(f"JSON登录响应内容: {login_response_json.json()}")
    # 这里预期会失败，因为OAuth2PasswordRequestForm要求表单数据

    return True


if __name__ == "__main__":
    try:
        print("测试密码哈希和验证功能...")
        success1 = test_password_hash()
        print("\n测试登录功能...")
        success2 = test_login()

        if success1 and success2:
            print("\n测试成功!")
            sys.exit(0)
        else:
            print("\n测试失败!")
            sys.exit(1)
    except Exception as e:
        print(f"\n测试过程中出现错误: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
