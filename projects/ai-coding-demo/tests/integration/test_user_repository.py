"""集成测试: 用户仓储

测试 SQLAlchemy 仓储实现
"""
import pytest
from uuid import UUID
from datetime import datetime

from domain.models.user import User
from infrastructure.repositories.user_repository_impl import SQLAlchemyUserRepository


class TestSQLAlchemyUserRepository:
    """SQLAlchemy 用户仓储集成测试"""

    def test_save_user(self, test_user_repository):
        """测试保存用户"""
        user = User(
            email="test@example.com",
            password_hash="hashed_password_123",
            username="testuser"
        )

        saved_user = test_user_repository.save(user)

        assert saved_user.id is not None
        assert saved_user.email == "test@example.com"
        assert saved_user.username == "testuser"
        assert isinstance(saved_user.id, UUID)

    def test_find_by_id(self, test_user_repository):
        """测试根据ID查找用户"""
        user = User(
            email="test@example.com",
            password_hash="hashed_password_123"
        )
        saved_user = test_user_repository.save(user)

        found_user = test_user_repository.find_by_id(saved_user.id)

        assert found_user is not None
        assert found_user.id == saved_user.id
        assert found_user.email == "test@example.com"

    def test_find_by_email(self, test_user_repository):
        """测试根据邮箱查找用户"""
        user = User(
            email="test@example.com",
            password_hash="hashed_password_123"
        )
        test_user_repository.save(user)

        found_user = test_user_repository.find_by_email("test@example.com")

        assert found_user is not None
        assert found_user.email == "test@example.com"

    def test_find_by_username(self, test_user_repository):
        """测试根据用户名查找用户"""
        user = User(
            email="test@example.com",
            password_hash="hashed_password_123",
            username="testuser"
        )
        test_user_repository.save(user)

        found_user = test_user_repository.find_by_username("testuser")

        assert found_user is not None
        assert found_user.username == "testuser"

    def test_email_exists(self, test_user_repository):
        """测试检查邮箱是否存在"""
        user = User(
            email="test@example.com",
            password_hash="hashed_password_123"
        )
        test_user_repository.save(user)

        assert test_user_repository.email_exists("test@example.com") is True
        assert test_user_repository.email_exists("nonexistent@example.com") is False

    def test_username_exists(self, test_user_repository):
        """测试检查用户名是否存在"""
        user = User(
            email="test@example.com",
            password_hash="hashed_password_123",
            username="testuser"
        )
        test_user_repository.save(user)

        assert test_user_repository.username_exists("testuser") is True
        assert test_user_repository.username_exists("nonexistent") is False

    def test_update_user(self, test_user_repository):
        """测试更新用户"""
        user = User(
            email="test@example.com",
            password_hash="hashed_password_123",
            username="testuser"
        )
        saved_user = test_user_repository.save(user)

        # 更新用户
        saved_user.username = "updateduser"
        updated_user = test_user_repository.update(saved_user)

        assert updated_user is not None
        assert updated_user.username == "updateduser"

    def test_delete_user(self, test_user_repository):
        """测试删除用户"""
        user = User(
            email="test@example.com",
            password_hash="hashed_password_123"
        )
        saved_user = test_user_repository.save(user)

        # 删除用户
        result = test_user_repository.delete(saved_user.id)

        assert result is True
        assert test_user_repository.find_by_id(saved_user.id) is None

    def test_list_all_users(self, test_user_repository):
        """测试列出所有用户"""
        # 创建多个用户
        for i in range(3):
            user = User(
                email=f"test{i}@example.com",
                password_hash=f"password_{i}"
            )
            test_user_repository.save(user)

        users = test_user_repository.list_all()

        assert len(users) == 3
