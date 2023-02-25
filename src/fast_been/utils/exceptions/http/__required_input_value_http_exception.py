from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class RequiredInputValueHTTPException(HTTPException):
    def __init__(self, key):
        status_code = HTTP_400_BAD_REQUEST
        detail = 'Entering the value of "{}" is required.'.format(key)
        super(RequiredInputValueHTTPException, self).__init__(
            status_code=status_code, detail=detail)
