"""
用户服务实现

基于规范: SPEC-USER-001
对应测试: tests/unit/domain/test_user_registration.py

此实现遵循领域驱动设计原则，处理用户注册相关的业务逻辑。
"""

import re
import bcrypt
from datetime import datetime, timedelta
from uuid import uuid4
from typing import Optional, List, Dict, Any

from src.domain.models.user import User, UserRegistrationResult
from src.domain.repositories.user_repository import UserRepository
from src.domain.exceptions import (
    ValidationError,
    ConflictError,
    RateLimitError,
    NotFoundError
)
from src.infrastructure.email import EmailService
from src.infrastructure.rate_limiter import RateLimiter
from src.infrastructure.logging import get_logger


logger = get_logger(__name__)


class UserService:
    """
    用户服务类

    负责处理用户注册、验证、资料管理等核心业务逻辑。
    实现规范: SPEC-USER-001
    """

    # 保留用户名列表（规范: SPEC-USER-001, 3.3）
    RESERVED_USERNAMES = {
        'admin', 'root', 'system', 'administrator',
        'moderator', 'support', 'help', 'api',
        'www', 'mail', 'ftp', 'localhost'
    }

    # 常见弱密码列表
    COMMON_WEAK_PASSWORDS = {
        'password', 'password123', '12345678', 'qwerty',
        'abc123', 'monkey', '1234567', 'letmein'
    }

    def __init__(
        self,
        user_repository: UserRepository,
        email_service: EmailService,
        rate_limiter: RateLimiter
    ):
        """
        初始化用户服务

        Args:
            user_repository: 用户数据仓储
            email_service: 邮件服务
            rate_limiter: 速率限制器
        """
        self.user_repository = user_repository
        self.email_service = email_service
        self.rate_limiter = rate_limiter

    def register_user(
        self,
        username: str,
        email: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone_number: Optional[str] = None,
        ip_address: Optional[str] = None
    ) -> UserRegistrationResult:
        """
        注册新用户

        实现规范: SPEC-USER-001, 2.1 核心功能

        Args:
            username: 用户名（3-20字符）
            email: 邮箱地址
            password: 密码（8-128字符）
            first_name: 名字（可选）
            last_name: 姓氏（可选）
            phone_number: 电话号码（可选）
            ip_address: 客户端IP（用于速率限制）

        Returns:
            UserRegistrationResult: 注册结果

        Raises:
            ValidationError: 输入验证失败
            ConflictError: 用户名或邮箱已存在
            RateLimitError: 超过速率限制
        """
        logger.info(f"开始注册流程: username={username}, email={email}")

        # 1. 速率限制检查（规范: SPEC-USER-001, 3.3）
        self._check_rate_limit(ip_address or 'unknown')

        # 2. 输入验证
        self._validate_username(username)
        self._validate_email(email)
        self._validate_password(password)

        if first_name:
            self._validate_name_field(first_name, "first_name")
        if last_name:
            self._validate_name_field(last_name, "last_name")
        if phone_number:
            self._validate_phone_number(phone_number)

        # 3. 检查唯一性（规范: SPEC-USER-001, 2.3）
        self._check_username_availability(username)
        self._check_email_availability(email)

        # 4. 密码加密（规范: SPEC-USER-001, 3.3）
        password_hash = self._hash_password(password)

        # 5. 生成邮箱验证 token（规范: SPEC-USER-001, 3.3）
        verification_token = uuid4()
        verification_expires = datetime.utcnow() + timedelta(hours=24)

        # 6. 创建用户对象
        user = User(
            id=uuid4(),
            username=username.lower(),  # 统一小写存储
            email=email.lower(),        # 统一小写存储
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email_verified=False,
            email_verification_token=verification_token,
            email_verification_expires=verification_expires,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_active=True,
            is_deleted=False
        )

        # 7. 保存到数据库
        try:
            saved_user = self.user_repository.create(user)
        except Exception as e:
            logger.error(f"保存用户失败: {str(e)}")
            raise

        # 8. 发送验证邮件（异步）（规范: SPEC-USER-001, 2.1）
        try:
            self.email_service.send_verification_email(
                email=saved_user.email,
                username=saved_user.username,
                verification_token=str(verification_token)
            )
            logger.info(f"验证邮件已发送: email={email}")
        except Exception as e:
            logger.error(f"发送验证邮件失败: {str(e)}")
            # 邮件发送失败不阻止注册

        # 9. 生成临时 token
        auth_token = self._generate_auth_token(saved_user.id)

        logger.info(f"注册成功: user_id={saved_user.id}, username={username}")

        # 10. 返回注册结果（规范: SPEC-USER-001, 3.1）
        return UserRegistrationResult(
            user_id=str(saved_user.id),
            username=saved_user.username,
            email=saved_user.email,
            email_verified=saved_user.email_verified,
            created_at=saved_user.created_at,
            token=auth_token
        )

    def verify_email(self, token: str) -> Dict[str, Any]:
        """
        验证邮箱

        实现规范: SPEC-USER-001, 3.1 API 接口

        Args:
            token: 邮箱验证 token

        Returns:
            验证结果

        Raises:
            ValidationError: token 无效或已过期
            NotFoundError: 用户不存在
        """
        logger.info(f"开始邮箱验证: token={token[:8]}...")

        # 1. 查找用户
        user = self.user_repository.find_by_verification_token(token)
        if not user:
            logger.warning(f"无效的验证 token: {token[:8]}...")
            raise ValidationError("无效的验证 token")

        # 2. 检查是否已验证
        if user.email_verified:
            logger.info(f"邮箱已经验证过: user_id={user.id}")
            return {
                "status": "success",
                "message": "邮箱已经验证过",
                "data": {
                    "user_id": str(user.id),
                    "email_verified": True
                }
            }

        # 3. 检查 token 是否过期（规范: SPEC-USER-001, 3.3）
        if datetime.utcnow() > user.email_verification_expires:
            logger.warning(f"验证 token 已过期: user_id={user.id}")
            raise ValidationError("验证 token 已过期，请重新发送验证邮件")

        # 4. 更新用户状态
        user.email_verified = True
        user.email_verification_token = None
        user.email_verification_expires = None
        user.updated_at = datetime.utcnow()

        self.user_repository.update(user)

        logger.info(f"邮箱验证成功: user_id={user.id}")

        return {
            "status": "success",
            "message": "邮箱验证成功",
            "data": {
                "user_id": str(user.id),
                "email_verified": True
            }
        }

    def resend_verification_email(self, email: str) -> Dict[str, Any]:
        """
        重新发送验证邮件

        实现规范: SPEC-USER-001, 3.1 API 接口

        Args:
            email: 用户邮箱

        Returns:
            操作结果

        Raises:
            NotFoundError: 用户不存在
            ValidationError: 邮箱已验证或速率限制
        """
        logger.info(f"重新发送验证邮件: email={email}")

        # 1. 查找用户
        user = self.user_repository.find_by_email(email.lower())
        if not user:
            raise NotFoundError("用户不存在")

        # 2. 检查是否已验证
        if user.email_verified:
            raise ValidationError("邮箱已经验证过")

        # 3. 速率限制检查（规范: SPEC-USER-001, 3.3）
        rate_limit_key = f"resend_verification:{user.id}"
        if not self.rate_limiter.check_limit(rate_limit_key, max_requests=5, window_hours=1):
            raise RateLimitError(
                "重发验证邮件次数过多，请稍后再试",
                retry_after=3600
            )

        # 4. 生成新的验证 token
        verification_token = uuid4()
        verification_expires = datetime.utcnow() + timedelta(hours=24)

        user.email_verification_token = verification_token
        user.email_verification_expires = verification_expires
        user.updated_at = datetime.utcnow()

        self.user_repository.update(user)

        # 5. 发送邮件
        try:
            self.email_service.send_verification_email(
                email=user.email,
                username=user.username,
                verification_token=str(verification_token)
            )
            logger.info(f"验证邮件已重新发送: email={email}")
        except Exception as e:
            logger.error(f"发送验证邮件失败: {str(e)}")
            raise

        return {
            "status": "success",
            "message": "验证邮件已重新发送"
        }

    def get_user_by_id(self, user_id: str) -> User:
        """获取用户（通过ID）"""
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise NotFoundError(f"用户不存在: {user_id}")
        return user

    # ====== 私有方法：验证逻辑 ======

    def _validate_username(self, username: str) -> None:
        """
        验证用户名
        规范: SPEC-USER-001, 3.3 业务规则
        """
        if not username:
            raise ValidationError("用户名不能为空")

        # 长度检查
        if len(username) < 3:
            raise ValidationError("用户名至少需要3个字符")
        if len(username) > 20:
            raise ValidationError("用户名最多20个字符")

        # 格式检查：字母开头，字母数字下划线
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', username):
            raise ValidationError(
                "用户名必须以字母开头，只能包含字母、数字和下划线"
            )

        # 保留用户名检查
        if username.lower() in self.RESERVED_USERNAMES:
            raise ValidationError("此用户名为系统保留，无法使用")

    def _validate_email(self, email: str) -> None:
        """
        验证邮箱格式
        规范: SPEC-USER-001, 3.3 业务规则
        """
        if not email:
            raise ValidationError("邮箱不能为空")

        # RFC 5322 简化版本
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            raise ValidationError("邮箱格式无效")

        if len(email) > 255:
            raise ValidationError("邮箱地址过长")

    def _validate_password(self, password: str) -> None:
        """
        验证密码强度
        规范: SPEC-USER-001, 3.3 业务规则
        """
        if not password:
            raise ValidationError("密码不能为空")

        # 长度检查
        if len(password) < 8:
            raise ValidationError("密码至少需要8个字符")
        if len(password) > 128:
            raise ValidationError("密码最多128个字符")

        # 复杂度检查
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)

        if not (has_upper and has_lower and has_digit):
            raise ValidationError(
                "密码必须包含至少一个大写字母、一个小写字母和一个数字"
            )

        # 弱密码检查
        if password.lower() in self.COMMON_WEAK_PASSWORDS:
            raise ValidationError("此密码过于常见，请选择更安全的密码")

    def _validate_name_field(self, name: str, field_name: str) -> None:
        """验证姓名字段"""
        if len(name) > 50:
            raise ValidationError(f"{field_name} 最多50个字符")

    def _validate_phone_number(self, phone: str) -> None:
        """验证电话号码（简化版）"""
        if not re.match(r'^\+?[1-9]\d{1,14}$', phone):
            raise ValidationError("电话号码格式无效")

    def _check_username_availability(self, username: str) -> None:
        """
        检查用户名是否可用
        规范: SPEC-USER-001, 2.3 边缘情况处理
        """
        existing_user = self.user_repository.find_by_username(username.lower())
        if existing_user:
            # 生成建议的替代用户名
            suggestions = self._generate_username_suggestions(username)
            raise ConflictError(
                message=f"用户名 '{username}' 已被使用",
                code="USERNAME_TAKEN",
                suggestions=suggestions
            )

    def _check_email_availability(self, email: str) -> None:
        """
        检查邮箱是否可用
        规范: SPEC-USER-001, 2.3 边缘情况处理
        """
        existing_user = self.user_repository.find_by_email(email.lower())
        if existing_user:
            raise ConflictError(
                message=f"邮箱 '{email}' 已被注册",
                code="EMAIL_ALREADY_REGISTERED"
            )

    def _hash_password(self, password: str) -> str:
        """
        密码加密
        规范: SPEC-USER-001, 3.3 业务规则
        使用 bcrypt，cost factor = 12
        """
        salt = bcrypt.gensalt(rounds=12)
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password_hash.decode('utf-8')

    def _check_rate_limit(self, identifier: str) -> None:
        """
        速率限制检查
        规范: SPEC-USER-001, 3.3 业务规则
        注册端点: 5次/小时/IP
        """
        rate_limit_key = f"registration:{identifier}"
        if not self.rate_limiter.check_limit(
            rate_limit_key,
            max_requests=5,
            window_hours=1
        ):
            raise RateLimitError(
                "注册请求过于频繁，请稍后再试",
                retry_after=3600
            )

    def _generate_username_suggestions(self, username: str) -> List[str]:
        """生成可用的用户名建议"""
        import random
        suggestions = []

        # 添加数字后缀
        for i in range(1, 4):
            suffix = random.randint(1, 999)
            suggestion = f"{username}{suffix}"
            if not self.user_repository.find_by_username(suggestion.lower()):
                suggestions.append(suggestion)

        # 添加下划线和年份
        year = datetime.utcnow().year
        suggestion = f"{username}_{year}"
        if not self.user_repository.find_by_username(suggestion.lower()):
            suggestions.append(suggestion)

        return suggestions[:3]  # 最多返回3个建议

    def _generate_auth_token(self, user_id: uuid4) -> str:
        """
        生成认证 token（JWT）
        这里简化处理，实际应该使用 JWT 库
        """
        # 实际实现应该使用 PyJWT 或类似库
        return f"token_{user_id}_{datetime.utcnow().timestamp()}"
