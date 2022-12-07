from sqlalchemy import Table, MetaData, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import mapper, relationship

from domain import model

metadata = MetaData()

phone_numbers = Table(
    "phone_numbers",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("phone", String(50), nullable=False),
    Column("contact_id", ForeignKey("contacts.id",
           ondelete="CASCADE", onupdate="CASCADE")),
)

contacts = Table(
    "contacts",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50), unique=True),
    Column("email", String(50), nullable=True),
    Column("address", String(255), nullable=True),
    Column("birthday", Date, nullable=True),
    Column("address_book_id", ForeignKey(
        "address_books.id", ondelete="CASCADE", onupdate="CASCADE")),
)

address_books = Table(
    "address_books",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", String),
    Column("version_number", Integer, nullable=False, server_default="0"),
)


def start_mappers():
    phones_mapper = mapper(model.Phone, phone_numbers)
    contacts_mapper = mapper(model.Contact,
                             contacts,
                             properties={
                                 "phone_numbers": relationship(phones_mapper, collection_class=set)
                             },
                             )

    mapper(
        model.AddressBook, address_books, properties={
            "contacts": relationship(contacts_mapper)}
    )
