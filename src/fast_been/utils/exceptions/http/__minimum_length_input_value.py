from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class MinimumLengthInputValueHTTPException(HTTPException):
    def __init__(self, key, minimum_length):
        status_code = HTTP_400_BAD_REQUEST
        detail = 'The length of the input value {} must be greater than {}.'.format(key, minimum_length)
        super(MinimumLengthInputValueHTTPException, self).__init__(
            status_code=status_code, detail=detail)
