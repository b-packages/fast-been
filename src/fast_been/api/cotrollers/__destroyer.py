from fast_been.utils.macros import ControllerType
from fast_been.utils.exceptions.http import (
    LookupFieldIsNotSetHTTPException,
    NotFoundHTTPException,
)

from . import APIController as Base
from .__macros import LOOKUP_FIELD as LOOKUP_FIELD_MACRO


class Destroyer(Base):

    def __init__(self, **kwargs):
        self.__lookup_field = kwargs.get(LOOKUP_FIELD_MACRO)
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
