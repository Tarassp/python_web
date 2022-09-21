from abc import ABC, abstractmethod


class SerializationInterface(ABC):
    @abstractmethod
    def save(self, object, filename, cls=None):
        NotImplementedError()

    @abstractmethod
    def load(self, filename, cls=None):
        NotImplementedError()

    @property
    @abstractmethod
    def extension(self):
        NotImplementedError()
