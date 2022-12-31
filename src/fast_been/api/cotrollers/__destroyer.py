from .__base import __Base


class Destroyer(__Base):
    def run(self, lookup_field):
        return self.destroy(lookup_field)

    def destroy(self, lookup_field):
        return self.__destroy(**{self.lookup_field_name: lookup_field})
