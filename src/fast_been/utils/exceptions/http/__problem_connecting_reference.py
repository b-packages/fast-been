from fastapi import HTTPException
from starlette.status import HTTP_502_BAD_GATEWAY


class ProblemConnectingReferenceHTTPException(HTTPException):
    def __init__(self):
        status_code = HTTP_502_BAD_GATEWAY
        detail = """There was a problem connecting to the reference.Please try again after a while and if you see
         this message again, let us know so that we can take care of your problem as soon as possible."""
        super(ProblemConnectingReferenceHTTPException, self).__init__(
            status_code=status_code, detail=detail)
