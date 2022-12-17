from typing import Optional, List
from datetime import date
from src.service_layer.unit_of_work import AbstractUnitOfWork
from src.domain.address_book_model import AddressBook
from src.domain.contact_model import Contact


class InvalidUserId(Exception):
    pass


def add_contact(user_id: str, name: str, phone_number: str, email: Optional[str],
                address: Optional[str], birthday: Optional[date], uow: AbstractUnitOfWork):
    with uow:
        address_book = uow.addressBooks.get(user_id)
        if address_book is None:
            address_book = AddressBook(user_id, contacts=[])
            uow.addressBooks.add(address_book)
        address_book.add_contact(name, phone_number, email, address, birthday)
        uow.commit()


def get_contact(user_id: str, id: int, uow: AbstractUnitOfWork):
    with uow:
        address_book = uow.addressBooks.get(user_id)
        if address_book is None:
            raise InvalidUserId(f"Invalid user id {user_id}")
    return address_book.get_contact(id)


def update_contact(user_id: str, id: int, name: str, phone_number: str, email: Optional[str],
                   address: Optional[str], uow: AbstractUnitOfWork):
    with uow:
        address_book = uow.addressBooks.get(user_id)
        if address_book is None:
            raise InvalidUserId(f"Invalid user id {user_id}")
        address_book.update_contact(
            id, name, phone_number, email, address, None)
        uow.commit()


def delete_contact(user_id: str, id: int, uow: AbstractUnitOfWork):
    with uow:
        address_book = uow.addressBooks.get(user_id)
        if address_book is None:
            raise InvalidUserId(f"Invalid user id {user_id}")
        removed_contact = address_book.delete_contact(id)
        uow.delete(removed_contact)
        uow.commit()


def get_all_contacts(user_id: str, uow: AbstractUnitOfWork) -> List[Contact]:
    with uow:
        address_book = uow.addressBooks.get(user_id)
        if address_book is None:
            return []
            # raise InvalidUserId(f"Invalid user id {user_id}")
    return address_book.contacts
