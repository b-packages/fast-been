from fast_been.utils.macros import ControllerType

from . import Base


class Updater(Base):
    def run(self, **kwargs):
        lookup_field = kwargs.get('lookup_field')
        input_data = kwargs.get('input_data')
        if lookup_field is None or input_data is None:
            return None
        return self.update(lookup_field, input_data)

    def update(self, lookup_field, input_data):
        input_ = self.input_data(**input_data)
        obj_ = self.update_data(lookup_field, **input_)
        if obj_ is None:
            return None
        output_ = self.output_data(**obj_.to_dict())
        return output_

    @property
    def controller_type(self):
        return ControllerType.updater()
