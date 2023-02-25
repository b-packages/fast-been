from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED


class AccessDeniedHTTPException(HTTPException):
    def __init__(self):
        status_code = HTTP_401_UNAUTHORIZED
        detail = 'Access denied.'
        super(AccessDeniedHTTPException, self).__init__(
            status_code=status_code, detail=detail)
