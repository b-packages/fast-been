from pydantic import BaseModel
import typing


class Cookie(BaseModel):
    key: str
    value: str = ''
    max_age: typing.Optional[int] = None
    expires: typing.Optional[int] = None
    path: str = '/'
    domain: typing.Optional[str] = None
    secure: bool = False
    httponly: bool = False
