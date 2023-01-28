from fast_been.utils.macros import ControllerType
from fast_been.utils.exceptions.http import (
    LookupFieldIsNotSetHTTPException,
    ThereIsNoInputDataToRegisterHTTPException,
    NotFoundHTTPException,
)

from . import Base


class Updater(Base):
    def run(self, **kwargs):
        lookup_field = kwargs.get('lookup_field')
        if lookup_field is None:
            raise LookupFieldIsNotSetHTTPException()
        input_data = kwargs.get('input_data')
        if input_data is None:
            raise ThereIsNoInputDataToRegisterHTTPException()
        return self.update(lookup_field, input_data)

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
