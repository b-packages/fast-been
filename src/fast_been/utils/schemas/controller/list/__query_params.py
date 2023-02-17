from pydantic import BaseModel
from typing import Optional, List, Dict

from fast_been.conf.base_settings import BASE_SETTINGS

FILTERS = 'filters'
FILTER_SET = 'filter_set'
ORDERING = 'ordering'
ORDER_SET = 'order_set'
PAGE = 'page'
PAGE_SIZE = 'page_size'


class QueryParams(BaseModel):
    def __init__(self, **kwargs):
        # Validate: Filters
        kwargs[FILTERS] = kwargs[FILTERS] if kwargs.get(FILTER_SET) and kwargs.get(FILTERS) else {}
        tmp = {}
        for k, v in kwargs[FILTERS].items():
            if k in kwargs[FILTER_SET]:
                tmp[k] = v
        kwargs[FILTERS] = tmp if len(tmp) else None
        kwargs.pop(FILTER_SET)
        # Validate: orderings
        kwargs[ORDERING] = kwargs[ORDERING] if kwargs.get(ORDER_SET) and kwargs.get(ORDERING) else []
        tmp = []
        for i in kwargs[ORDERING]:
            if i in kwargs[ORDER_SET]:
                tmp.append(i)
        kwargs[ORDERING] = tmp if len(tmp) else None
        kwargs.pop(ORDER_SET)
        # Validate: page
        tmp = kwargs[PAGE] if kwargs.get(PAGE) else 0
        kwargs[PAGE] = tmp if 0 < tmp else BASE_SETTINGS.PAGINATION.DEFAULT_START_PAGE_NUMBER
        # Validate: page_size
        tmp = kwargs[PAGE_SIZE] if kwargs.get(PAGE_SIZE) else 0
        kwargs[PAGE_SIZE] = tmp if 0 < tmp else BASE_SETTINGS.PAGINATION.PAGE_SIZE
        super(QueryParams, self).__init__(**kwargs)

    page: int
    page_size: int
    filters: Optional[Dict[str, str]]
    ordering: Optional[List[str]]
    search: Optional[str]
    url: Optional[str]
