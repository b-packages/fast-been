from fast_been.utils.macros import ControllerType

from . import Base


class Lister(Base):

    def run(self, **kwargs) -> dict:
        return self.list(**kwargs)

    def list(self, **kwargs) -> dict:
        return self.list_data(**kwargs)

    @property
    def controller_type(self) -> str:
        return ControllerType.lister()
