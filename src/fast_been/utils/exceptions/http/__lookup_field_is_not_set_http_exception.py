from fastapi import HTTPException


class LookupFieldIsNotSetHTTPException(HTTPException):
    def __init__(self):
        status_code = 400
        detail = 'Lookup field is not set.'
        super(LookupFieldIsNotSetHTTPException, self).__init__(
            status_code=status_code, detail=detail)
