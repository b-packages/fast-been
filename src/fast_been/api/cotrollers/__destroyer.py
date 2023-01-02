from ._base import Base


class Destroyer(Base):
    def run(self, lookup_field):
        return self.destroy(lookup_field)

    def destroy(self, lookup_field):
        return self.destroy_data(**{self.lookup_field_name: lookup_field})
