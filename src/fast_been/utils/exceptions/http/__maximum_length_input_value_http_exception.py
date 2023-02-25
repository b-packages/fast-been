from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class MaximumLengthInputValueHTTPException(HTTPException):
    def __init__(self, key, maximum_length):
        status_code = HTTP_400_BAD_REQUEST
        detail = 'The length of input value {} must be less than {}.'.format(key, maximum_length)
        super(MaximumLengthInputValueHTTPException, self).__init__(
            status_code=status_code, detail=detail)
