from .__base import Base


class Retriever(Base):

    def run(self, **kwargs):
        lookup_field = kwargs.get('lookup_field')
        if lookup_field is None:
            return None
        return self.retrieve(lookup_field)

    def retrieve(self, lookup_field):
        instance_ = self.retrieve_data(**{self.lookup_field_name: lookup_field})
        outputs_ = self.output_data(**instance_.to_dict())
        return outputs_
