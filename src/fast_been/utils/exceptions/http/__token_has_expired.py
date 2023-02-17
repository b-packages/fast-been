from fastapi import HTTPException
from fast_been.utils.http.response.status.code import UNAUTHORIZED


class TokenHasExpiredHTTPException(HTTPException):
    def __init__(self):
        status_code = UNAUTHORIZED
        detail = 'The token has expired.'
        super(TokenHasExpiredHTTPException, self).__init__(
            status_code=status_code, detail=detail)
