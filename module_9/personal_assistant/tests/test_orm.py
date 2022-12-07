from domain import model
from datetime import date


def test_phone_mapper_can_save_phones(session):
    phone = model.Phone("380664245216")
    session.add(phone)
    session.commit()

    rows = list(session.execute('SELECT phone FROM "phone_numbers"'))
    assert rows == [("380664245216",)]


def test_retrieving_contacts(session):
    session.execute(
        "INSERT INTO contacts (name, email, address, birthday)"
        ' VALUES ("Taras", "my_email@gamil.com", "Soborna Street 100", null)'
    )
    session.execute(
        "INSERT INTO contacts (name, email, address, birthday)"
        ' VALUES ("Olexsander", "his_email@gamil.com", "Oxford Srteet 1", "2000-01-01")'
    )
    expected = [
        model.Contact("Taras", "my_email@gamil.com",
                      "Soborna Street 100", None, set()),
        model.Contact("Olexsander", "his_email@gmail.com",
                      "Oxford Street 1", date(2011, 4, 11), set())
    ]

    assert session.query(model.Contact).all() == expected


def test_saving_contacts(session):
    contact = model.Contact("Taras", "my_email@gamil.com",
                            "Soborna Street 100", None, set())
    session.add(contact)
    session.commit()
    rows = session.execute(
        'SELECT name, email, address, birthday FROM "contacts"'
    )
    assert list(rows) == [
        ("Taras", "my_email@gamil.com", "Soborna Street 100", None)]


def test_retrieving_address_book(session):
    session.execute(
        "INSERT INTO address_books (user_id, version_number)"
        ' VALUES ("user-001", 1)'
    )
    expected = [
        model.AddressBook("user-001", [], 1)
    ]

    assert session.query(model.AddressBook).all() == expected


def test_saving_address_book(session):
    address_book = model.AddressBook("user-001", [], 1)
    session.add(address_book)
    session.commit()
    rows = session.execute(
        'SELECT user_id, version_number FROM "address_books"'
    )
    assert list(rows) == [("user-001", 1)]
