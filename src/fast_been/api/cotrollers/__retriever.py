from fast_been.utils.exceptions.http import (
    LookupFieldIsNotSetHTTPException,
    NotFoundHTTPException,
)
from fast_been.utils.macros import ControllerType
from . import APIController as Base


class Retriever(Base):

    def __init__(self, lookup_field):
        self.__lookup_field = lookup_field
        if self.__lookup_field is None:
            raise LookupFieldIsNotSetHTTPException()

    def run(self):
        return self.retrieve()

    def retrieve(self):
        obj_ = self.retrieve_data(**{self.lookup_field_name: self.__lookup_field})
        if not obj_:
            raise NotFoundHTTPException()
        outputs_ = self.output_data(**obj_.to_dict())
        return outputs_

    @property
    def controller_type(self):
        return ControllerType.retriever()
