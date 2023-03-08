from starlette.status import HTTP_201_CREATED, HTTP_200_OK
from . import APIView as Base


class RetrieverOrCreator(Base):
    expected_status_code = None

    def run(self, input_data: dict):
        self.content, created = self.get_controller.run(input_data=input_data)
        status_code = HTTP_201_CREATED if created else HTTP_200_OK
        self.expected_status_code = self.expected_status_code or status_code
        return self.response()
