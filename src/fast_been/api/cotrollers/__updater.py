from .__base import __Base


class Updater(__Base):
    def run(self, lookup_field, data: dict):
        return self.update(lookup_field, data)

    def update(self, lookup_field, data):
        old_instance_ = self.__retrieve(**{self.lookup_field_name: lookup_field})
        if not old_instance_:
            return None
        self.__destroy(**{self.lookup_field_name: lookup_field})
        old_data_ = old_instance_.to_dict()
        input_ = self.__input(**data)
        data_ = old_data_.update(input_)
        instance_ = self.__create(**data_)
        output_ = self.__output(**instance_.to_dict())
        return output_
