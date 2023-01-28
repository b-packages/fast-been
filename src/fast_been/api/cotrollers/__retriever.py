from fast_been.utils.macros import ControllerType
from fast_been.utils.exceptions.http import LookupFieldIsNotSetHTTPException, NotFoundHTTPException

from . import Base


class Retriever(Base):

    def run(self, **kwargs):
        lookup_field = kwargs.get('lookup_field')
        if lookup_field is None:
            raise LookupFieldIsNotSetHTTPException()
        return self.retrieve(lookup_field)

    def retrieve(self, lookup_field):
        obj_ = self.retrieve_data(**{self.lookup_field_name: lookup_field})
        if not obj_:
            raise NotFoundHTTPException()
        outputs_ = self.output_data(**obj_.to_dict())
        return outputs_

    @property
    def controller_type(self):
        return ControllerType.retriever()
