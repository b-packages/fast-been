from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class MinimumValueInputValueHTTPException(HTTPException):
    def __init__(self, key, minimum_value):
        status_code = HTTP_400_BAD_REQUEST
        detail = 'The input value of {} must be greater than {}.'.format(key, minimum_value)
        super(MinimumValueInputValueHTTPException, self).__init__(
            status_code=status_code, detail=detail)