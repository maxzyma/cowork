"""测试工具函数和 fixtures"""
import sys
import os
from typing import Generator

import pytest
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from infrastructure.database import Base, get_db
from infrastructure.repositories.user_repository_impl import SQLAlchemyUserRepository


# 使用内存 SQLite 数据库进行测试
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def test_engine():
    """创建测试数据库引擎"""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_session(test_engine) -> Generator[Session, None, None]:
    """创建测试数据库会话"""
    connection = test_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def test_user_repository(test_session):
    """创建测试用户仓储"""
    return SQLAlchemyUserRepository(test_session)


@pytest.fixture
def test_db(test_session):
    """FastAPI 依赖注入测试数据库"""
    try:
        yield test_session
    finally:
        test_session.rollback()
