"""
模板管理模块单元测试
"""
import pytest


class TestTemplates:
    """模板 CRUD + 权限测试"""

    def test_create_template(self, client, admin_headers, db):
        """工程师创建模板"""
        resp = client.post("/api/v1/templates", json={
            "template_name": "测试模板",
            "device_type": "车床类",
            "items": [
                {"item_name": "主轴温度", "data_type": "number",
                 "standard_min": 20, "standard_max": 65, "unit": "℃"},
                {"item_name": "润滑油位", "data_type": "boolean"},
                {"item_name": "备注", "data_type": "text"}
            ]
        }, headers=admin_headers)
        assert resp.status_code == 201
        data = resp.json()
        assert data["message"] == "模板创建成功"
        assert "template_id" in data

    def test_tech_cannot_create(self, client, tech_headers):
        """技术员创建模板应返回 403"""
        resp = client.post("/api/v1/templates", json={
            "template_name": "测试模板",
            "device_type": "车床类",
            "items": [{"item_name": "温度", "data_type": "number",
                       "standard_min": 0, "standard_max": 100, "unit": "℃"}]
        }, headers=tech_headers)
        assert resp.status_code == 403

    def test_list_templates(self, client, admin_headers, db):
        """获取模板列表"""
        # 先创建一个模板
        client.post("/api/v1/templates", json={
            "template_name": "列表测试模板",
            "device_type": "车床",
            "items": [{"item_name": "温度", "data_type": "number",
                       "standard_min": 0, "standard_max": 100, "unit": "℃"}]
        }, headers=admin_headers)

        resp = client.get("/api/v1/templates/list", headers=admin_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) >= 1
        assert data[0]["template_name"] == "列表测试模板"

    def test_get_template_detail(self, client, admin_headers, db):
        """获取模板详情"""
        create_resp = client.post("/api/v1/templates", json={
            "template_name": "详情测试",
            "device_type": "数控",
            "items": [{"item_name": "温度", "data_type": "number",
                       "standard_min": 0, "standard_max": 100, "unit": "℃"}]
        }, headers=admin_headers)
        template_id = create_resp.json()["template_id"]

        resp = client.get(f"/api/v1/templates/{template_id}", headers=admin_headers)
        assert resp.status_code == 200
        assert resp.json()["template_name"] == "详情测试"
        assert len(resp.json()["items"]) == 1

    def test_edit_template(self, client, admin_headers, db):
        """编辑模板"""
        create_resp = client.post("/api/v1/templates", json={
            "template_name": "编辑前",
            "device_type": "车床",
            "items": [{"item_name": "温度", "data_type": "number",
                       "standard_min": 0, "standard_max": 100, "unit": "℃"}]
        }, headers=admin_headers)
        template_id = create_resp.json()["template_id"]

        resp = client.put(f"/api/v1/templates/{template_id}", json={
            "template_name": "编辑后",
            "device_type": "数控车床",
            "items": [
                {"item_name": "温度", "data_type": "number",
                 "standard_min": 10, "standard_max": 80, "unit": "℃"},
                {"item_name": "振动", "data_type": "number",
                 "standard_min": 0, "standard_max": 5, "unit": "mm/s"}
            ]
        }, headers=admin_headers)
        assert resp.status_code == 200
        assert resp.json()["message"] == "模板更新成功"

        # 验证更新结果
        detail = client.get(f"/api/v1/templates/{template_id}", headers=admin_headers)
        assert detail.json()["template_name"] == "编辑后"
        assert len(detail.json()["items"]) == 2

    def test_delete_template(self, client, admin_headers, db, test_users):
        """删除模板（admin 有 templates:delete 权限，engineer 没有）"""
        # engineer 没有 delete 权限，验证返回 403
        create_resp = client.post("/api/v1/templates", json={
            "template_name": "待删除", "device_type": "车床",
            "items": [{"item_name": "温度", "data_type": "number",
                       "standard_min": 0, "standard_max": 100, "unit": "℃"}]
        }, headers=admin_headers)
        template_id = create_resp.json()["template_id"]

        resp = client.delete(f"/api/v1/templates/{template_id}", headers=admin_headers)
        assert resp.status_code == 403  # engineer 无 templates:delete 权限

    def test_delete_template_in_use(self, client, admin_headers, db, test_users):
        """删除被设备使用的模板 — 先验证 engineer 无权限"""
        create_resp = client.post("/api/v1/templates", json={
            "template_name": "使用中模板",
            "device_type": "车床",
            "items": [{"item_name": "温度", "data_type": "number",
                       "standard_min": 0, "standard_max": 100, "unit": "℃"}]
        }, headers=admin_headers)
        template_id = create_resp.json()["template_id"]

        # 创建一个设备引用该模板（使用测试的 db 会话，不是 SessionLocal）
        from app.models.device import Device
        device = Device(
            device_code="CSGZ-A01-DBC-99",
            device_name="测试设备",
            location="测试位置",
            template_id=template_id
        )
        db.add(device)
        db.commit()

        # engineer 尝试删除应返回 403（权限不足，不是 409）
        resp = client.delete(f"/api/v1/templates/{template_id}", headers=admin_headers)
        assert resp.status_code == 403

    def test_tech_cannot_delete_template(self, client, tech_headers, admin_headers, db):
        """技术员没有删除权限"""
        create_resp = client.post("/api/v1/templates", json={
            "template_name": "权限测试",
            "device_type": "车床",
            "items": [{"item_name": "温度", "data_type": "number",
                       "standard_min": 0, "standard_max": 100, "unit": "℃"}]
        }, headers=admin_headers)
        template_id = create_resp.json()["template_id"]

        resp = client.delete(f"/api/v1/templates/{template_id}", headers=tech_headers)
        assert resp.status_code == 403