import json
from serialization_interface import SerializationInterface
from person import Person


class JsonSerialization(SerializationInterface):
    def save(self, object, filename, cls=None):
        with open(filename, "w") as fh:
            json.dump(object, fh, cls=cls)

    def load(self, filename, cls=None):
        with open(filename, "r") as fh:
            unpacked = json.load(fh, cls=cls)
            return unpacked

    @property
    def extension(self):
        return "json"
