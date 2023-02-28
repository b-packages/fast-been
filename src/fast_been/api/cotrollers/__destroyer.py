from fast_been.utils.exceptions.http import (
    LookupFieldIsNotSetHTTPException,
    NotFoundHTTPException,
)
from . import APIController as Base


class Destroyer(Base):

    def run(self, lookup_fields: dict) -> None:
        self.lookup_fields = lookup_fields
        if not len(self.lookup_fields):
            raise LookupFieldIsNotSetHTTPException()
        return self.destroy()

    def destroy(self) -> None:
        obj = self.destroy_data()
        if obj is None:
            raise NotFoundHTTPException()

    @property
    def controller_type(self) -> str:
        return 'DESTROYER'
