from src.domain.user_model import User
from src.domain.address_book_model import AddressBook
from src.domain.contact_model import Contact
from datetime import date


def test_users_mapper_can_load_users(session):
    session.execute("insert into users (username, email, p_hash, token_cookie) values "
                    '("name_1","email_1","hash_1","cookie_1"),'
                    '("name_2","email_2","hash_2","cookie_2")'
                    )
    expected = [
        User("name_1", "email_1", "hash_1", "cookie_1"),
        User("name_2", "email_2", "hash_2", "cookie_2")
    ]

    assert session.query(User).all() == expected


def test_users_mapper_can_save_users(session):
    user = User("name_1", "email_1", "hash_1", "cookie_1")
    session.add(user)
    session.commit()
    rows = list(session.execute(
        'SELECT username, email, p_hash, token_cookie FROM "users"'))
    expected = [("name_1", "email_1", "hash_1", "cookie_1")]
    assert rows == expected


def test_contacts_mapper_can_load_contacts(session):
    session.execute("INSERT INTO contacts (name, phone_number, email, address, birthday) VALUES "
                    '("contact_1", "0661111111", "contact1@gmail.com", "address_1", "2001-01-01"),'
                    '("contact_2", "0662222222", "contact2@gmail.com", "address_2", "2002-02-02")'
                    )

    expected = [
        Contact("contact_1", "0661111111", "contact1@gmail.com",
                "address_1", date(2001, 1, 1)),
        Contact("contact_2", "0662222222", "contact2@gmail.com",
                "address_2", date(2002, 2, 2))
    ]

    assert session.query(Contact).all() == expected


def test_contacts_mapper_can_save_contacts(session):
    contact = Contact("contact_1", "0661111111",
                      "contact1@gmail.com", "address_1", date(2001, 1, 1))
    session.add(contact)
    session.commit()

    rows = list(session.execute(
        'SELECT name, phone_number, email, address, birthday FROM "contacts"'))
    expected = [("contact_1", "0661111111", "contact1@gmail.com",
                 "address_1", "2001-01-01")]

    assert rows == expected


def test_address_book_can_load_contacts(session):
    session.execute('INSERT INTO contacts (name, phone_number, email, address, birthday, address_book_id) VALUES '
                    '("contact_1", "0661111111", "contact1@gmail.com", "address_1", "2001-01-01", 1),'
                    '("contact_2", "0662222222", "contact2@gmail.com", "address_2", "2002-02-02", 1)'
                    )
    session.execute('INSERT INTO address_books (user_id) VALUES '
                    '("user_007")')

    address_book = session.query(AddressBook).first()
    assert address_book.contacts == [Contact("contact_1", "0661111111",
                                             "contact1@gmail.com", "address_1", date(2001, 1, 1)),
                                     Contact("contact_2", "0662222222",
                                             "contact2@gmail.com", "address_2", date(2002, 2, 2))]


def test_address_book_can_save_contacts(session):
    contact_1 = Contact("contact_1", "0661111111",
                        "contact1@gmail.com", "address_1", date(2001, 1, 1))
    contact_2 = Contact("contact_2", "0662222222",
                        "contact2@gmail.com", "address_2", date(2002, 2, 2))
    address_book = AddressBook('user_007', [contact_1, contact_2])
    session.add(address_book)
    session.commit()

    rows = list(session.execute(
        'SELECT ab.user_id, c.name, c.phone_number, c.email, c.address, c.birthday '
        'FROM "contacts" AS c '
        'JOIN "address_books" AS ab ON c.address_book_id = ab.id'))
    expected = [("user_007", "contact_1", "0661111111",
                 "contact1@gmail.com", "address_1", "2001-01-01"),
                ('user_007', "contact_2", "0662222222",
                 "contact2@gmail.com", "address_2", "2002-02-02")]

    assert rows == expected
