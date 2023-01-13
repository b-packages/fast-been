from pydantic import BaseModel
import typing
from . import Cookie


class Response(BaseModel):
    content: typing.Any = None
    status_code: typing.Optional[int] = None
    headers: typing.Optional[typing.Mapping[str, str]] = None
    media_type: typing.Optional[str] = None
    background: typing.Any = None
    cookies: typing.List[Cookie] = []
