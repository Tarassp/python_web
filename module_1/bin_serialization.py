import pickle
from serialization_interface import SerializationInterface

class BinSerialization(SerializationInterface):
    def save(self, object, filename, cls = None):
        with open(filename, 'wb') as fh:
            pickle.dump(object, fh) 
    
    def load(self, filename, cls = None):
        with open(filename, 'rb') as fh:
            unpacked = pickle.load(fh)
            return unpacked
    
    @property    
    def extension(self):
        return 'bin'