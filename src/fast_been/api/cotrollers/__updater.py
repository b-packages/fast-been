from .__base import Base


class Updater(Base):
    def run(self, **kwargs):
        lookup_field = kwargs.get('lookup_field')
        input_data = kwargs.get('input_data')
        if lookup_field is None or input_data is None:
            return None
        return self.update(lookup_field, input_data)

    def update(self, lookup_field, input_data):
        old_instance_ = self.retrieve_data(**{self.lookup_field_name: lookup_field})
        if not old_instance_:
            return None
        self.destroy_data(**{self.lookup_field_name: lookup_field})
        old_data_ = old_instance_.to_dict()
        input_ = self.input_data(**input_data)
        data_ = old_data_.update(input_)
        instance_ = self.create_data(**data_)
        output_ = self.output_data(**instance_.to_dict())
        return output_
