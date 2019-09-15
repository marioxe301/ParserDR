from abc import ABC, abstractmethod

class ParserFunctions(ABC):
    @abstractmethod
    def Program(self):
        raise NotImplementedError

    @abstractmethod
    def nextToken(self):
        raise NotImplementedError

    @abstractmethod
    def seekToken(self):
        raise NotImplementedError