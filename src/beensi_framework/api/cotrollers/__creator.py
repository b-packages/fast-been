from .__base import __Base


class Creator(__Base):

    def run(self, data: list | dict, many=False):
        self.validate_data(data, many=many)
        input_data = self.input(many=many)
        return self.__create(input_data, many=many)

    def __create(self, data: list | dict, many=False):
        if not many:
            return self.__create_many_false(data)
        return self.__create_many_true(data)

    def __create_many_false(self, data: dict):
        tmp = self.__create_instance(data)
        self.validate_data(tmp.to_dict())
        return self.output()

    def __create_many_true(self, data: list):
        tmp = []
        for d in data:
            tmp_ = self.__create_instance(d)
            tmp.append(tmp_.to_dict())
        self.validate_data(tmp, many=True)
        return self.output(many=True)

    def __create_instance(self, data: dict):
        instance = self.model(**data)
        instance.__set_pid(data['pid'] if 'pid' in data else None)
        instance.__set_create_datetime()
        instance.__set_is_active()
        instance.__set_hashed()
        self.db.add(instance)
        self.db.commit()
        self.db.referesh(instance)
        return instance
