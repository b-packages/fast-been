from abc import ABC, abstractmethod


class Base(ABC):
    @abstractmethod
    def pattern(self):
        pass

    @abstractmethod
    def info(self):
        pass
