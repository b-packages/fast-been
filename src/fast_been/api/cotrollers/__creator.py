from .__base import Base


class Creator(Base):

    def run(self, **kwargs):
        input_data = kwargs.get('input_data')
        if input_data is None:
            return None
        return self.create(input_data)

    def create(self, input_data: dict):
        input_ = self.input_data(**input_data)
        instance_ = self.create_data(**input_)
        output_ = self.output_data(**instance_.to_dict())
        return output_
