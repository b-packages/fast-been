from abc import ABC, abstractmethod
from typing import Optional
from starlette.responses import Response, JSONResponse
from starlette.status import HTTP_200_OK
from starlette.requests import Request

from fast_been.conf.base_settings import BASE_SETTINGS

JWT_SECRET_KEY = BASE_SETTINGS.JWT.SECRET_KEY
JWT_ALGORITHM = BASE_SETTINGS.JWT.ALGORITHM


class Base(ABC):
    controller_class = None
    expected_status_code = HTTP_200_OK
    content = None

    def __init__(self, request: Optional[Request], response: Optional[Response]):
        self.request = request
        self.response = response

    @abstractmethod
    def run(self, **kwargs):
        pass

    __controller_instance = None

    @property
    def get_controller(self):
        if self.__controller_instance:
            return self.__controller_instance
        self.__controller_instance = self.controller_class()
        return self.__controller_instance

    def just_response(self):
        response = JSONResponse if self.content else Response
        rslt = response(
            status_code=self.expected_status_code,
            content=self.content,
        )
        return rslt
