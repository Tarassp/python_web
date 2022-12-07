from typing import Optional, List
from dataclasses import dataclass
from datetime import date


class ContactNotFound(Exception):
    ...


class Phone:
    def __init__(self, phone) -> None:
        self.phone = phone

    def __hash__(self):
        return hash(self.phone)


@dataclass
class Contact:
    name: str
    email: Optional[str]
    address: Optional[str]
    birthday: Optional[date]
    phone_numbers: set[Phone]

    def __repr__(self):
        string_repr = self.name + " "
        if self.email is not None:
            string_repr += self.email + " "
        if self.address is not None:
            string_repr += self.address + " "
        if self.birthday is not None:
            string_repr += self.birthday.strftime("%m/%d/%Y") + " "
        if len(self.phone_numbers) > 0:
            for phone in self.phone_numbers:
                string_repr += phone.phone + " "
        return string_repr.rstrip()

    def __eq__(self, other):
        if not isinstance(other, Contact):
            return False
        return other.name == self.name

    def __hash__(self):
        return hash(self.name)

    def __contains__(self, other):
        return other in str(self)


class AddressBook:
    def __init__(self, user_id: str, contacts: List[Contact], version_number: int = 0):
        self.user_id = user_id
        self.contacts = contacts
        self.version_number = version_number

    def __repr__(self):
        return f"<AddressBook {self.user_id}, {self.version_number}>"

    def __eq__(self, other):
        if not isinstance(other, AddressBook):
            return False
        return other.user_id == self.user_id

    def __hash__(self):
        return hash(self.user_id)

    def get_contact(self, name: str) -> Contact:
        try:
            return next(c for c in self.contacts if c.name == name)
        except StopIteration:
            raise ContactNotFound(f'There is no contact for name {name}')

    def add_contact(self, name: str, email: Optional[str], birthday: Optional[date], phones: set[Phone]) -> Contact:
        contact = Contact(name, email, None, birthday, phones)
        self.contacts.append(contact)
        return contact

    def update_contact(self, name: str, email: Optional[str] = None, address: Optional[str] = None, birthday: Optional[date] = None, phones: set[Phone] = set()) -> Contact:
        contact = self.get_contact(name)
        if email is not None:
            contact.email = email
        if address is not None:
            contact.address = address
        if birthday is not None:
            contact.birthday = birthday
        if phones:
            contact.phone_numbers = phones
        return contact

    def delete_contact(self, name) -> Contact:
        contact = self.get_contact(name)
        self.contacts.remove(contact)
        return contact

    def search(self, name: str) -> List[Contact]:
        return list(filter(lambda contact: name in contact, self.contacts))


class User:
    def __init__(self, name: str, user_id: str) -> None:
        self.name = name
        self.id = user_id
