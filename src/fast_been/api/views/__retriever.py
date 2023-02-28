from . import APIView as Base


class Retriever(Base):
    def run(self, lookup_fields):
        self.content = self.get_controller.run(lookup_fields=lookup_fields)
        return self.response()
