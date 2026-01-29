"""用户仓储实现

基于 SQLAlchemy 的用户数据访问实现
实现 UserRepository 接口
"""
from typing import Optional, List
from uuid import UUID

from sqlalchemy.orm import Session

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from domain.models.user import User
from domain.repositories.user_repository import UserRepository
from infrastructure.models.user_sql_model import UserModel


class SQLAlchemyUserRepository(UserRepository):
    """SQLAlchemy 用户仓储实现"""

    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> User:
        """保存用户"""
        user_model = UserModel(
            id=user.id,
            email=user.email,
            password_hash=user.password_hash,
            username=user.username,
            is_active=user.is_active,
            created_at=user.created_at
        )

        self.session.add(user_model)
        self.session.commit()
        self.session.refresh(user_model)

        return self._to_domain(user_model)

    def find_by_id(self, user_id: UUID) -> Optional[User]:
        """根据ID查找用户"""
        user_model = self.session.query(UserModel).filter(
            UserModel.id == user_id
        ).first()

        return self._to_domain(user_model) if user_model else None

    def find_by_email(self, email: str) -> Optional[User]:
        """根据邮箱查找用户"""
        user_model = self.session.query(UserModel).filter(
            UserModel.email == email
        ).first()

        return self._to_domain(user_model) if user_model else None

    def find_by_username(self, username: str) -> Optional[User]:
        """根据用户名查找用户"""
        user_model = self.session.query(UserModel).filter(
            UserModel.username == username
        ).first()

        return self._to_domain(user_model) if user_model else None

    def email_exists(self, email: str) -> bool:
        """检查邮箱是否存在"""
        return self.session.query(UserModel).filter(
            UserModel.email == email
        ).first() is not None

    def username_exists(self, username: str) -> bool:
        """检查用户名是否存在"""
        return self.session.query(UserModel).filter(
            UserModel.username == username
        ).first() is not None

    def update(self, user: User) -> User:
        """更新用户"""
        user_model = self.session.query(UserModel).filter(
            UserModel.id == user.id
        ).first()

        if user_model:
            user_model.email = user.email
            user_model.password_hash = user.password_hash
            user_model.username = user.username
            user_model.is_active = user.is_active

            self.session.commit()
            self.session.refresh(user_model)

            return self._to_domain(user_model)

        return None

    def delete(self, user_id: UUID) -> bool:
        """删除用户"""
        user_model = self.session.query(UserModel).filter(
            UserModel.id == user_id
        ).first()

        if user_model:
            self.session.delete(user_model)
            self.session.commit()
            return True

        return False

    def list_all(self, limit: int = 100, offset: int = 0) -> List[User]:
        """列出所有用户"""
        user_models = self.session.query(UserModel).limit(limit).offset(offset).all()
        return [self._to_domain(um) for um in user_models]

    @staticmethod
    def _to_domain(user_model: UserModel) -> User:
        """将 SQL 模型转换为领域模型"""
        if not user_model:
            return None

        return User(
            id=user_model.id,
            email=user_model.email,
            password_hash=user_model.password_hash,
            username=user_model.username,
            is_active=user_model.is_active,
            created_at=user_model.created_at
        )
