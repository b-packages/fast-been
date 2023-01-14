from pydantic import BaseModel
from typing import Optional, Any


class Request(BaseModel):
    base_request: Any = None
    input_data: Optional[dict] = None
    lookup_field: Any = None
    page: Optional[int] = None
    page_size: Optional[int] = None
    filters: Optional[list] = None
    ordering: Optional[list] = None
    search: Optional[list] = None
    beanser_pid: Optional[str] = None

    def decoder(self, **kwargs):
        _okwargs = dict()
        self.input_data = kwargs.get('input_data')
        self.lookup_field = kwargs.get('lookup_field')
        self.base_request = kwargs.get('request')
        if self.base_request:
            self.page = self.base_request.query_params.get('page')
            self.page_size = self.base_request.query_params.get('page_size')
            self.filters = self.base_request.query_params.get('filters')
            self.ordering = self.base_request.query_params.get('ordering')
            self.search = self.base_request.query_params.get('search')
