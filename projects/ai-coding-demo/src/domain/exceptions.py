"""
领域异常定义

定义业务逻辑中的异常类型
"""

from typing import Optional, List


class BaseDomainError(Exception):
    """基础领域异常"""

    def __init__(self, message: str, code: str = None):
        self.message = message
        self.code = code or self.__class__.__name__
        super().__init__(self.message)


class ValidationError(BaseDomainError):
    """
    验证错误

    当输入数据不符合业务规则时抛出
    """

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        code: str = "VALIDATION_ERROR"
    ):
        self.field = field
        super().__init__(message, code)


class ConflictError(BaseDomainError):
    """
    冲突错误

    当资源冲突（如用户名已存在）时抛出
    """

    def __init__(
        self,
        message: str,
        code: str = "CONFLICT",
        suggestions: Optional[List[str]] = None
    ):
        self.suggestions = suggestions or []
        super().__init__(message, code)


class NotFoundError(BaseDomainError):
    """
    资源未找到错误
    """

    def __init__(
        self,
        message: str,
        resource_type: Optional[str] = None,
        code: str = "NOT_FOUND"
    ):
        self.resource_type = resource_type
        super().__init__(message, code)


class AuthenticationError(BaseDomainError):
    """
    认证错误
    """

    def __init__(
        self,
        message: str = "认证失败",
        code: str = "AUTHENTICATION_ERROR"
    ):
        super().__init__(message, code)


class AuthorizationError(BaseDomainError):
    """
    授权错误
    """

    def __init__(
        self,
        message: str = "无权访问此资源",
        code: str = "AUTHORIZATION_ERROR"
    ):
        super().__init__(message, code)


class RateLimitError(BaseDomainError):
    """
    速率限制错误

    实现规范: SPEC-USER-001, 3.3 业务规则
    """

    def __init__(
        self,
        message: str,
        retry_after: int,
        code: str = "RATE_LIMIT_EXCEEDED"
    ):
        self.retry_after = retry_after
        super().__init__(message, code)


class BusinessRuleError(BaseDomainError):
    """
    业务规则错误
    """

    def __init__(
        self,
        message: str,
        rule_code: Optional[str] = None,
        code: str = "BUSINESS_RULE_VIOLATION"
    ):
        self.rule_code = rule_code
        super().__init__(message, code)


class ExternalServiceError(BaseDomainError):
    """
    外部服务错误
    """

    def __init__(
        self,
        message: str,
        service_name: Optional[str] = None,
        code: str = "EXTERNAL_SERVICE_ERROR"
    ):
        self.service_name = service_name
        super().__init__(message, code)
