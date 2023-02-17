from fast_been.utils.macros import ControllerType
from fast_been.utils.exceptions.http import (
    LookupFieldIsNotSetHTTPException,
    NotFoundHTTPException,
)

from . import Base


class Retriever(Base):

    def __init__(self, **kwargs):
        self.__lookup_field = kwargs.get('lookup_field')
        if self.__lookup_field is None:
            raise LookupFieldIsNotSetHTTPException()

    def run(self):
        return self.retrieve(self.__lookup_field)

    def retrieve(self, lookup_field):
        obj_ = self.retrieve_data(**{self.lookup_field_name: lookup_field})
        if not obj_:
            raise NotFoundHTTPException()
        outputs_ = self.output_data(**obj_.to_dict())
        return outputs_

    @property
    def controller_type(self):
        return ControllerType.retriever()
