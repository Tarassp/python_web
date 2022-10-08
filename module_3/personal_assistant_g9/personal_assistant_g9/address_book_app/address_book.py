from collections import UserDict
from address_book_app.fields import Phone, Name
from address_book_app.record import Record


class AddressBook(UserDict):
    def add_record(self, name: str, phones: list[str]):
        name_field = Name(name)
        phones_field = [Phone(v) for v in phones]
        record = Record(name_field, phones_field)
        self.data[name_field.value] = record

    def remove_record(self, record: Record):
        return self.data.pop(record.name.value)

    def find_by_name(self, name: Name) -> Record | None:
        for key, value in self.data.items():
            if key.lower() == name.value.lower():
                return value
        return None

    def find_by_phone(self, phone: Phone) -> Record | None:
        for record in self.data.values():
            if phone in record.phones:
                return record

    def search(self, text: str) -> list[Record]:
        return list(filter(lambda record: text in record, self.data.values()))

    def iterator(self, n):
        records: list[Record] = list(self.data.values())
        for i in range(0, len(records), n):
            yield records[i : i + n]
