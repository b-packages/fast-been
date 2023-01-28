from fastapi import HTTPException


class ThereIsNoInputDataToRegisterHTTPException(HTTPException):
    def __init__(self):
        status_code = 400
        detail = 'There is no input data to register.'
        super(ThereIsNoInputDataToRegisterHTTPException, self).__init__(
            status_code=status_code, detail=detail)
