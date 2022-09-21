from serialization_interface import SerializationInterface


class Repository:
    def __init__(self, serializer: SerializationInterface, filename: str):
        self.serializer = serializer
        self.filename = filename

    def save(self, object, cls=None):
        filename = self.filename + "." + self.serializer.extension
        self.serializer.save(object, filename, cls=cls)

    def load(self, cls=None):
        filename = self.filename + "." + self.serializer.extension
        return self.serializer.load(filename, cls=cls)
