from . import APIView as Base


class Updater(Base):
    def run(self, lookup_field, input_data):
        self.content = self.get_controller.run(
            lookup_field=lookup_field, input_data=input_data)
        return self.just_response()
