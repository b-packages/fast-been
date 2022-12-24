from .__base import __Base


class Getter(__Base):

    def run(self, **kwargs):
        tmp = self.__get(**kwargs)
        if tmp is None:
            return None
        self.validate_data(**tmp.to_dict())
        return self.output()

    def __get(self, **kwargs):
        return self.queryset.filter(**kwargs).first()
