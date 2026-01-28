"""API 配置和依赖注入

提供 FastAPI 的依赖注入
"""
from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Annotated

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from infrastructure.database import get_db
from infrastructure.repositories.user_repository_impl import SQLAlchemyUserRepository


async def get_user_repository(
    session: Annotated[Session, Depends(get_db)]
) -> SQLAlchemyUserRepository:
    """获取用户仓储依赖"""
    return SQLAlchemyUserRepository(session)
