from typing import Optional
from address_book_app.fields import Address, Phone, Name, Birthday, Email
from datetime import datetime
import re


class Record:
    def __init__(self, name: Name, phones: list[Phone]) -> None:
        self.name = name
        self.phones = phones
        self.email: Optional[Email] = None
        self.address: Optional[Address] = None
        self.birthday: Optional[Birthday] = None

    def add_phone(self, phone_numbers: list[str]):
        phones = [Phone(number) for number in phone_numbers]
        self.phones.extend(phones)

    def set_email(self, email: str):
        email_field = Email(email)
        self.email = email_field

    def set_address(self, address: list[str]):
        address_field = Address(" ".join(address))
        self.address = address_field

    def set_birthday(self, birthday: str):
        birthday_field = Birthday(birthday)
        self.birthday = birthday_field

    def remove_phone(self, phone: Phone):
        self.phones.remove(phone)

    def update_phone(self, phone: Phone):
        pass

    def days_to_birthday(self) -> Optional[int]:
        if self.birthday:
            birthday_date = self.birthday.datetime
            now = datetime.now()
            delta1 = datetime(now.year, birthday_date.month, birthday_date.day)
            delta2 = datetime(now.year + 1, birthday_date.month, birthday_date.day)
            return ((delta1 if delta1 > now else delta2) - now).days
        return None

    def __contains__(self, other):
        l = []
        if self.__has_valid_phone(other):
            l = list(filter(lambda x: other in x, self.phones))
        if not l:
            return other in self.name
        return bool(l)

    def __has_valid_phone(self, string: str) -> bool:
        return re.search("^\+?\d+$", string) != None

    def __str__(self) -> str:
        description = str(self.name)

        if self.phones:
            description += " " + ", ".join(map(str, self.phones))

        if self.address:
            description += " " + str(self.address)

        if self.email:
            description += " " + str(self.email)

        if self.birthday:
            description += " " + str(self.birthday)

        return description
