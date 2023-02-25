from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST


class RegexValidatorInputValueHTTPException(HTTPException):
    def __init__(self, key, validator_message_info):
        status_code = HTTP_400_BAD_REQUEST
        detail = 'The input value "{}" is not valid.\n{}'.format(key, validator_message_info)
        super(RegexValidatorInputValueHTTPException, self).__init__(
            status_code=status_code, detail=detail)
