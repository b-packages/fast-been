from datetime import datetime
from jose import jwt

from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException

from fast_been.utils.http.response.status.code import OK, BAD_REQUEST, CREATED, NO_CONTENT
from fast_been.conf.base_settings import BASE_SETTINGS
from fast_been.utils.generators.auth.jwt import access_token
from fast_been.utils.macros import ControllerType
from fast_been.utils.schemas.http import (
    Request as FastBeenRequest,
    Response as FastBeenResponse,
    Cookie as FastBeenCookie,
)
from fast_been.utils.date_time import now

JWT_SECRET_KEY = BASE_SETTINGS.JWT.SECRET_KEY
JWT_ALGORITHM = BASE_SETTINGS.JWT.ALGORITHM


class Base:
    def run(self, **kwargs):
        try:
            self.__request_setter(**kwargs)
            self.__does_it_have_access()
            rslt = self.__get_controller.run(**self.__request.dict())
            self.__set_response_status_code(self.expected_status_code if rslt else BAD_REQUEST)
            self.__set_response_content(rslt)
            return self.__response
        except HTTPException as exp:
            return exp

    controller_class = None

    __controller_instance = None

    @property
    def __get_controller(self):
        if self.__controller_instance:
            return self.__controller_instance
        self.__controller_instance = self.controller_class()
        return self.__controller_instance

    expected_status_code = None

    @property
    def __expected_status_code(self):
        return self.expected_status_code or self.__get_controller.controller_type or OK

    __request: FastBeenRequest = FastBeenRequest()

    def __request_setter(self, **kwargs):
        self.__request.decoder(**kwargs)

    @staticmethod
    def __default_status_code_controller(value):
        mapper = {
            ControllerType.creator: CREATED,
            ControllerType.destroyer: NO_CONTENT,
            ControllerType.lister: OK,
            ControllerType.retriever: OK,
            ControllerType.updater: OK,
        }
        if value in mapper:
            return mapper[value]
        return None

    __response_: FastBeenResponse = FastBeenResponse()

    @property
    def __response(self):
        rslt = JSONResponse(
            status_code=self.__response_.status_code,
            content=self.__response_.content,
            headers=self.__response_.headers,
            media_type=self.__response_.media_type,
            background=self.__response_.background,
        )
        for c in self.__response_.cookies:
            rslt.set_cookie(**c.dict())
        return rslt

    def __set_response_status_code(self, value):
        self.__response_.status_code = value

    def __set_response_content(self, value):
        self.__response_.content = value

    def __set_response_headers(self, value):
        self.__response_.headers = value

    def __set_response_media_type(self, value):
        self.__response_.media_type = value

    def __set_response_background(self, value):
        self.__response_.background = value

    def __set_response_cookie(self, value: dict):
        self.__response_.cookies.append(FastBeenCookie(**value))

    need_authentication = False

    def __does_it_have_access(self):
        request: Request = self.__request.base_request
        if not self.need_authentication:
            return True
        if 'Authorization' not in request.cookies:
            return False
        token_decoded = jwt.decode(
            request.cookies['Authorization'],
            key=JWT_SECRET_KEY,
            algorithms=JWT_ALGORITHM,
        )
        if token_decoded is None:
            return False
        if datetime.utcfromtimestamp(token_decoded['exp']) < now():
            return False
        self.__request.beanser_pid = token_decoded['sub']
        self.__set_response_cookie(
            {
                'key': 'Authorization',
                'value': access_token(pid=token_decoded['sub']),
                'secure': False,
                'httponly': True,
            }
        )
        return True