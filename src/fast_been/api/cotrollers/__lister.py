from fast_been.utils.macros import ControllerType

from . import APIController as Base


class Lister(Base):

    def __init__(self, query_params, **kwargs):
        self.__query_params = query_params

    def run(self) -> dict:
        return self.list()

    def list(self) -> dict:
        return self.list_data(**self.__query_params)

    @property
    def controller_type(self) -> str:
        return ControllerType.lister()
