from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class TypeInputValueHTTPException(HTTPException):
    def __init__(self, key, type_input_value):
        status_code = HTTP_400_BAD_REQUEST
        detail = 'The input value type {} must be {}.'.format(key, type_input_value)
        super(TypeInputValueHTTPException, self).__init__(
            status_code=status_code, detail=detail)
