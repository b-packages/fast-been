from fastapi import HTTPException


class MinimumValueInputValueHTTPException(HTTPException):
    def __init__(self, key, minimum_value):
        status_code = 418
        detail = 'The input value of {} must be greater than {}.'.format(key, minimum_value)
        super(MinimumValueInputValueHTTPException, self).__init__(
            status_code=status_code, detail=detail)