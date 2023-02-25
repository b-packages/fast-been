from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED


class TokenIsNotAcceptedHTTPException(HTTPException):
    def __init__(self):
        status_code = HTTP_401_UNAUTHORIZED
        detail = 'The token is not accepted.'
        super(TokenIsNotAcceptedHTTPException, self).__init__(
            status_code=status_code, detail=detail)
