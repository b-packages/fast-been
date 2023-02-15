from fast_been.utils.http.response.status.code import NO_CONTENT
from fastapi.responses import JSONResponse

from . import Base


class Destroyer(Base):
    expected_status_code = NO_CONTENT

    def get_response(self):
        # rslt = JSONResponse(
        #     status_code=self.response.status_code,
        #     content=self.response.content,
        #     headers=self.response.headers,
        #     media_type=self.response.media_type,
        #     background=self.response.background,
        # )
        # for c in self.response.cookies:
        #     rslt.set_cookie(**c.dict())
        return None
