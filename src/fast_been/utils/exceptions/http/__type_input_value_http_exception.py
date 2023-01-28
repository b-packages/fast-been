from fastapi import HTTPException


class TypeInputValueHTTPException(HTTPException):
    def __init__(self, key, type_input_value):
        status_code = 400
        detail = 'The input value type {} must be {}.'.format(key, type_input_value)
        super(TypeInputValueHTTPException, self).__init__(
            status_code=status_code, detail=detail)
