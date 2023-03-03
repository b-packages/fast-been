from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class InformationExpiredHTTPException(HTTPException):
    def __init__(self):
        status_code = HTTP_400_BAD_REQUEST
        detail = 'The entered information has expired.'
        super(InformationExpiredHTTPException, self).__init__(
            status_code=status_code, detail=detail)
