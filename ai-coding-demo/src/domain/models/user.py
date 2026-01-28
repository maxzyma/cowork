"""
用户领域模型

基于规范: SPEC-DATA-USER-001
定义用户实体及其行为
"""

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID
from typing import Optional


@dataclass
class User:
    """
    用户实体

    实现规范: SPEC-DATA-USER-001
    """

    # 主键
    id: UUID

    # 基本信息
    username: str
    email: str
    password_hash: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None

    # 邮箱验证
    email_verified: bool = False
    email_verification_token: Optional[UUID] = None
    email_verification_expires: Optional[datetime] = None

    # 时间戳
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    last_login: Optional[datetime] = None

    # 状态
    is_active: bool = True
    is_deleted: bool = False

    def __post_init__(self):
        """初始化后验证"""
        self.username = self.username.lower()
        self.email = self.email.lower()

    @property
    def full_name(self) -> str:
        """获取全名"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def can_login(self) -> bool:
        """检查是否可以登录"""
        return (
            self.is_active and
            not self.is_deleted and
            self.email_verified
        )

    def verify_email(self) -> None:
        """验证邮箱"""
        self.email_verified = True
        self.email_verification_token = None
        self.email_verification_expires = None
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """停用账户"""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def soft_delete(self) -> None:
        """软删除"""
        self.is_deleted = True
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def update_last_login(self) -> None:
        """更新最后登录时间"""
        self.last_login = datetime.utcnow()
        self.updated_at = datetime.utcnow()


@dataclass
class UserRegistrationResult:
    """
    用户注册结果

    实现规范: SPEC-USER-001, 3.1 API 接口
    """

    user_id: str
    username: str
    email: str
    email_verified: bool
    created_at: datetime
    token: str

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "email_verified": self.email_verified,
            "created_at": self.created_at.isoformat(),
            "token": self.token
        }


@dataclass
class UserProfile:
    """
    用户资料（扩展信息）
    """

    id: UUID
    user_id: UUID
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    birth_date: Optional[datetime] = None
    preferences: dict = field(default_factory=dict)

    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def update_preferences(self, preferences: dict) -> None:
        """更新用户偏好设置"""
        self.preferences.update(preferences)
        self.updated_at = datetime.utcnow()
