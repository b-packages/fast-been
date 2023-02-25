from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class AllowNullInputValueHTTPException(HTTPException):
    def __init__(self, key):
        status_code = HTTP_400_BAD_REQUEST
        detail = 'The input value of "{}" cannot be null.'.format(key)
        super(AllowNullInputValueHTTPException, self).__init__(
            status_code=status_code, detail=detail)
