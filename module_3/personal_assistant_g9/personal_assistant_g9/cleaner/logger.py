from abc import ABC, abstractmethod

class Logger(ABC):
    @abstractmethod
    def log(self, message, path):
        pass
    
class ConsoleLogger(Logger):
    def log(self, message, path = None):
        print(message)
            
    
class FileLogger(Logger):
    def log(self, message: dict, path):
        l = [f'{key}: {", ".join(value)}\n' for key, value in message.items() ]
        with open(path / 'log.txt', 'w') as fh:
            fh.writelines(l)