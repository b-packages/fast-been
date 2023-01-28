from fast_been.utils.macros import ControllerType

from . import Base


class Destroyer(Base):
    def run(self, **kwargs):
        lookup_field = kwargs.get('lookup_field')
        if lookup_field is None:
            return None
        return self.destroy(lookup_field)

    def destroy(self, lookup_field):
        obj = self.destroy_data(lookup_field)
        if obj is None:
            return False
        return True

    @property
    def controller_type(self):
        return ControllerType.destroyer()
