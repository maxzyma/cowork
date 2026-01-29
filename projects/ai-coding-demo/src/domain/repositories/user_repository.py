"""
用户仓储接口

定义用户数据访问抽象
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from src.domain.models.user import User


class UserRepository(ABC):
    """
    用户仓储接口

    定义用户数据访问的抽象接口
    实现类负责具体的数据库操作
    """

    @abstractmethod
    def create(self, user: User) -> User:
        """
        创建新用户

        Args:
            user: 用户实体

        Returns:
            创建的用户（包含生成的ID等）

        Raises:
            ConflictError: 用户名或邮箱已存在
        """
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """
        更新用户

        Args:
            user: 用户实体

        Returns:
            更新后的用户

        Raises:
            NotFoundError: 用户不存在
        """
        pass

    @abstractmethod
    def delete(self, user_id: UUID) -> None:
        """
        删除用户（软删除）

        Args:
            user_id: 用户ID

        Raises:
            NotFoundError: 用户不存在
        """
        pass

    @abstractmethod
    def find_by_id(self, user_id: UUID) -> Optional[User]:
        """
        通过ID查找用户

        Args:
            user_id: 用户ID

        Returns:
            用户实体或None
        """
        pass

    @abstractmethod
    def find_by_username(self, username: str) -> Optional[User]:
        """
        通过用户名查找用户

        Args:
            username: 用户名（小写）

        Returns:
            用户实体或None
        """
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        """
        通过邮箱查找用户

        Args:
            email: 邮箱地址（小写）

        Returns:
            用户实体或None
        """
        pass

    @abstractmethod
    def find_by_verification_token(self, token: str) -> Optional[User]:
        """
        通过验证token查找用户

        Args:
            token: 验证token

        Returns:
            用户实体或None
        """
        pass

    @abstractmethod
    def find_many(
        self,
        offset: int = 0,
        limit: int = 100,
        is_active: Optional[bool] = None,
        is_deleted: Optional[bool] = False
    ) -> List[User]:
        """
        查找多个用户（分页）

        Args:
            offset: 偏移量
            limit: 返回数量限制
            is_active: 是否激活（None表示不过滤）
            is_deleted: 是否删除（默认只返回未删除的）

        Returns:
            用户列表
        """
        pass

    @abstractmethod
    def count(
        self,
        is_active: Optional[bool] = None,
        is_deleted: Optional[bool] = False
    ) -> int:
        """
        统计用户数量

        Args:
            is_active: 是否激活
            is_deleted: 是否删除

        Returns:
            用户数量
        """
        pass

    @abstractmethod
    def username_exists(self, username: str) -> bool:
        """
        检查用户名是否存在

        Args:
            username: 用户名（小写）

        Returns:
            是否存在
        """
        pass

    @abstractmethod
    def email_exists(self, email: str) -> bool:
        """
        检查邮箱是否存在

        Args:
            email: 邮箱地址（小写）

        Returns:
            是否存在
        """
        pass
