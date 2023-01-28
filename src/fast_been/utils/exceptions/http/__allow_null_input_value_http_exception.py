from fastapi import HTTPException


class AllowNullInputValueHTTPException(HTTPException):
    def __init__(self, key):
        status_code = 400
        detail = 'The input value of "{}" cannot be null.'.format(key)
        super(AllowNullInputValueHTTPException, self).__init__(
            status_code=status_code, detail=detail)
