from fast_been.utils.http.response.status.code import NO_CONTENT

from . import Base


class Destroyer(Base):
    expected_status_code = NO_CONTENT
