from fast_been.utils.macros import ControllerType
from fast_been.utils.exceptions.http import ThereIsNoInputDataToRegisterHTTPException

from . import Base


class Creator(Base):
    instance = None

    def run(self, **kwargs):
        input_data = kwargs.get('input_data')
        if input_data is None:
            raise ThereIsNoInputDataToRegisterHTTPException()
        return self.create(input_data)

    def create(self, input_data: dict):
        input_ = self.input_data(**input_data)
        self.instance = self.create_data(**input_)
        output_ = self.output_data(**self.instance.to_dict())
        return output_

    @property
    def controller_type(self):
        return ControllerType.creator()
