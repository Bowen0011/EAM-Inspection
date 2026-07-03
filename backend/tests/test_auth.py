"""
认证模块单元测试
"""
import pytest
from app.services.auth_service import hash_password, verify_password


class TestAuth:
    """认证 API 测试"""

    def test_login_success(self, client, test_users):
        """测试正确账号密码登录"""
        resp = client.post("/api/v1/auth/login", json={
            "username": "engineer01",
            "password": "test123456"
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["username"] == "engineer01"

    def test_login_wrong_password(self, client, test_users):
        """测试错误密码"""
        resp = client.post("/api/v1/auth/login", json={
            "username": "engineer01",
            "password": "wrong_password"
        })
        assert resp.status_code == 401
        assert "用户名或密码错误" in resp.json()["detail"]

    def test_login_disabled_user(self, client, test_users):
        """测试被禁用的用户登录"""
        resp = client.post("/api/v1/auth/login", json={
            "username": "disabled_user",
            "password": "test123456"
        })
        assert resp.status_code == 403
        assert "账号已被禁用" in resp.json()["detail"]

    def test_change_password_success(self, client, test_users, engineer_token):
        """测试修改密码成功"""
        resp = client.post("/api/v1/auth/change-password", json={
            "old_password": "test123456",
            "new_password": "newpass123456"
        }, headers={"Authorization": f"Bearer {engineer_token}"})
        assert resp.status_code == 200
        assert resp.json()["message"] == "密码修改成功"

    def test_change_password_wrong_old(self, client, test_users, engineer_token):
        """测试旧密码错误"""
        resp = client.post("/api/v1/auth/change-password", json={
            "old_password": "wrong_old",
            "new_password": "newpass123456"
        }, headers={"Authorization": f"Bearer {engineer_token}"})
        assert resp.status_code == 400
        assert "旧密码错误" in resp.json()["detail"]

    def test_hash_password(self):
        """测试密码加密与验证"""
        pw = hash_password("test123456")
        assert verify_password("test123456", pw) is True
        assert verify_password("wrong", pw) is False