from . import APIView as Base


class Lister(Base):
    def run(self, query_params: dict):
        self.content = self.get_controller.run(query_params=query_params)
        return self.just_response()
