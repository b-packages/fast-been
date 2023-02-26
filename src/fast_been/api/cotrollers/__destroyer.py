from fast_been.utils.exceptions.http import (
    LookupFieldIsNotSetHTTPException,
    NotFoundHTTPException,
)
from . import APIController as Base


class Destroyer(Base):

    def __init__(self):
        self.__lookup_field = None

    def run(self, lookup_field) -> None:
        self.__lookup_field = lookup_field
        if self.__lookup_field is None:
            raise LookupFieldIsNotSetHTTPException()
        return self.destroy()

    def destroy(self) -> None:
        obj = self.destroy_data(self.__lookup_field)
        if obj is None:
            raise NotFoundHTTPException()

    @property
    def controller_type(self) -> str:
        return 'DESTROYER'
