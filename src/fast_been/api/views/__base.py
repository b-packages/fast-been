from typing import Optional, Any

from fastapi.responses import JSONResponse, Response
from starlette.datastructures import QueryParams
from starlette.requests import Request
from starlette.status import HTTP_200_OK

from fast_been.conf.base_settings import BASE_SETTINGS
from fast_been.utils.schemas.http import (
    Response as FastBeenResponse,
    Cookie as FastBeenCookie,
)

JWT_SECRET_KEY = BASE_SETTINGS.JWT.SECRET_KEY
JWT_ALGORITHM = BASE_SETTINGS.JWT.ALGORITHM


class Base:
    controller_class = None
    expected_status_code = HTTP_200_OK

    def __init__(self, **kwargs):
        self.request: Optional[Request] = kwargs.get('request')
        self.query_params: Optional[QueryParams] = self.request.query_params if self.request else {}
        self.input_data: Optional[dict] = kwargs.get('input_data')
        self.lookup_field: Any = kwargs.get('lookup_field')

    def set_cookie(self, value: dict):
        self.__response.cookies.append(FastBeenCookie(**value))

    def delete_cookie(self, key):
        for i, c in enumerate(self.__response.cookies):
            if c.key == key:
                self.__response.cookies.pop(i)
                return

    def run(self):
        rslt = self.get_controller.run()
        self.__response.content = rslt
        return self.response()

    __controller_instance = None

    @property
    def get_controller(self):
        if self.__controller_instance:
            return self.__controller_instance
        self.__controller_instance = self.controller_class(
            request=self.request, input_data=self.input_data,
            lookup_field=self.lookup_field, query_params=self.query_params)
        return self.__controller_instance

    __response: FastBeenResponse = FastBeenResponse()

    def response(self):
        response = JSONResponse if self.__response.content else Response
        rslt = response(
            status_code=self.__response.status_code or self.expected_status_code,
            content=self.__response.content,
            headers=self.__response.headers,
            media_type=self.__response.media_type,
            background=self.__response.background,
        )
        for c in self.__response.cookies:
            rslt.set_cookie(**c.dict())
        return rslt
