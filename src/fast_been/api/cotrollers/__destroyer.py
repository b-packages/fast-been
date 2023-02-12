from fast_been.utils.macros import ControllerType
from fast_been.utils.exceptions.http import LookupFieldIsNotSetHTTPException, NotFoundHTTPException

from . import Base


class Destroyer(Base):
    def run(self, **kwargs):
        lookup_field = kwargs.get('lookup_field')
        if lookup_field is None:
            raise LookupFieldIsNotSetHTTPException()
        return self.destroy(lookup_field)

    def destroy(self, lookup_field):
        obj = self.destroy_data(lookup_field)
        if obj is None:
            raise NotFoundHTTPException()

    @property
    def controller_type(self):
        return ControllerType.destroyer()
