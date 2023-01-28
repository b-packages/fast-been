from fastapi import HTTPException


class RequiredInputValueHTTPException(HTTPException):
    def __init__(self, key):
        status_code = 400
        detail = 'Entering the value of "{}" is required.'.format(key)
        super(RequiredInputValueHTTPException, self).__init__(
            status_code=status_code, detail=detail)
