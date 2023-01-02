from ._base import Base


class Retriever(Base):

    def run(self, lookup_field):
        return self.retrieve(lookup_field)

    def retrieve(self, lookup_field):
        instance_ = self.retrieve_data(**{self.lookup_field_name: lookup_field})
        outputs_ = self.output_data(**instance_.to_dict())
        return outputs_
