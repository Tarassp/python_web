from cleaner.cleaner_client import CleanerClient
from shared.client import Client
from address_book_app.address_book_client import AddressBookClient
from notebook_app.notebook_client import NotebookClient
import os

welcome_message = """Welcome to Personal Assistant Manager!
Menu:
    1. NoteBook 
    2. AddressBook
    3. FolderCleaner
    4. Exit from Personal Assistant Manager
Enter your option: """


class Application:
    def __init__(self) -> None:
        self.client: Client

    def start(self) -> None:
        while True:
            line = input(welcome_message)
            match line:
                case "1":
                    os.system("cls||clear")
                    self.client = NotebookClient()
                case "2":
                    os.system("cls||clear")
                    self.client = AddressBookClient()
                case "3":
                    os.system("cls||clear")
                    self.client = CleanerClient()
                case "4" | "exit":
                    os.system("cls||clear")
                    break
                case _:
                    print("Wrong command")
            self.client.run()


if __name__ == "__main__":
    app = Application()
    app.start()
