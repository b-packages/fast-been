from .__base import __Base


class Retriever(__Base):

    def run(self, lookup_field):
        return self.retrieve(lookup_field)

    def retrieve(self, lookup_field):
        instance_ = self.__retrieve(**{self.lookup_field_name: lookup_field})
        outputs_ = self.__output(**instance_.to_dict())
        return outputs_
