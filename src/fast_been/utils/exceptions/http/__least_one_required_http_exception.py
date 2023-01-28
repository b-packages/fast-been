from fastapi import HTTPException


class LeastOneRequiredHTTPException(HTTPException):
    def __init__(self, least_one_required_list: list):
        status_code = 400
        tmp = ', '.join(least_one_required_list)
        detail = 'The data entered by the user must include at least one of the following items.\n{}'.format(tmp)
        super(LeastOneRequiredHTTPException, self).__init__(
            status_code=status_code, detail=detail)
