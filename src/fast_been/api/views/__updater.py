from . import APIView as Base


class Updater(Base):
    def run(self, lookup_fields, input_data):
        self.content = self.get_controller.run(
            lookup_fields=lookup_fields, input_data=input_data)
        return self.response()
