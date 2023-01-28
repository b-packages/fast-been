from fastapi import HTTPException


class AllowBlankInputValueHTTPException(HTTPException):
    def __init__(self, key):
        status_code = 400
        detail = 'The input value "{}" cannot be blank.'.format(key)
        super(AllowBlankInputValueHTTPException, self).__init__(
            status_code=status_code, detail=detail)
