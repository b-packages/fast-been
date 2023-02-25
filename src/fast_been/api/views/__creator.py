from starlette.status import HTTP_201_CREATED
from . import APIView as Base


class Creator(Base):
    expected_status_code = HTTP_201_CREATED
