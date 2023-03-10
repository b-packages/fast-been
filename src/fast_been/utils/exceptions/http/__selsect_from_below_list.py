from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class SelectFromBelowListHTTPException(HTTPException):
    def __init__(self, key, pick_list):
        status_code = HTTP_400_BAD_REQUEST
        detail = 'Please select the value of {} from the list below.\n - {}'.format(key, pick_list)
        super(SelectFromBelowListHTTPException, self).__init__(
            status_code=status_code, detail=detail)
