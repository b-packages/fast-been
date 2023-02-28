from fast_been.utils.exceptions.http import (
    LookupFieldIsNotSetHTTPException,
    ThereIsNoInputDataToRegisterHTTPException,
    NotFoundHTTPException,
)
from . import APIController as Base


class Updater(Base):
    __input_data = None

    def run(self, lookup_fields, input_data) -> dict:
        self.lookup_fields = lookup_fields
        if not len(self.lookup_fields):
            raise LookupFieldIsNotSetHTTPException()
        self.__input_data = input_data
        if self.__input_data is None:
            raise ThereIsNoInputDataToRegisterHTTPException()
        return self.update()

    def update(self) -> dict:
        input_ = self.input_data(**self.__input_data)
        obj_ = self.update_data(**input_)
        if obj_ is None:
            raise NotFoundHTTPException()
        output_ = self.output_data(**obj_.to_dict())
        return output_

    @property
    def controller_type(self) -> str:
        return 'UPDATER'
