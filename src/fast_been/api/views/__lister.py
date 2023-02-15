from fast_been.utils.http.response.status.code import OK

from . import Base


class Lister(Base):
    expected_status_code = OK
