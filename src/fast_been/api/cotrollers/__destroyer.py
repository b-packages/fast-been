from fast_been.utils.macros import ControllerType
from fast_been.utils.exceptions.http import (
    LookupFieldIsNotSetHTTPException,
    NotFoundHTTPException,
)

from . import Base


class Destroyer(Base):

    def __init__(self, **kwargs):
        self.__lookup_field = kwargs.get('lookup_field')
        if self.__lookup_field is None:
            raise LookupFieldIsNotSetHTTPException()

    def run(self):
        return self.destroy(self.__lookup_field)

    def destroy(self, lookup_field):
        obj = self.destroy_data(lookup_field)
        if obj is None:
            raise NotFoundHTTPException()

    @property
    def controller_type(self):
        return ControllerType.destroyer()
