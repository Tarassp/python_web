from sqlalchemy.orm import relationship, backref, registry
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Table
from src.domain import contact_model, address_book_model, user_model


mapper_registry = registry()
Base = mapper_registry.generate_base()


users = Table(
    'users',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(120), nullable=False),
    Column('email', String(120), unique=True, nullable=False),
    Column('p_hash', String(255), nullable=False),
    Column('token_cookie', String(255), nullable=True, default=None)
)

contacts = Table(
    'contacts',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(100), unique=True, nullable=False),
    Column('phone_number', String(50), nullable=False),
    Column('email', String(50), nullable=True),
    Column('address', String(255), nullable=True),
    Column('birthday', Date, nullable=True),
    Column('address_book_id', Integer, ForeignKey(
        "address_books.id", ondelete="CASCADE", onupdate="CASCADE"))

)

address_books = Table(
    'address_books',
    Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey(
        'users.id', ondelete="CASCADE", onupdate="CASCADE"))
)


def start_mappers():
    users_mapper = mapper_registry.map_imperatively(user_model.User, users)

    address_books_mapper = mapper_registry.map_imperatively(
        address_book_model.AddressBook,
        address_books,
        properties={
            'user': relationship(users_mapper, backref=backref("address_book", uselist=False))
        }
    )

    mapper_registry.map_imperatively(
        contact_model.Contact,
        contacts,
        properties={
            'address_book': relationship(address_books_mapper, backref='contacts')
        }
    )
