from fast_been.utils.macros import ControllerType
from fast_been.utils.exceptions.http import (
    LookupFieldIsNotSetHTTPException,
    ThereIsNoInputDataToRegisterHTTPException,
    NotFoundHTTPException,
)

from . import Base


class Updater(Base):

    def __init__(self, **kwargs):
        self.__lookup_field = kwargs.get('lookup_field')
        if self.__lookup_field is None:
            raise LookupFieldIsNotSetHTTPException()
        self.__input_data = kwargs.get('input_data')
        if self.__input_data is None:
            raise ThereIsNoInputDataToRegisterHTTPException()

    def run(self, **kwargs):
        return self.update(self.__lookup_field, self.__input_data)

    def update(self, lookup_field, input_data):
        input_ = self.input_data(**input_data)
        obj_ = self.update_data(lookup_field, **input_)
        if obj_ is None:
            raise NotFoundHTTPException()
        output_ = self.output_data(**obj_.to_dict())
        return output_

    @property
    def controller_type(self):
        return ControllerType.updater()
