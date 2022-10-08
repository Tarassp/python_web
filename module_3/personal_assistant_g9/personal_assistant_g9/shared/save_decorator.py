
def save_func(self, func):
       def inner(*args, **kwargs):
            result = func(*args, **kwargs)
            self._storage.save(self._notebook)
            return result
        return inner