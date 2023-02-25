from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED


class TokenHasExpiredHTTPException(HTTPException):
    def __init__(self):
        status_code = HTTP_401_UNAUTHORIZED
        detail = 'The token has expired.'
        super(TokenHasExpiredHTTPException, self).__init__(
            status_code=status_code, detail=detail)
