from fast_been.utils.exceptions.http import ThereIsNoInputDataToRegisterHTTPException
from fast_been.utils.macros import ControllerType
from . import APIController as Base


class Creator(Base):

    def __init__(self, input_data):
        self.__input_data = input_data
        if self.__input_data is None:
            raise ThereIsNoInputDataToRegisterHTTPException()
        self.instance = None

    def run(self):
        return self.create()

    def create(self):
        input_ = self.input_data(**self.__input_data)
        self.instance = self.create_data(**input_)
        output_ = self.output_data(**self.instance.to_dict())
        return output_

    @property
    def controller_type(self):
        return ControllerType.creator()
