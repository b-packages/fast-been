from pydantic import BaseModel
from typing import Optional, Any
from fast_been.conf.base_settings import BASE_SETTINGS
from .__macro import *


class Request(BaseModel):

    def __init__(self, **kwargs):
        super(Request, self).__init__(**self.__kwargs(**kwargs))

    # input data
    input_data: Optional[dict]
    # auth
    beanser_pid: Optional[str]
    # url
    lookup_field: Any
    url: str = ''
    # query params
    page: Optional[int]
    page_size: Optional[int]
    filters: Optional[list]
    ordering: Optional[list]
    search: Optional[list]
    # base request
    base_request: Any

    @staticmethod
    def __base_request_decoder(**kwargs):
        base_request = kwargs[BASE_REQUEST] = kwargs.get(REQUEST)
        if base_request:
            qp = base_request.query_params.copy()
            kwargs[PAGE] = qp.pop(PAGE) if PAGE in qp else BASE_SETTINGS.PAGINATION.DEFAULT_START_PAGE_NUMBER
            kwargs[PAGE_SIZE] = qp.pop(PAGE_SIZE) if PAGE_SIZE in qp else BASE_SETTINGS.PAGINATION.PAGE_SIZE
            kwargs[ORDERING] = qp.pop(ORDERING) if ORDERING in qp else BASE_SETTINGS.PAGINATION.PAGE_SIZE
            kwargs[SEARCH] = qp.pop(SEARCH) if SEARCH in qp else BASE_SETTINGS.PAGINATION.PAGE_SIZE
            kwargs[FILTERS] = FILTERS
            tmp = str(base_request.url)
            kwargs[URL] = tmp.split('?')[0]
        return kwargs

    def __kwargs(self, **kwargs):
        kwargs = self.__base_request_decoder(**kwargs)
        return kwargs
