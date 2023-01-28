from fastapi import HTTPException


class NotFoundHTTPException(HTTPException):
    def __init__(self):
        status_code = 404
        super(NotFoundHTTPException, self).__init__(status_code=status_code)
