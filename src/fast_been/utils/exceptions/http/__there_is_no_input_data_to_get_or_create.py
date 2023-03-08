from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class ThereIsNoInputDataToGetOrCreateHTTPException(HTTPException):
    def __init__(self):
        status_code = HTTP_400_BAD_REQUEST
        detail = 'There is no input data to get or create.'
        super(ThereIsNoInputDataToGetOrCreateHTTPException, self).__init__(
            status_code=status_code, detail=detail)
