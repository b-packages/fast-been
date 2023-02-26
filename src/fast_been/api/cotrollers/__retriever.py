from fast_been.utils.exceptions.http import (
    LookupFieldIsNotSetHTTPException,
    NotFoundHTTPException,
)
from . import APIController as Base


class Retriever(Base):

    def __init__(self):
        self.__lookup_field = None

    def run(self, lookup_field) -> dict:
        self.__lookup_field = lookup_field
        if self.__lookup_field is None:
            raise LookupFieldIsNotSetHTTPException()
        return self.retrieve()

    def retrieve(self) -> dict:
        obj_ = self.retrieve_data(**{self.lookup_field_name: self.__lookup_field})
        if not obj_:
            raise NotFoundHTTPException()
        outputs_ = self.output_data(**obj_.to_dict())
        return outputs_

    @property
    def controller_type(self) -> str:
        return 'RETRIEVER'
