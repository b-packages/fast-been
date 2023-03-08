from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class LookupFieldIsNotSetHTTPException(HTTPException):
    def __init__(self):
        status_code = HTTP_400_BAD_REQUEST
        detail = 'Lookup field is not set.'
        super(LookupFieldIsNotSetHTTPException, self).__init__(
            status_code=status_code, detail=detail)
