"""
测试配置与公共 Fixtures
使用 SQLite 避免依赖 MySQL，Mock 启动事件
"""
import sys
import os

os.environ["MYSQL_HOST"] = "127.0.0.1"

import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from passlib.hash import bcrypt

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

# Mock 掉所有数据库依赖，防止启动时连接 MySQL
with patch("app.database.init_db"), \
     patch("app.services.auth_service.init_admin_user"), \
     patch("app.database.SessionLocal"):
    from app.database import Base, get_db
    from app.main import app
    from app.models.user import User, UserRole

# SQLite 测试引擎
TEST_DB_URL = "sqlite:///./test.db"
_test_engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
_TestSession = sessionmaker(autocommit=False, autoflush=False, bind=_test_engine)

Base.metadata.create_all(bind=_test_engine)


def override_get_db():
    db = _TestSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def clean_db():
    with _test_engine.begin() as conn:
        conn.execute(text("PRAGMA foreign_keys=OFF"))
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(text(f"DELETE FROM {table.name}"))
        conn.execute(text("PRAGMA foreign_keys=ON"))


@pytest.fixture
def db():
    db = _TestSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def test_users(db):
    users = [
        User(username="engineer01", password_hash=bcrypt.hash("test123456"),
             role=UserRole.ENGINEER, real_name="测试工程师", is_active=1),
        User(username="tech01", password_hash=bcrypt.hash("test123456"),
             role=UserRole.TECH, real_name="测试技术员", is_active=1),
        User(username="disabled_user", password_hash=bcrypt.hash("test123456"),
             role=UserRole.TECH, real_name="已禁用技术员", is_active=0),
    ]
    for u in users:
        db.add(u)
    db.commit()
    for u in users:
        db.refresh(u)
    return {u.username: u for u in users}


@pytest.fixture
def engineer_token(client, test_users):
    r = client.post("/api/v1/auth/login", json={
        "username": "engineer01", "password": "test123456"
    })
    assert r.status_code == 200
    return r.json()["access_token"]


@pytest.fixture
def tech_token(client, test_users):
    r = client.post("/api/v1/auth/login", json={
        "username": "tech01", "password": "test123456"
    })
    assert r.status_code == 200
    return r.json()["access_token"]


@pytest.fixture
def admin_headers(engineer_token):
    return {"Authorization": f"Bearer {engineer_token}"}


@pytest.fixture
def tech_headers(tech_token):
    return {"Authorization": f"Bearer {tech_token}"}