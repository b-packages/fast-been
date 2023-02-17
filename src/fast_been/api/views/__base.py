from datetime import datetime
from jose import jwt

from fastapi.responses import JSONResponse, Response
from fastapi import Request

from fast_been.utils.generators.auth.jwt import access_token
from fast_been.utils.http.response.status.code import (
    OK as OK_HTTP_STATUS_CODE,
)
from fast_been.conf.base_settings import BASE_SETTINGS
from fast_been.__macros import (
    WWW_AUTHORIZATION as WWW_AUTHORIZATION_MACRO,
    VALUE as VALUE_MACRO,
    SECURE as SECURE_MACRO,
    HTTPONLY as HTTPONLY_MACRO,
    KEY as KEY_MACRO,
    EXP as EXP_MACRO,
    SUB as SUB_MACRO,
    DATA as DATA_MACRO,
)
from fast_been.utils.exceptions.http import (
    LoginRequiredHTTPException,
    TokenIsNotAcceptedHTTPException,
    TokenHasExpiredHTTPException,
)
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
    expected_status_code = OK_HTTP_STATUS_CODE
    need_authentication = False

    def __init__(self, **kwargs):
        self.__set_request(**kwargs)
        self.__access_checked()

    request: FastBeenRequest

    def __set_request(self, **kwargs):
        self.request = FastBeenRequest(**kwargs)

    def __access_checked(self):
        if not self.need_authentication:
            return
        request: Request = self.request.base_request
        if WWW_AUTHORIZATION_MACRO not in request.cookies:
            raise LoginRequiredHTTPException()
        token_decoded = jwt.decode(
            request.cookies[WWW_AUTHORIZATION_MACRO],
            key=JWT_SECRET_KEY,
            algorithms=JWT_ALGORITHM,
        )
        if token_decoded is None:
            raise TokenIsNotAcceptedHTTPException()
        if datetime.utcfromtimestamp(token_decoded[EXP_MACRO]) < now():
            raise TokenHasExpiredHTTPException()
        self.request.beanser_pid = token_decoded[SUB_MACRO]
        self.set_access_token(pid=token_decoded[SUB_MACRO], data=token_decoded[DATA_MACRO])

    def set_access_token(self, pid: str, data: dict):
        self.set_cookie(
            {
                KEY_MACRO: WWW_AUTHORIZATION_MACRO,
                VALUE_MACRO: access_token(pid=pid, data=data),
                SECURE_MACRO: False,
                HTTPONLY_MACRO: True,
            }
        )

    def delete_access_token(self):
        self.delete_cookie(WWW_AUTHORIZATION_MACRO)

    def set_cookie(self, value: dict):
        self.__response.cookies.append(FastBeenCookie(**value))

    def delete_cookie(self, key):
        for i, c in enumerate(self.__response.cookies):
            if c.key == key:
                self.__response.cookies.pop(i)
                return

    def run(self):
        rslt = self.get_controller.run()
        self.set_response_content(rslt)
        return self.response

    __controller_instance = None

    @property
    def get_controller(self):
        if self.__controller_instance:
            return self.__controller_instance
        self.__controller_instance = self.controller_class(**self.request.dict())
        return self.__controller_instance

    __response: FastBeenResponse = FastBeenResponse()

    @property
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

    def set_response_status_code(self, value):
        self.__response.status_code = value

    def set_response_content(self, value):
        self.__response.content = value

    def set_response_headers(self, value):
        self.__response.headers = value

    def set_response_media_type(self, value):
        self.__response.media_type = value

    def set_response_background(self, value):
        self.__response.background = value
