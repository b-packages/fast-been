from pydantic import BaseModel
from typing import Optional, List, Dict

from fast_been.conf.base_settings import BASE_SETTINGS

FILTERS = 'filters'
FILTER_SET = 'filter_set'
ORDERING = 'ordering'
ORDER_SET = 'order_set'


class QueryParams(BaseModel):
    def __init__(self, **kwargs):
        kwargs[FILTERS] = kwargs[FILTERS] if kwargs.get(FILTER_SET) else {}
        tmp = {}
        for k, v in kwargs[FILTERS].items():
            if k in kwargs[FILTER_SET]:
                tmp[k] = v
        kwargs[FILTERS] = tmp if len(tmp) else None
        kwargs.pop(FILTER_SET)

        kwargs[ORDERING] = kwargs[ORDERING] if kwargs.get(ORDER_SET) else []
        tmp = []
        for i in kwargs[ORDERING]:
            if i in kwargs[ORDER_SET]:
                tmp.append(i)
        kwargs[ORDERING] = tmp if len(tmp) else None
        kwargs.pop(ORDER_SET)
        super(QueryParams, self).__init__(**kwargs)

    page: int = BASE_SETTINGS.PAGINATION.DEFAULT_START_PAGE_NUMBER
    page_size: int = BASE_SETTINGS.PAGINATION.PAGE_SIZE
    filters: Optional[Dict[str]]
    ordering: Optional[List[str]]
    search: Optional[str]
