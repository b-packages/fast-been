from fastapi import HTTPException
from fast_been.utils.http.response.status.code import UNAUTHORIZED


class AccessDeniedHTTPException(HTTPException):
    def __init__(self):
        status_code = UNAUTHORIZED
        detail = 'Access denied.'
        super(AccessDeniedHTTPException, self).__init__(
            status_code=status_code, detail=detail)
