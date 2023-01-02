from .__base import Base


class Updater(Base):
    def run(self, lookup_field, data: dict):
        return self.update(lookup_field, data)

    def update(self, lookup_field, data):
        old_instance_ = self.retrieve_data(**{self.lookup_field_name: lookup_field})
        if not old_instance_:
            return None
        self.destroy_data(**{self.lookup_field_name: lookup_field})
        old_data_ = old_instance_.to_dict()
        input_ = self.input_data(**data)
        data_ = old_data_.update(input_)
        instance_ = self.create_data(**data_)
        output_ = self.output_data(**instance_.to_dict())
        return output_
