from fastapi import HTTPException
from starlette.status import HTTP_404_NOT_FOUND


class NotFoundHTTPException(HTTPException):
    def __init__(self):
        status_code = HTTP_404_NOT_FOUND
        super(NotFoundHTTPException, self).__init__(status_code=status_code)
