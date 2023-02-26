from pydantic import BaseModel
from typing import Optional, Any
from fast_been.conf.base_settings import BASE_SETTINGS
from .__macro import *


class Request(BaseModel):

    def __init__(self, **kwargs):
        base_request = kwargs[BASE_REQUEST] = kwargs.get(REQUEST)
        if base_request:
            qp = dict(base_request.query_params)
            kwargs[PAGE] = qp.pop(PAGE) if PAGE in qp else BASE_SETTINGS.PAGINATION.DEFAULT_START_PAGE_NUMBER
            kwargs[PAGE_SIZE] = qp.pop(PAGE_SIZE) if PAGE_SIZE in qp else BASE_SETTINGS.PAGINATION.PAGE_SIZE
            kwargs[ORDERING] = qp.pop(ORDERING) if ORDERING in qp else BASE_SETTINGS.PAGINATION.ORDERING
            kwargs[SEARCH] = qp.pop(SEARCH) if SEARCH in qp else None
            kwargs[FILTERS] = qp
            tmp = str(base_request.url)
            kwargs[URL] = tmp.split('?')[0]
        super(Request, self).__init__(**kwargs)

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
    filters: Optional[dict]
    ordering: Optional[list]
    search: Any
    # base request
    base_request: Any
