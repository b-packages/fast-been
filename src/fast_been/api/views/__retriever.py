from . import APIView as Base


class Retriever(Base):
    def run(self, lookup_field):
        self.content = self.get_controller.run(lookup_field=lookup_field)
        return self.just_response()
