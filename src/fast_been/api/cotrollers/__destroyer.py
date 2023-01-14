from fast_been.utils.macros import ControllerType

from . import Base


class Destroyer(Base):
    def run(self, **kwargs):
        lookup_field = kwargs.get('lookup_field')
        if lookup_field is None:
            return None
        return self.destroy(lookup_field)

    def destroy(self, lookup_field):
        return self.destroy_data(**{self.lookup_field_name: lookup_field})

    @property
    def controller_type(self):
        return ControllerType.destroyer()
