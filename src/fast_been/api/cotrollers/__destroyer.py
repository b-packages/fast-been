from fast_been.utils.exceptions.http import (
    LookupFieldIsNotSetHTTPException,
    NotFoundHTTPException,
)
from fast_been.utils.macros import ControllerType
from . import APIController as Base


class Destroyer(Base):

    def __init__(self, lookup_field, **kwargs):
        self.__lookup_field = lookup_field
        if self.__lookup_field is None:
            raise LookupFieldIsNotSetHTTPException()

    def run(self):
        return self.destroy()

    def destroy(self):
        obj = self.destroy_data(self.__lookup_field)
        if obj is None:
            raise NotFoundHTTPException()

    @property
    def controller_type(self):
        return ControllerType.destroyer()
