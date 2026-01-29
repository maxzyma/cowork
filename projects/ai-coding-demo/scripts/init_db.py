#!/usr/bin/env python3
"""
数据库初始化脚本
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from infrastructure.database import init_db, engine
from infrastructure.models.user_sql_model import UserModel


def main():
    """初始化数据库表"""
    print("初始化数据库...")

    try:
        init_db()
        print("✅ 数据库初始化成功！")

        # 检查表是否创建
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        print(f"创建的表: {', '.join(tables)}")

    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
