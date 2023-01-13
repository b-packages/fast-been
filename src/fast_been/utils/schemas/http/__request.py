from fastapi import Request as FastAPIRequest
from pydantic import BaseModel
from typing import Any


class Request(BaseModel):
    base_request: FastAPIRequest = None
    input_data: Any = None
    lookup_field: Any = None
    page: Any = None
    page_size: Any = None
    filters: Any = None
    ordering: Any = None
    search: Any = None
    beanser_pid: Any = None

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
