"""
用户注册服务单元测试

基于规范: SPEC-USER-001
测试覆盖:
- 成功注册场景
- 输入验证场景
- 冲突处理场景
- 边缘情况场景
"""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4

# 模拟的导入（实际实现时替换）
from src.domain.services.user_service import UserService
from src.domain.models.user import User
from src.domain.exceptions import (
    ValidationError,
    ConflictError,
    RateLimitError
)


class TestUserRegistration:
    """用户注册功能测试套件"""

    @pytest.fixture
    def user_service(self):
        """创建用户服务实例"""
        # 使用测试数据库和模拟依赖
        return UserService()

    @pytest.fixture
    def valid_registration_data(self):
        """有效的注册数据"""
        return {
            "username": "john_doe",
            "email": "john@example.com",
            "password": "SecurePass123",
            "firstName": "John",
            "lastName": "Doe"
        }

    # ====== 成功场景测试 ======

    def test_successful_registration_with_all_fields(
        self, user_service, valid_registration_data
    ):
        """
        测试用例: 使用所有字段成功注册
        规范参考: SPEC-USER-001, 5.1 功能测试用例
        """
        # Given: 有效的完整注册信息
        data = valid_registration_data

        # When: 执行注册
        result = user_service.register_user(**data)

        # Then: 验证注册成功
        assert result is not None
        assert result.user_id is not None
        assert result.username == "john_doe"
        assert result.email == "john@example.com"
        assert result.email_verified is False
        assert result.created_at is not None
        assert result.token is not None

    def test_successful_registration_with_minimal_fields(self, user_service):
        """
        测试用例: 使用最小字段成功注册
        规范参考: SPEC-USER-001, 2.1 核心功能
        """
        # Given: 最小必需信息
        data = {
            "username": "jane_doe",
            "email": "jane@example.com",
            "password": "SecurePass456"
        }

        # When: 执行注册
        result = user_service.register_user(**data)

        # Then: 验证注册成功
        assert result is not None
        assert result.username == "jane_doe"
        assert result.email == "jane@example.com"
        assert result.first_name is None
        assert result.last_name is None

    def test_password_is_encrypted_on_registration(self, user_service):
        """
        测试用例: 密码加密存储
        规范参考: SPEC-USER-001, 3.3 业务规则
        """
        # Given: 包含明文密码的注册数据
        data = {
            "username": "secure_user",
            "email": "secure@example.com",
            "password": "MySecurePass123"
        }

        # When: 执行注册
        result = user_service.register_user(**data)

        # Then: 验证密码已加密
        # 密码不应该在响应中返回
        assert not hasattr(result, 'password')
        # 存储的应该是加密后的哈希
        stored_user = user_service.get_user_by_id(result.user_id)
        assert stored_user.password_hash.startswith('$2b$')
        assert stored_user.password_hash != "MySecurePass123"

    def test_verification_email_is_sent(self, user_service, mocker):
        """
        测试用例: 验证邮件发送
        规范参考: SPEC-USER-001, 2.1 核心功能
        """
        # Given: 模拟邮件服务
        mock_email_service = mocker.patch(
            'src.infrastructure.email.EmailService.send_verification_email'
        )

        data = {
            "username": "new_user",
            "email": "new@example.com",
            "password": "SecurePass789"
        }

        # When: 执行注册
        result = user_service.register_user(**data)

        # Then: 验证邮件已发送
        mock_email_service.assert_called_once()
        call_args = mock_email_service.call_args
        assert call_args[0][0] == "new@example.com"
        assert 'verification_token' in call_args[1]

    # ====== 输入验证测试 ======

    def test_username_too_short_raises_validation_error(self, user_service):
        """
        测试用例: 用户名过短
        规范参考: SPEC-USER-001, 3.3 业务规则
        """
        # Given: 用户名少于3字符
        data = {
            "username": "ab",
            "email": "user@example.com",
            "password": "SecurePass123"
        }

        # When/Then: 应该抛出验证错误
        with pytest.raises(ValidationError) as exc_info:
            user_service.register_user(**data)

        assert "username" in str(exc_info.value).lower()
        assert "3" in str(exc_info.value)

    def test_username_too_long_raises_validation_error(self, user_service):
        """
        测试用例: 用户名过长
        规范参考: SPEC-USER-001, 3.3 业务规则
        """
        # Given: 用户名超过20字符
        data = {
            "username": "a" * 21,
            "email": "user@example.com",
            "password": "SecurePass123"
        }

        # When/Then: 应该抛出验证错误
        with pytest.raises(ValidationError) as exc_info:
            user_service.register_user(**data)

        assert "username" in str(exc_info.value).lower()
        assert "20" in str(exc_info.value)

    def test_username_with_invalid_characters_raises_error(self, user_service):
        """
        测试用例: 用户名包含非法字符
        规范参考: SPEC-USER-001, 3.3 业务规则
        """
        # Given: 用户名包含特殊字符
        invalid_usernames = [
            "user-name",  # 连字符
            "user.name",  # 点号
            "user name",  # 空格
            "user@name",  # @符号
            "用户名",      # 中文
        ]

        for username in invalid_usernames:
            data = {
                "username": username,
                "email": "user@example.com",
                "password": "SecurePass123"
            }

            # When/Then: 应该抛出验证错误
            with pytest.raises(ValidationError) as exc_info:
                user_service.register_user(**data)

            assert "username" in str(exc_info.value).lower()

    def test_invalid_email_format_raises_validation_error(self, user_service):
        """
        测试用例: 邮箱格式无效
        规范参考: SPEC-USER-001, 2.3 边缘情况处理
        """
        # Given: 各种无效的邮箱格式
        invalid_emails = [
            "notanemail",
            "missing@domain",
            "@nodomain.com",
            "spaces in@email.com",
            "double@@domain.com",
        ]

        for email in invalid_emails:
            data = {
                "username": "valid_user",
                "email": email,
                "password": "SecurePass123"
            }

            # When/Then: 应该抛出验证错误
            with pytest.raises(ValidationError) as exc_info:
                user_service.register_user(**data)

            assert "email" in str(exc_info.value).lower()

    def test_weak_password_raises_validation_error(self, user_service):
        """
        测试用例: 密码强度不足
        规范参考: SPEC-USER-001, 2.3 边缘情况处理
        """
        # Given: 各种弱密码
        weak_passwords = [
            "short",           # 太短
            "alllowercase",    # 只有小写
            "ALLUPPERCASE",    # 只有大写
            "NoNumbers",       # 没有数字
            "12345678",        # 只有数字
            "password123",     # 常见弱密码
        ]

        for password in weak_passwords:
            data = {
                "username": "valid_user",
                "email": "valid@example.com",
                "password": password
            }

            # When/Then: 应该抛出验证错误
            with pytest.raises(ValidationError) as exc_info:
                user_service.register_user(**data)

            error_message = str(exc_info.value).lower()
            assert "password" in error_message

    # ====== 冲突处理测试 ======

    def test_duplicate_username_raises_conflict_error(
        self, user_service, valid_registration_data
    ):
        """
        测试用例: 用户名已存在
        规范参考: SPEC-USER-001, 2.3 边缘情况处理
        """
        # Given: 已注册的用户
        user_service.register_user(**valid_registration_data)

        # When: 尝试使用相同用户名注册
        duplicate_data = {
            "username": "john_doe",  # 相同用户名
            "email": "different@example.com",
            "password": "SecurePass123"
        }

        # Then: 应该抛出冲突错误
        with pytest.raises(ConflictError) as exc_info:
            user_service.register_user(**duplicate_data)

        error = exc_info.value
        assert error.code == "USERNAME_TAKEN"
        assert "john_doe" in error.message
        # 应该提供替代用户名建议
        assert error.suggestions is not None
        assert len(error.suggestions) > 0

    def test_duplicate_email_raises_conflict_error(
        self, user_service, valid_registration_data
    ):
        """
        测试用例: 邮箱已注册
        规范参考: SPEC-USER-001, 2.3 边缘情况处理
        """
        # Given: 已注册的用户
        user_service.register_user(**valid_registration_data)

        # When: 尝试使用相同邮箱注册
        duplicate_data = {
            "username": "different_user",
            "email": "john@example.com",  # 相同邮箱
            "password": "SecurePass123"
        }

        # Then: 应该抛出冲突错误
        with pytest.raises(ConflictError) as exc_info:
            user_service.register_user(**duplicate_data)

        error = exc_info.value
        assert error.code == "EMAIL_ALREADY_REGISTERED"
        assert "john@example.com" in error.message

    # ====== 边界情况测试 ======

    def test_username_case_insensitive(self, user_service):
        """
        测试用例: 用户名不区分大小写
        规范参考: SPEC-USER-001, 3.3 业务规则
        """
        # Given: 注册一个用户
        user_service.register_user(
            username="JohnDoe",
            email="john@example.com",
            password="SecurePass123"
        )

        # When: 尝试使用不同大小写的用户名注册
        # Then: 应该抛出冲突错误（因为视为相同用户名）
        with pytest.raises(ConflictError):
            user_service.register_user(
                username="johndoe",  # 全小写
                email="different@example.com",
                password="SecurePass123"
            )

    def test_email_case_insensitive(self, user_service):
        """
        测试用例: 邮箱不区分大小写
        规范参考: SPEC-USER-001, 3.3 业务规则
        """
        # Given: 注册一个用户
        user_service.register_user(
            username="user1",
            email="Test@Example.COM",
            password="SecurePass123"
        )

        # When: 尝试使用不同大小写的邮箱注册
        # Then: 应该抛出冲突错误
        with pytest.raises(ConflictError):
            user_service.register_user(
                username="user2",
                email="test@example.com",  # 全小写
                password="SecurePass123"
            )

    def test_reserved_usernames_are_rejected(self, user_service):
        """
        测试用例: 保留用户名被拒绝
        规范参考: SPEC-USER-001, 3.3 业务规则
        """
        # Given: 保留的用户名列表
        reserved_usernames = ["admin", "root", "system", "administrator"]

        for username in reserved_usernames:
            data = {
                "username": username,
                "email": f"{username}@example.com",
                "password": "SecurePass123"
            }

            # When/Then: 应该抛出验证错误
            with pytest.raises(ValidationError) as exc_info:
                user_service.register_user(**data)

            assert "reserved" in str(exc_info.value).lower()

    # ====== 速率限制测试 ======

    def test_rate_limit_exceeded_raises_error(self, user_service, mocker):
        """
        测试用例: 超过速率限制
        规范参考: SPEC-USER-001, 3.3 业务规则
        """
        # Given: 模拟速率限制检查
        mock_rate_limiter = mocker.patch(
            'src.infrastructure.rate_limiter.RateLimiter.check_limit',
            side_effect=RateLimitError("Rate limit exceeded", retry_after=60)
        )

        data = {
            "username": "rate_limited_user",
            "email": "ratelimit@example.com",
            "password": "SecurePass123"
        }

        # When/Then: 应该抛出速率限制错误
        with pytest.raises(RateLimitError) as exc_info:
            user_service.register_user(**data)

        error = exc_info.value
        assert error.retry_after == 60

    # ====== 邮箱验证测试 ======

    def test_email_verification_token_is_generated(self, user_service):
        """
        测试用例: 生成邮箱验证 token
        规范参考: SPEC-USER-001, 3.3 业务规则
        """
        # Given: 注册数据
        data = {
            "username": "verify_user",
            "email": "verify@example.com",
            "password": "SecurePass123"
        }

        # When: 执行注册
        result = user_service.register_user(**data)

        # Then: 验证 token 已生成
        stored_user = user_service.get_user_by_id(result.user_id)
        assert stored_user.email_verification_token is not None
        assert stored_user.email_verification_expires is not None
        # Token 应该在 24 小时后过期
        expiry_delta = stored_user.email_verification_expires - datetime.utcnow()
        assert timedelta(hours=23) < expiry_delta < timedelta(hours=25)

    def test_verify_email_with_valid_token(self, user_service):
        """
        测试用例: 使用有效 token 验证邮箱
        规范参考: SPEC-USER-001, 3.1 API 接口
        """
        # Given: 已注册但未验证的用户
        result = user_service.register_user(
            username="verify_user2",
            email="verify2@example.com",
            password="SecurePass123"
        )

        stored_user = user_service.get_user_by_id(result.user_id)
        token = stored_user.email_verification_token

        # When: 使用 token 验证邮箱
        verify_result = user_service.verify_email(token)

        # Then: 验证成功
        assert verify_result.success is True
        assert verify_result.email_verified is True

        # 确认用户状态已更新
        verified_user = user_service.get_user_by_id(result.user_id)
        assert verified_user.email_verified is True
        assert verified_user.email_verification_token is None

    def test_verify_email_with_expired_token(self, user_service, mocker):
        """
        测试用例: 使用过期 token 验证邮箱
        规范参考: SPEC-USER-001, 2.3 边缘情况处理
        """
        # Given: 已注册但 token 已过期的用户
        result = user_service.register_user(
            username="expired_user",
            email="expired@example.com",
            password="SecurePass123"
        )

        stored_user = user_service.get_user_by_id(result.user_id)
        token = stored_user.email_verification_token

        # 模拟时间流逝，token 过期
        mocker.patch(
            'src.domain.services.user_service.datetime'
        ).utcnow.return_value = datetime.utcnow() + timedelta(hours=25)

        # When/Then: 应该抛出验证错误
        with pytest.raises(ValidationError) as exc_info:
            user_service.verify_email(token)

        assert "expired" in str(exc_info.value).lower()

    def test_resend_verification_email(self, user_service, mocker):
        """
        测试用例: 重新发送验证邮件
        规范参考: SPEC-USER-001, 3.1 API 接口
        """
        # Given: 已注册但未验证的用户
        result = user_service.register_user(
            username="resend_user",
            email="resend@example.com",
            password="SecurePass123"
        )

        mock_email_service = mocker.patch(
            'src.infrastructure.email.EmailService.send_verification_email'
        )

        # When: 重新发送验证邮件
        resend_result = user_service.resend_verification_email("resend@example.com")

        # Then: 验证邮件已发送
        assert resend_result.success is True
        mock_email_service.assert_called_once()


# ====== 集成测试标记 ======

@pytest.mark.integration
class TestUserRegistrationIntegration:
    """用户注册集成测试（需要真实数据库）"""

    def test_full_registration_workflow(self):
        """
        测试用例: 完整注册流程集成测试
        规范参考: SPEC-USER-001
        """
        # 这里会进行端到端的集成测试
        # 包括数据库、邮件服务、缓存等
        pass
