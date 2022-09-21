from bin_serialization import BinSerialization
from json_serialization import JsonSerialization
from person import Person, PersonEncoder, PersonDecoder
from repository import Repository


# This main function checks only HW #1
# To check HW #2 (META class) go to meta.py module
def main():
    user = Person("Alex", 30)
    repository = Repository(JsonSerialization(), "users")

    command = ""
    while command != "exit":
        command = input(
            "1. BinSerialization\n2. JsonSerialization\nEnter your choice: "
        )
        clsEncoder = None
        clsDecoder = None

        if command == "1":
            repository.serializer = BinSerialization()
        elif command == "2":
            clsEncoder = PersonEncoder
            clsDecoder = PersonDecoder
            repository.serializer = JsonSerialization()
        else:
            return

        repository.save(user, cls=clsEncoder)
        print(f"Original: {user}")

        unpacked_user = repository.load(cls=clsDecoder)
        print(f"Unpacked: {unpacked_user}")


if __name__ == "__main__":
    main()
