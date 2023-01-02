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

    def run(self, request: Request, lookup_field=None, input_data=None):
        try:
            if not self.__is_login_check(request):
                return self.response
            func = self.func_method(request.method.lower())
            func(
                input_data=input_data,
                lookup_field=lookup_field,
                page=request.query_params.get('page'),
                page_size=request.query_params.get('page_size'),
                filters=request.query_params.get('filters'),
                ordering=request.query_params.get('ordering'),
                search=request.query_params.get('search')
            )
            return self.response
        except HTTPException as exp:
            return exp

    def get(self, lookup_field, page, page_size, filters, ordering, search, **kwargs):
        output = self.controller.run(
            lookup_field=lookup_field, page=page, page_size=page_size,
            filters=filters, ordering=ordering, search=search)
        if output:
            self.response.status_code = 200
            self.response.body = self.response.render(output)
        else:
            self.response.status_code = 404

    def post(self, input_data: dict, **kwargs):
        output = self.controller.run(data=input_data)
        self.response.status_code = 201
        self.response.body = self.response.render(output)

    def put(self, lookup_field, input_data, **kwargs):
        output = self.controller.run(
            lookup_field=lookup_field, data=input_data)
        if output:
            self.response.status_code = 200
            self.response.body = self.response.render(output)
        else:
            self.response.status_code = 404

    def patch(self, lookup_field, input_data, **kwargs):
        output = self.controller.run(
            lookup_field=lookup_field, data=input_data)
        if output:
            self.response.status_code = 200
            self.response.body = self.response.render(output)
        else:
            self.response.status_code = 404

    def delete(self, lookup_field, **kwargs):
        output = self.controller.run(lookup_field=lookup_field)
        if output:
            self.response.status_code = 204
        else:
            self.response.status_code = 404

    def __method_not_allowed(self, **kwargs):
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
