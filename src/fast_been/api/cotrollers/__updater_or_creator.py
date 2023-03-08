from fast_been.utils.exceptions.http import ThereIsNoInputDataToUpdateOrCreateHTTPException
from . import APIController as Base


class UpdaterOrCreator(Base):

    def __init__(self):
        self.__input_data = None
        self.instance = None

    def run(self, input_data) -> (dict, bool):
        self.__input_data = self.lookup_fields = input_data
        if self.__input_data is None:
            raise ThereIsNoInputDataToUpdateOrCreateHTTPException()
        return self.update_or_create()

    def update_or_create(self) -> (dict, bool):
        created = False
        input_ = self.input_data(**self.__input_data)

        self.instance = self.update_data(**input_)

        if not self.instance:
            self.instance = self.create_data(**input_)
            created = True

        output_ = self.output_data(**self.instance.to_dict())
        return output_, created

    @property
    def controller_type(self) -> str:
        return 'CREATOR_OR_UPDATER'
