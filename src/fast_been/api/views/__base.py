from datetime import datetime
from jose import jwt

from fastapi.responses import JSONResponse
from fastapi import Request, HTTPException

from fast_been.utils.http.response.status.code import OK, BAD_REQUEST, CREATED, NO_CONTENT, UNAUTHORIZED
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
    controller_class = None
    expected_status_code = None
    need_authentication = False
    response: FastBeenResponse = FastBeenResponse()

    def run(self, **kwargs):
        try:
            self.__request_setter(**kwargs)
            if not self.__does_it_have_access():
                return self.get_response()
            rslt = self.__get_controller.run(**self.__request.dict())
            self.__set_response_status_code(self.expected_status_code if rslt else BAD_REQUEST)
            self.__set_response_content(rslt)
            return self.get_response()
        except HTTPException as exp:
            return exp

    def get_response(self):
        rslt = JSONResponse(
            status_code=self.response.status_code,
            content=self.response.content,
            headers=self.response.headers,
            media_type=self.response.media_type,
            background=self.response.background,
        )
        for c in self.response.cookies:
            rslt.set_cookie(**c.dict())
        return rslt

    def set_access_token(self, pid: str, data: dict):
        self.__set_cookie(
            {
                'key': 'Authorization',
                'value': access_token(pid=pid, data=data),
                'secure': False,
                'httponly': True,
            }
        )

    def delete_access_token(self):
        self.__delete_cookie('Authorization')

    __controller_instance = None
    __request: FastBeenRequest = FastBeenRequest()

    @property
    def __get_controller(self):
        if self.__controller_instance:
            return self.__controller_instance
        self.__controller_instance = self.controller_class()
        return self.__controller_instance

    @property
    def __expected_status_code(self):
        return self.expected_status_code or self.__get_controller.controller_type or OK

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

    def __set_response_status_code(self, value):
        self.response.status_code = value

    def __set_response_content(self, value):
        self.response.content = value

    def __set_response_headers(self, value):
        self.response.headers = value

    def __set_response_media_type(self, value):
        self.response.media_type = value

    def __set_response_background(self, value):
        self.response.background = value

    def __does_it_have_access(self):
        request: Request = self.__request.base_request
        if not self.need_authentication:
            return True
        if 'Authorization' not in request.cookies:
            self.response.status_code = UNAUTHORIZED
            return False
        token_decoded = jwt.decode(
            request.cookies['Authorization'],
            key=JWT_SECRET_KEY,
            algorithms=JWT_ALGORITHM,
        )
        if token_decoded is None:
            self.response.status_code = UNAUTHORIZED
            return False
        if datetime.utcfromtimestamp(token_decoded['exp']) < now():
            self.response.status_code = UNAUTHORIZED
            return False
        self.__request.beanser_pid = token_decoded['sub']
        self.set_access_token(pid=token_decoded['sub'], data=token_decoded['data'])
        return True

    def __set_cookie(self, value: dict):
        self.response.cookies.append(FastBeenCookie(**value))

    def __delete_cookie(self, key):
        for i, c in enumerate(self.response.cookies):
            if c.key == key:
                self.response.cookies.pop(i)
                return
