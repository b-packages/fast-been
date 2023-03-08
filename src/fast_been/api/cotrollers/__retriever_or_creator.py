from fast_been.utils.exceptions.http import ThereIsNoInputDataToGetOrCreateHTTPException
from . import APIController as Base


class RetrieverOrCreator(Base):

    def __init__(self):
        self.__input_data = None
        self.instance = None

    def run(self, input_data) -> (dict, bool):
        self.__input_data = self.lookup_fields = input_data
        if self.__input_data is None:
            raise ThereIsNoInputDataToGetOrCreateHTTPException()
        return self.get_or_create()

    def get_or_create(self) -> (dict, bool):
        created = False

        self.instance = self.retrieve_data()

        if not self.instance:
            input_ = self.input_data(**self.__input_data)
            self.instance = self.create_data(**input_)
            created = True

        output_ = self.output_data(**self.instance.to_dict())
        return output_, created

    @property
    def controller_type(self) -> str:
        return 'RETRIEVER_OR_CREATOR'
