from fastapi import HTTPException


class MaximumValueInputValueHTTPException(HTTPException):
    def __init__(self, key, maximum_value):
        status_code = 400
        detail = 'The input value of {} must be less than {}.'.format(key, maximum_value)
        super(MaximumValueInputValueHTTPException, self).__init__(
            status_code=status_code, detail=detail)
