from .__base import __Base


class Creator(__Base):

    def run(self, data: dict):
        return self.create(data)

    def create(self, data: dict):
        input_ = self.__input(**data)
        instance_ = self.__create(**input_)
        output_ = self.__output(**instance_)
        return output_
