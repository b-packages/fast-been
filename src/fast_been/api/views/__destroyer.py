from starlette.status import HTTP_204_NO_CONTENT
from . import APIView as Base


class Destroyer(Base):
    expected_status_code = HTTP_204_NO_CONTENT

    def run(self, lookup_field):
        self.content = self.get_controller.run(lookup_field=lookup_field)
        return self.response()
