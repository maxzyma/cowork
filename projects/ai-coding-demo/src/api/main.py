"""FastAPI 应用入口点

实现用户管理 API，基于规范 SPEC-USER-001
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from uuid import UUID

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.services.user_service import UserService
from domain.models.user import User
from domain.exceptions import (
    UserAlreadyExistsError,
    ValidationError,
    DomainError
)


class RegistrationRequest(BaseModel):
    """用户注册请求模型"""
    email: EmailStr = Field(..., description="用户邮箱")
    password: str = Field(..., min_length=8, max_length=128, description="用户密码")
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="用户名")


class UserResponse(BaseModel):
    """用户响应模型"""
    id: UUID
    email: str
    username: Optional[str]
    is_active: bool
    created_at: str

    @classmethod
    def from_domain(cls, user: User) -> "UserResponse":
        """从领域模型转换"""
        return cls(
            id=user.id,
            email=user.email,
            username=user.username,
            is_active=user.is_active,
            created_at=user.created_at.isoformat()
        )


class ErrorResponse(BaseModel):
    """错误响应模型"""
    error: str
    detail: str


# 创建 FastAPI 应用
app = FastAPI(
    title="User Management Service",
    description="AI Coding 驱动开发演示 - 用户管理服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 用户服务实例 (实际应用中应该通过依赖注入)
user_service = UserService()


@app.get("/", tags=["Health"])
async def root():
    """健康检查端点"""
    return {
        "service": "User Management Service",
        "status": "healthy",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """详细健康检查"""
    return {
        "status": "healthy",
        "service": "user-management",
        "dependencies": []
    }


@app.post(
    "/api/v1/users/register",
    response_model=UserResponse,
    responses={
        400: {"model": ErrorResponse, "description": "验证错误"},
        409: {"model": ErrorResponse, "description": "用户已存在"},
        500: {"model": ErrorResponse, "description": "服务器错误"}
    },
    tags=["Users"]
)
async def register_user(request: RegistrationRequest):
    """
    用户注册端点

    基于规范: SPEC-USER-001

    **业务规则:**
    - 邮箱必须唯一
    - 密码强度: 最少8字符，包含大小写字母、数字
    - 用户名可选，如果提供必须唯一

    **成功响应:** 201 + 用户信息
    **失败响应:**
    - 400: 输入验证失败
    - 409: 邮箱或用户名已存在
    """
    try:
        # 调用领域服务进行用户注册
        user = user_service.register_user(
            email=request.email,
            password=request.password,
            username=request.username
        )

        return UserResponse.from_domain(user)

    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=409,
            detail={
                "error": "USER_ALREADY_EXISTS",
                "detail": str(e)
            }
        )

    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "VALIDATION_ERROR",
                "detail": str(e)
            }
        )

    except DomainError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "DOMAIN_ERROR",
                "detail": str(e)
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "INTERNAL_ERROR",
                "detail": "An unexpected error occurred"
            }
        )


@app.get(
    "/api/v1/users/{user_id}",
    response_model=UserResponse,
    responses={
        404: {"model": ErrorResponse, "description": "用户不存在"}
    },
    tags=["Users"]
)
async def get_user(user_id: UUID):
    """
    获取用户信息

    **参数:**
    - user_id: 用户UUID

    **成功响应:** 200 + 用户信息
    **失败响应:**
    - 404: 用户不存在
    """
    # TODO: 实现获取用户逻辑
    raise HTTPException(status_code=501, detail="Not implemented yet")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """全局异常处理器"""
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_ERROR",
            "detail": "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
