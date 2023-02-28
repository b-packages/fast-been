from fast_been.utils.exceptions.http import (
    LookupFieldIsNotSetHTTPException,
    NotFoundHTTPException,
)
from . import APIController as Base


class Retriever(Base):

    def run(self, lookup_fields) -> dict:
        self.lookup_fields = lookup_fields
        if not len(self.lookup_fields):
            raise LookupFieldIsNotSetHTTPException()
        return self.retrieve()

    def retrieve(self) -> dict:
        obj_ = self.retrieve_data()
        if not obj_:
            raise NotFoundHTTPException()
        outputs_ = self.output_data(**obj_.to_dict())
        return outputs_

    @property
    def controller_type(self) -> str:
        return 'RETRIEVER'
