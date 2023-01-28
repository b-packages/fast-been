from fastapi import HTTPException


class RegexValidatorInputValueHTTPException(HTTPException):
    def __init__(self, key, validator_message_info):
        status_code = 400
        detail = 'The input value "{}" is not valid.\n{}'.format(key, validator_message_info)
        super(RegexValidatorInputValueHTTPException, self).__init__(
            status_code=status_code, detail=detail)
