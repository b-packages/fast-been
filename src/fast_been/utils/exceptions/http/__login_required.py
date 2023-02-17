from fastapi import HTTPException
from fast_been.utils.http.response.status.code import UNAUTHORIZED


class LoginRequiredHTTPException(HTTPException):
    def __init__(self):
        status_code = UNAUTHORIZED
        detail = 'You are not logged in.'
        super(LoginRequiredHTTPException, self).__init__(
            status_code=status_code, detail=detail)
