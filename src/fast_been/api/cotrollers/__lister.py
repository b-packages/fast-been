from fast_been.utils.macros import ControllerType

from . import Base


class Lister(Base):

    def __init__(self, **kwargs):
        self.__params = kwargs

    def run(self) -> dict:
        return self.list()

    def list(self) -> dict:
        return self.list_data(**self.__params)

    @property
    def controller_type(self) -> str:
        return ControllerType.lister()
