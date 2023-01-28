import math
from typing import Optional
from pydantic import BaseModel


class OutputList(BaseModel):
    def __init__(self, **kwargs):
        nxt = None
        number_of_pages = math.ceil(kwargs['count'] / kwargs['page_size'])
        if kwargs['page_number'] < number_of_pages:
            nxt = '?page={}&page_size={}'.format(kwargs['page_number'] + 1, kwargs['page_size'])
        kwargs['next_page'] = nxt

        prv = None
        if 1 < kwargs['page_number']:
            prv = '?page={}&page_size={}'.format(kwargs['page_number'] - 1, kwargs['page_size'])
        kwargs['previous_page'] = prv

        super(OutputList, self).__init__(**kwargs)

    count: int
    page_number: int = 1
    page_size: int
    result: list = []
    next_page: Optional[str]
    previous_page: Optional[str]
