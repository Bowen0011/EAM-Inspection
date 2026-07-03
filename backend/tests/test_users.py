"""
用户管理模块单元测试
"""
import pytest


class TestUsers:
    """用户管理 API 测试"""

    def test_health_check(self, client):
        """健康检查接口"""
        resp = client.get("/api/v1/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    def test_list_users_no_permission(self, client, test_users, tech_headers):
        """技术员无权查看用户列表"""
        resp = client.get("/api/v1/users/list", headers=tech_headers)
        assert resp.status_code == 403

    def test_reset_password_no_permission(self, client, test_users, tech_headers):
        """技术员无权重置密码"""
        user = test_users["tech01"]
        resp = client.post(f"/api/v1/users/{user.id}/reset-password", headers=tech_headers)
        assert resp.status_code == 403

    def test_toggle_status_no_permission(self, client, test_users, tech_headers):
        """技术员无权开关用户"""
        user = test_users["tech01"]
        resp = client.put(f"/api/v1/users/{user.id}/toggle-status", json={
            "is_active": False
        }, headers=tech_headers)
        assert resp.status_code == 403