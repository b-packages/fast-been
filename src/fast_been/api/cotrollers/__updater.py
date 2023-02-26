from fast_been.utils.exceptions.http import (
    LookupFieldIsNotSetHTTPException,
    ThereIsNoInputDataToRegisterHTTPException,
    NotFoundHTTPException,
)
from . import APIController as Base


class Updater(Base):

    def __init__(self):
        self.__input_data = None
        self.__lookup_field = None

    def run(self, lookup_field, input_data) -> dict:
        self.__lookup_field = lookup_field
        if self.__lookup_field is None:
            raise LookupFieldIsNotSetHTTPException()
        self.__input_data = input_data
        if self.__input_data is None:
            raise ThereIsNoInputDataToRegisterHTTPException()
        return self.update()

    def update(self) -> dict:
        input_ = self.input_data(**self.__input_data)
        obj_ = self.update_data(self.__lookup_field, **input_)
        if obj_ is None:
            raise NotFoundHTTPException()
        output_ = self.output_data(**obj_.to_dict())
        return output_

    @property
    def controller_type(self) -> str:
        return 'UPDATER'
