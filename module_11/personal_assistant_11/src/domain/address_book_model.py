from typing import List, Optional
from src.domain.contact_model import Contact
from datetime import date


class ContactNotFound(Exception):
    ...


class AddressBook:
    def __init__(self, user_id: str, contacts: List[Contact]):
        self.user_id = user_id
        self.contacts = contacts

    def __repr__(self):
        return f"<AddressBook user_id: {self.user_id}, number of contacts: {len(self.contacts)}"

    def __eq__(self, other):
        if not isinstance(other, AddressBook):
            return False
        return other.user_id == self.user_id

    def __hash__(self):
        return hash(self.user_id)

    def get_contact(self, id: int) -> Contact:
        try:
            return next(c for c in self.contacts if c.id == id)
        except StopIteration:
            raise ContactNotFound(f'There is no contact with id {id}')

    def add_contact(self, name: str, phone_number: str, email: Optional[str], address: Optional[str], birthday: Optional[date]) -> Contact:
        contact = Contact(name, phone_number, email, address, birthday)
        self.contacts.append(contact)
        return contact

    def update_contact(self, id: int, name: str, phone_number: str, email: Optional[str] = None, address: Optional[str] = None, birthday: Optional[date] = None) -> Contact:
        contact = self.get_contact(id)
        if name:
            contact.name = name
        if phone_number is not None:
            contact.phone_number = phone_number
        if email is not None:
            contact.email = email
        if address is not None:
            contact.address = address
        if birthday is not None:
            contact.birthday = birthday
        return contact

    def delete_contact(self, id: int) -> Contact:
        contact = self.get_contact(id)
        self.contacts.remove(contact)
        return contact

    def search(self, name: str) -> List[Contact]:
        return list(filter(lambda contact: name in contact, self.contacts))
