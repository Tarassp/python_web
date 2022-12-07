from __future__ import annotations
from typing import Optional, List
from datetime import date

from domain import model
from service_layer import unit_of_work


class InvalidUserId(Exception):
    pass


def add_contact(user_id: str, name: str, email: Optional[str], birthday: Optional[date], phones: List[str],
                uow: unit_of_work.AbstractUnitOfWork,
                ):
    with uow:
        address_book = uow.repository.get(user_id)
        if address_book is None:
            address_book = model.AddressBook(user_id, contacts=[])
            uow.repository.add(address_book)
        u_phones = set(model.Phone(n) for n in phones)
        address_book.add_contact(name, email, birthday, u_phones)
        uow.commit()


def add_phone(user_id: str, name: str, phone_number: str,
              uow: unit_of_work.AbstractUnitOfWork) -> model.Contact:
    phone = [model.Phone(phone_number)]
    with uow:
        address_book = uow.repository.get(user_id)
        if address_book is None:
            raise InvalidUserId(f"Invalid user id {user_id}")
        contact = address_book.update_contact(name=name, phones=set(phone))
        uow.commit()
    return contact


def delete_contact(user_id: str, name: str, uow: unit_of_work.AbstractUnitOfWork) -> model.Contact:
    with uow:
        address_book = uow.repository.get(user_id)
        contact = address_book.delete_contact(name)
        uow.commit()
    return contact


def get_all_contacts(user_id: str, uow: unit_of_work.AbstractUnitOfWork) -> List[model.Contact]:
    with uow:
        address_book = uow.repository.get(user_id)
    return address_book.contacts


def search_contacts(user_id: str, name: str, uow: unit_of_work.AbstractUnitOfWork) -> List[model.Contact]:
    with uow:
        address_book = uow.repository.get(user_id)
        contacts = address_book.search(name)
    return contacts
