import json


class Person(json.JSONEncoder, json.JSONDecoder):
    def __init__(self, name: str, age: int) -> None:
        self.name = name
        self.age = age
        self.some_tuple = (5, 6)

    def __repr__(self) -> str:
        return (
            f"id: {id(self)} name: {self.name} age: {self.age} tuple: {self.some_tuple}"
        )


class PersonEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Person):
            return {
                "__person__": True,
                "name": o.name,
                "age": o.age,
                "some_tuple": o.some_tuple,
            }
        return super().default(o)


class PersonDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        json.JSONDecoder.__init__(self, object_hook=self.object_hook, *args, **kwargs)

    def object_hook(self, dct):
        if "__person__" in dct:
            some_tuple = dct["some_tuple"]
            o = Person(dct["name"], dct["age"])
            o.some_tuple = tuple(some_tuple)
            return o
        return dct
