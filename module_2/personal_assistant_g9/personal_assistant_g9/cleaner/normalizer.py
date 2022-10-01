import re
from abc import ABC, abstractmethod

class NormalizerInterface(ABC):
    @abstractmethod
    def normalize(self, text) -> str:
        pass

class NameNormalizer(NormalizerInterface):
    cyrillic_symbols = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
    translation = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")
    def __init__(self):
        self.table = {}
        for c, t in zip(NameNormalizer.cyrillic_symbols, NameNormalizer.translation):
            self.table[ord(c)] = t 
            self.table[ord(c.upper())] = t.upper()
            
    def translate(self, name):
        return name.translate(self.table)

    def normalize(self, name) -> str:
        new_name = self.translate(name)
        return re.sub(r'[^\w]', '_', new_name)