from __future__ import annotations
from typing import Optional
from datetime import date


class Contact:
    def __init__(self, name: str, phone_number: str, email: Optional[str], address: Optional[str], birthday: Optional[date]):
        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.birthday = birthday

    def __repr__(self):
        string_repr = self.name + " "
        if self.phone_number:
            string_repr += self.phone_number + " "
        if self.email is not None:
            string_repr += self.email + " "
        if self.address is not None:
            string_repr += self.address + " "
        if self.birthday is not None:
            string_repr += self.birthday.strftime("%m/%d/%Y")

        return string_repr

    def __eq__(self, other):
        if not isinstance(other, Contact):
            return False
        return other.name == self.name

    def __hash__(self):
        return hash(self.name)

    def __contains__(self, other):
        return other in str(self)
