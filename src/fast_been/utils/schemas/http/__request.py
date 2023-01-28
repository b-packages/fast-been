from pydantic import BaseModel
from typing import Optional, Any

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
            kwargs[PAGE] = base_request.query_params.get(PAGE)
            kwargs[PAGE_SIZE] = base_request.query_params.get(PAGE_SIZE)
            kwargs[FILTERS] = base_request.query_params.get(FILTERS)
            kwargs[ORDERING] = base_request.query_params.get(ORDERING)
            kwargs[SEARCH] = base_request.query_params.get(SEARCH)
            kwargs[URL] = str(base_request.url)
        return kwargs

    def __kwargs(self, **kwargs):
        kwargs = self.__base_request_decoder(**kwargs)
        return kwargs
