from starlette.status import HTTP_204_NO_CONTENT
from . import APIView as Base


class Destroyer(Base):
    expected_status_code = HTTP_204_NO_CONTENT
