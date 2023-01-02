from .__base import Base


class Creator(Base):

    def run(self, data: dict):
        return self.create(data)

    def create(self, data: dict):
        input_ = self.input_data(**data)
        instance_ = self.create_data(**input_)
        output_ = self.output_data(**instance_.to_dict())
        return output_
