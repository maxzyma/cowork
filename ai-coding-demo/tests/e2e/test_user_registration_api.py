"""E2E 测试: 用户注册 API

测试完整的用户注册流程
"""
import pytest
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from api.main import app


@pytest.mark.e2e
class TestUserRegistrationE2E:
    """用户注册端到端测试"""

    async def test_register_user_success(self):
        """测试成功注册用户"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/users/register",
                json={
                    "email": "test@example.com",
                    "password": "SecurePass123",
                    "username": "testuser"
                }
            )

            assert response.status_code == 200
            data = response.json()
            assert data["email"] == "test@example.com"
            assert data["username"] == "testuser"
            assert data["is_active"] is True
            assert "id" in data

    async def test_register_user_invalid_email(self):
        """测试注册时使用无效邮箱"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/users/register",
                json={
                    "email": "invalid-email",
                    "password": "SecurePass123"
                }
            )

            assert response.status_code == 422  # Pydantic validation error

    async def test_register_user_weak_password(self):
        """测试注册时使用弱密码"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.post(
                "/api/v1/users/register",
                json={
                    "email": "test@example.com",
                    "password": "weak"
                }
            )

            assert response.status_code == 422  # Pydantic validation error

    async def test_health_check(self):
        """测试健康检查端点"""
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as client:
            response = await client.get("/health")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
