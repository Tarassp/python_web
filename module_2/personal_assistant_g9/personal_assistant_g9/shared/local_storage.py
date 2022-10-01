import pickle
from abc import abstractmethod
from typing import Protocol


class Storage(Protocol):
    @abstractmethod
    def save(self, object, filename=None):
        raise NotImplementedError

    @abstractmethod
    def load(self, filename=None):
        raise NotImplementedError


class LocalStorage(Storage):
    def __init__(self, filename) -> None:
        self._default_filename = filename

    def save(self, object, filename=None):
        with open(filename or self._default_filename, "wb") as fh:
            pickle.dump(object, fh)

    def load(self, filename=None):
        try:
            with open(filename or self._default_filename, "rb") as fh:
                unpacked = pickle.load(fh)
                return unpacked
        except:
            return None
