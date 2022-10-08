from shared.client import Client
from shared.local_storage import LocalStorage
from shared.service import Service
from address_book_app.address_book import AddressBook
from address_book_app.address_book_service import AddressBookService


class AddressBookClient(Client):
    @property
    def message(self) -> str:
        return "Welcome to Address Book App!\nEnter the command or type 'help' to see the list of commands: "

    def create_service(self) -> Service:
        storage = LocalStorage("address_book")
        address_book = storage.load() or AddressBook()
        return AddressBookService(storage, address_book)
