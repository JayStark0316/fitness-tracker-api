class BaseAPIException(Exception):
    def __init__(self, message, status_code: int = 500):
        super().__init__(message)
        self.status_code = status_code
        self.message = message

class BadRequestException(BaseAPIException):
    def __init__(self, message):
        super().__init__(message, 400)

class NotFoundException(BaseAPIException):
    def __init__(self, message):
        super().__init__(message, 404)

class InvalidArgumentException(BaseAPIException):
    def __init__(self, message):
        super().__init__(message, status_code=400)

class PermissionDeniedException(BaseAPIException):
    def __init__(self,message):
        super().__init__(message, status_code=403)

class UnauthorizedException(BaseAPIException):
    def __init__(self,message):
        super().__init__(message, status_code=401)

class ResourceConflictException(BaseAPIException):
    def __init__(self, message):
        super().__init__(message, status_code=409)

class InternalServerErrorException(BaseAPIException):
    def __init__(self, message):
        super().__init__(message, 500)