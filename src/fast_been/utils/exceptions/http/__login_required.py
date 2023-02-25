from fastapi import HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED


class LoginRequiredHTTPException(HTTPException):
    def __init__(self):
        status_code = HTTP_401_UNAUTHORIZED
        detail = 'You are not logged in.'
        super(LoginRequiredHTTPException, self).__init__(
            status_code=status_code, detail=detail)
