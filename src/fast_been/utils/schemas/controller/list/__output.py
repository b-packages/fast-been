import math
from typing import Optional
from pydantic import BaseModel

COUNT = 'count'
PAGE_SIZE = 'page_size'
PAGE_NUMBER = 'page_number'
NEXT_PAGE = 'next_page'
PREVIOUS_PAGE = 'previous_page'
URL = 'url'


class OutputList(BaseModel):
    def __init__(self, **kwargs):
        nxt = None
        number_of_pages = math.ceil(kwargs[COUNT] / kwargs[PAGE_SIZE])
        if kwargs[PAGE_NUMBER] < number_of_pages:
            nxt = '{}?page={}&page_size={}'.format(kwargs[URL], kwargs[PAGE_NUMBER] + 1, kwargs[PAGE_SIZE])
        kwargs[NEXT_PAGE] = nxt

        prv = None
        if 1 < kwargs[PAGE_NUMBER]:
            prv = '{}?page={}&page_size={}'.format(kwargs[URL], kwargs[PAGE_NUMBER] - 1, kwargs[PAGE_SIZE])
        kwargs[PREVIOUS_PAGE] = prv

        super(OutputList, self).__init__(**kwargs)

    count: int
    page_number: int = 1
    page_size: int
    next_page: Optional[str]
    previous_page: Optional[str]
    result: list = []
