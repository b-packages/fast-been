from . import APIController as Base


class Lister(Base):

    def __init__(self):
        self.__query_params = None

    def run(self, query_params, **kwargs) -> dict:
        self.__query_params = query_params
        return self.list()

    def list(self) -> dict:
        return self.list_data(**self.__query_params)

    @property
    def controller_type(self) -> str:
        return 'LISTER'
