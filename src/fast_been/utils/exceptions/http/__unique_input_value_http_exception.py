from fastapi import HTTPException


class UniqueInputValueHTTPException(HTTPException):
    def __init__(self, key):
        status_code = 400
        detail = 'The input value "{}" must be unique.'.format(key)
        super(UniqueInputValueHTTPException, self).__init__(
            status_code=status_code, detail=detail)
