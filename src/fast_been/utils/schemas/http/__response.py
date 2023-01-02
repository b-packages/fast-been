from pydantic import BaseModel
import typing


class SetCookie(BaseModel):
    key: str
    value: str = ''
    max_age: typing.Optional[int] = None
    expires: typing.Optional[int] = None
    path: str = '/'
    domain: typing.Optional[str] = None
    secure: bool = False
    httponly: bool = False


class Response(BaseModel):
    content: typing.Any = None
    status_code: int = 200
    headers: typing.Optional[typing.Mapping[str, str]] = None
    media_type: typing.Optional[str] = None
    background: typing.Any = None
    set_cookies: typing.List[SetCookie] = []
