from datetime import datetime
from jose import jwt
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse

from fast_been.conf.base_settings import BASE_SETTINGS
from fast_been.utils.date_time import now
from fast_been.utils.generators.auth.jwt import access_token
from fast_been.utils.schemas.http import Response as FastBeenResponse

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
    __response: FastBeenResponse = FastBeenResponse()

    def __init__(self, controller_class, methods=None, is_login=False):
        self.__controller_class = controller_class
        self.__methods = methods
        self.__is_login = is_login

    def run(self, request: Request, lookup_field=None, input_data=None):
        try:
            if not self.__is_login_check(request):
                return self.http_response
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
            return self.http_response
        except HTTPException as exp:
            return exp

    def get(self, lookup_field, page, page_size, filters, ordering, search, **kwargs):
        output = self.controller.run(
            lookup_field=lookup_field, page=page, page_size=page_size,
            filters=filters, ordering=ordering, search=search)
        if output:
            self.__response.status_code = 200
            self.__response.content = output
        else:
            self.__response.status_code = 404

    def post(self, input_data: dict, **kwargs):
        output = self.controller.run(data=input_data)
        self.__response.status_code = 201
        self.__response.content = output

    def put(self, lookup_field, input_data, **kwargs):
        output = self.controller.run(
            lookup_field=lookup_field, data=input_data)
        if output:
            self.__response.status_code = 200
            self.__response.content = output
        else:
            self.__response.status_code = 404

    def patch(self, lookup_field, input_data, **kwargs):
        output = self.controller.run(
            lookup_field=lookup_field, data=input_data)
        if output:
            self.__response.status_code = 200
            self.__response.content = output
        else:
            self.__response.status_code = 404

    def delete(self, lookup_field, **kwargs):
        output = self.controller.run(lookup_field=lookup_field)
        if output:
            self.__response.status_code = 204
        else:
            self.__response.status_code = 404

    def __method_not_allowed(self, **kwargs):
        self.__response.status_code = 405

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
    def http_response(self):
        rslt = JSONResponse(
            status_code=self.__response.status_code,
            content=self.__response.content,
            headers=self.__response.headers,
            media_type=self.__response.media_type,
            background=self.__response.background,
        )
        for c in self.__response.set_cookies:
            rslt.set_cookie(**c.dict())
        return rslt

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
        self.__response.set_cookies.append(
            **{
                'key': 'Authorization',
                'value': access_token(pid=token_decoded['sub']),
                'secure': False,
                'httponly': True,
            }
        )
        return True
