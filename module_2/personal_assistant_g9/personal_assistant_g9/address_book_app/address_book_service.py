from typing import Optional
from address_book_app.address_book import AddressBook
from shared.client import Service
from shared.cli_command import CLICommand
from address_book_app.fields import Name
from address_book_app.record import Record
from shared.error_decorator import *
from shared.assistant_exceptions import *
from shared.local_storage import Storage
from shared.status import Status


class AddressBookService(Service):
    def __init__(self, storage: Storage, address_book: AddressBook) -> None:
        self._address_book = address_book
        self._selected_record: Optional[Record] = None
        self._searched_records: list[Record] = []
        self._storage = storage
        self._handlers = {
            CLICommand.ADD: self._handle_add,
            CLICommand.ADDPHONE: self._handle_add_phone,
            CLICommand.SETEMAIL: self._handle_set_email,
            CLICommand.SETADDRESS: self._handle_set_address,
            CLICommand.SETBIRTHDAY: self._handle_set_birthday,
            CLICommand.SELECTREQUEST: self._handle_select_request,
            CLICommand.SELECT: self._handle_select_record,
            CLICommand.CHANGE: self._handle_change,
            CLICommand.PHONE: self._handle_phone,
            CLICommand.DELETE: self._handle_delete,
            CLICommand.SHOW: self._handle_show,
            CLICommand.SHOWSELECTED: self._handle_show_selected,
            CLICommand.SEARCH: self._handle_search,
            CLICommand.SEARCHSELECTING: self._handle_search_selecting,
            CLICommand.SAVE: self._handle_save,
            CLICommand.LOAD: self._handle_open,
            CLICommand.EXIT: self._handle_exit,
            CLICommand.HELP: self._handle_help,
            CLICommand.UNKNOWN: self._handle_unknown,
        }

    @input_error
    def get_handler(self, command: CLICommand):
        if command is CLICommand.UNKNOWN:
            raise UnknownAssistentCommand
        return self._handlers[command]

    def handle(self, command: CLICommand, value: list[str]) -> Status:
        handler = self.get_handler(command)
        return handler(value)

    def _handle_select_request(self, value: list[str]) -> Status:
        if not len(self._address_book):
            return Status("Address Book is empty. Add some record first.")
        if len(value) == 1 and int(value[0]) <= len(self._address_book):
            return self._handle_select_record(value)
        request = Status.Request(
            'Enter some text to find records or just hit "Enter" to show all records: ',
            CLICommand.SEARCHSELECTING,
        )
        return Status(request=request)

    def _handle_select_record(self, value: list[str]) -> Status:
        record_number = int(value[0])
        if (record_number - 1) < len(self._searched_records):
            self._selected_record = self._searched_records[record_number - 1]
        elif record_number <= len(self._address_book):
            self._selected_record = list(self._address_book.data.values())[
                record_number - 1
            ]
        else:
            if len(self._address_book) == 0:
                return Status("Cannot select the record because Address Book is empty.")
            else:
                return Status("You entered wrong record number.")
        return Status(
            f"{self._selected_record}.\nUse <SET EMAIL>, <SET ADDRESS>, <SET BIRTHDAY> or <DELETE> command to work on it"
        )

    def _handle_search_selecting(self, value: list[str]) -> Status:
        search_status = self._handle_search(value)
        if search_status.response.lower() != "no results":
            search_status.request = Status.Request(
                "Enter the record number: ", CLICommand.SELECT
            )
        return search_status

    @input_error
    def _handle_add(self, value: list[str]) -> Status:
        if len(value) < 2:
            raise UnknownAssistentValue("Give me a name and phone number(s) please.")
        self._address_book.add_record(value[0], value[1:])
        self._storage.save(self._address_book)
        return Status("Contact added successfully!")

    def _handle_add_phone(self, value: list[str]) -> Status:
        if len(value) < 1:
            raise UnknownAssistentValue("Please, enter one or more phone numbers!")
        if self._selected_record:
            self._selected_record.add_phone(value)
        else:
            return Status(
                "You didn't select record yet. Please use SELECT command first."
            )
        self._selected_record = None

        self._storage.save(self._address_book)
        if len(value) > 1:
            return Status("Phones are added successfully!")
        return Status("Phone is added successfully!")

    def _handle_set_email(self, value: list[str]) -> Status:
        if len(value) != 1:
            raise UnknownAssistentValue("Should be only one email")
        if self._selected_record:
            self._selected_record.set_email(value[0])
        else:
            return Status(
                "You didn't select record yet. Please use SELECT command first."
            )
        self._selected_record = None
        self._storage.save(self._address_book)
        return Status("Email is set successfully!")

    def _handle_set_address(self, value: list[str]) -> Status:
        if len(value) < 1:
            raise UnknownAssistentValue("Address cannot be empty!")
        if self._selected_record:
            self._selected_record.set_address(value)
        else:
            return Status(
                "You didn't select record yet. Please use SELECT command first."
            )
        self._selected_record = None
        self._storage.save(self._address_book)
        return Status("Address is set successfully!")

    def _handle_set_birthday(self, value: list[str]) -> Status:
        if len(value) != 1:
            raise UnknownAssistentValue("Should be only one birthday")
        if self._selected_record:
            self._selected_record.set_birthday(value[0])
        else:
            return Status(
                "You didn't select record yet. Please use SELECT command first."
            )
        self._selected_record = None
        self._storage.save(self._address_book)
        return Status("Birthday is set successfully!")

    @input_error
    def _handle_change(self, value: list[str]) -> str:
        if len(value) != 2:
            raise UnknownAssistentValue("Give me name and phone please.")
        message = "Contact updated successfully!"
        if value[0].lower() not in [x.lower() for x in self._address_book.keys()]:
            message = "This contact does not exist for updating.\nSo a new contact was created!"
        self._handle_add(value)
        return message

    @input_error
    def _handle_phone(self, value: list[str]) -> Status:
        if len(value) != 1:
            raise UnknownAssistentValue("Give me name.")
        record = (
            self._address_book.find_by_name(Name(value[0]))
            or "The specified contact does not exist."
        )
        return Status(str(record))

    def _handle_delete(self, value) -> Status:
        if self._selected_record:
            self._address_book.remove_record(self._selected_record)
            self._selected_record = None
            self._storage.save(self._address_book)
            return Status("Record is deleted successfully!")
        return Status(
            "You didn't select a record yet. Please use SELECT command first."
        )

    @input_error
    def _handle_search(self, value: list[str]) -> Status:
        searched_text = " ".join(value)
        self._searched_records = self._address_book.search(searched_text)

        if self._searched_records:
            message = ""
            for i, v in enumerate(self._searched_records):
                message += f"{i + 1}. {v}\n"
            message.strip("\n")
            message = "----------------------\n" + message + "----------------------"
            return Status(message)
        return Status("No Results")

    def _handle_show_selected(self, value) -> Status:
        if self._selected_record:
            return Status(str(self._selected_record))
        return Status("You didn't select record yet. Please use SELECT command first.")

    @input_error
    def _handle_show(self, value) -> Status:
        status = self._handle_search([])

        if status.response == "No Results":
            return Status("Contact list is empty!")

        return status

    def _handle_save(self, value: list[str]) -> Status:
        if len(value) != 1:
            raise IncorrectFileName()
        self._storage.save(self._address_book, value[0])
        return Status("Address Book saved successfully!")

    def _handle_open(self, value: list[str]) -> Status:
        if len(value) != 1:
            raise IncorrectFileName()
        self._address_book = self._storage.load(value[0])
        return self._handle_show(None)

    @input_error
    def _handle_exit(self, value) -> Status:
        return Status("Good bye!")

    @input_error
    def _handle_help(self, value) -> Status:
        commands = [
            "ADD <name> <phone> <phone>...",
            "SELECT",
            "SELECT <number of record>",
            "SET EMAIL <email>",
            "SET ADDRESS <address>",
            "SET BIRTHDAY <birthday>",
            "DELETE",
            "SEARCH <text>",
            "CHANGE <name> <phone>",
            "PHONE <name>",
            "LOAD <filename>",
            "SAVE <filename>",
            "SELECTED",
            "SHOW ALL",
            "GOOD BYE",
            "CLOSE",
            "EXIT",
        ]
        return Status("\n".join(commands))

    @input_error
    def _handle_unknown(value) -> str:
        return "Incorrect Command!!!"
