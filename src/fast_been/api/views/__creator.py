from starlette.status import HTTP_201_CREATED
from . import APIView as Base


class Creator(Base):
    expected_status_code = HTTP_201_CREATED

    def run(self, input_data: dict):
        self.content = self.get_controller.run(input_data=input_data)
        return self.just_response()
