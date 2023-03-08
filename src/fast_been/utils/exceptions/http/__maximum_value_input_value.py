from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class MaximumValueInputValueHTTPException(HTTPException):
    def __init__(self, key, maximum_value):
        status_code = HTTP_400_BAD_REQUEST
        detail = 'The input value of {} must be less than {}.'.format(key, maximum_value)
        super(MaximumValueInputValueHTTPException, self).__init__(
            status_code=status_code, detail=detail)
