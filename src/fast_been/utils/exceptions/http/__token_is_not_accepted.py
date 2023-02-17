from fastapi import HTTPException
from fast_been.utils.http.response.status.code import UNAUTHORIZED


class TokenIsNotAcceptedHTTPException(HTTPException):
    def __init__(self):
        status_code = UNAUTHORIZED
        detail = 'The token is not accepted.'
        super(TokenIsNotAcceptedHTTPException, self).__init__(
            status_code=status_code, detail=detail)
