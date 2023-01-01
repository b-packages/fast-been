from datetime import datetime
from jose import jwt
from fastapi import Response, Request, HTTPException

from fast_been.conf.base_settings import BASE_SETTINGS
from fast_been.utils.date_time import now
from fast_been.utils.generators.auth.jwt import access_token

JWT_ALGORITHM = BASE_SETTINGS.JWT.ALGORITHM
JWT_SECRET_KEY = BASE_SETTINGS.JWT.SECRET_KEY

GET = 'get'
POST = 'post'
PUT = 'put'
PATCH = 'PATCH'
DELETE = 'delete'


class Base:
    __controller_class = None
    __methods = None
    __is_login: bool = False
    __response: Response = None

    def __init__(self, controller_class, methods=None, is_login=False):
        self.__controller_class = controller_class
        self.__methods = methods
        self.__is_login = is_login

    def run(self, request: Request, lookup_field=None):
        try:
            if not self.__is_login_check(request):
                return self.response
            func = self.func_method(request.method.lower())
            func(lookup_field=lookup_field, query_params=request.query_params, data=request.body())
            return self.response
        except HTTPException as exp:
            return exp

    def get(self, **kwargs):
        output = self.controller.run(**kwargs)
        if output:
            self.response.status_code = 200
            self.response.body = self.response.render(output)
        else:
            self.response.status_code = 404

    def post(self, **kwargs):
        output = self.controller.run(data=kwargs['data'])
        self.response.status_code = 201
        self.response.body = self.response.render(output)

    def put(self, **kwargs):
        output = self.controller.run(
            lookup_field=kwargs['lookup_field'], data=kwargs['data'])
        if output:
            self.response.status_code = 200
            self.response.body = self.response.render(output)
        else:
            self.response.status_code = 404

    def patch(self, **kwargs):
        output = self.controller.run(
            lookup_field=kwargs['lookup_field'], data=kwargs['data'])
        if output:
            self.response.status_code = 200
            self.response.body = self.response.render(output)
        else:
            self.response.status_code = 404

    def delete(self, **kwargs):
        output = self.controller.run(lookup_field=kwargs['lookup_field'])
        if output:
            self.response.status_code = 204
        else:
            self.response.status_code = 404

    def __method_not_allowed(self, request: Request):
        return self.response(status_code=405)

    def func_method(self, method):
        if method not in self.methods:
            return self.__method_not_allowed
        if method == GET:
            return self.get
        if method == POST:
            return self.post
        if method == PUT:
            return self.put
        if method == PATCH:
            return self.patch
        if method == DELETE:
            return self.delete
        return self.__method_not_allowed

    @property
    def methods(self):
        return self.__methods

    @property
    def response(self):
        if self.__response is None:
            self.__response = Response()
        return self.__response

    @property
    def controller(self):
        return self.__controller_class()

    def __is_login_check(self, request: Request):
        if not self.__is_login:
            return True
        if 'Authorization' not in request.cookies:
            return False
        token_decoded = jwt.decode(
            request.cookies['Authorization'],
            key=JWT_SECRET_KEY,
            algorithms=JWT_ALGORITHM,
        )
        if datetime.utcfromtimestamp(token_decoded['exp']) < now():
            return False
        request.scope['beanser_pid'] = token_decoded['sub']
        self.response.set_cookie(
            key='Authorization',
            value=access_token(pid=token_decoded['sub']),
            secure=False,
            httponly=True,
        )
        return True
