from fast_been.utils.http.response.status.code import CREATED

from . import Base


class Creator(Base):
    expected_status_code = CREATED