from presentation_layer.cli.cli_command import CLICommand
from presentation_layer.assistant_exceptions import *
from typing import Optional
from presentation_layer.cli.status import Status
from service_layer.unit_of_work import SqlAlchemyUnitOfWork
from domain.model import User
from service_layer import services
from datetime import date, datetime


class AddressBookService:
    def __init__(self, user: User) -> None:
        self.user = user
        self._handlers = {
            CLICommand.ADD: self._handle_add,
            CLICommand.SHOW: self._handle_show,
            CLICommand.ADDPHONE: self._handle_add_phone,
            CLICommand.DELETE: self._handle_delete,
            CLICommand.SEARCH: self._handle_search,
            CLICommand.EXIT: self._handle_exit,
            CLICommand.HELP: self._handle_help,
            CLICommand.UNKNOWN: self._handle_unknown,
        }

    def get_handler(self, command: CLICommand):
        if command is CLICommand.UNKNOWN:
            raise UnknownAssistentCommand
        return self._handlers[command]

    def handle(self, command: CLICommand, value: list[str]) -> Status:
        handler = self.get_handler(command)
        return handler(value)

    def _handle_add(self, value: list[str]) -> Status:
        if len(value) < 2:
            raise UnknownAssistentValue(
                "Give me at least a name and phone number(s) please.")
        name = value[0]
        phone = value[1]
        email: Optional[str] = None
        birthday: Optional[date] = None
        try:
            email = value[2]
            birthday = datetime.fromisoformat(value[3]).date()
        except Exception as err:
            ...
            # print(f"Error inside add contact: {err}")

        new_contact = services.add_contact(self.user.id, name, email, birthday,
                                           [phone], SqlAlchemyUnitOfWork())
        return Status("Contact added successfully!")

    def _handle_add_phone(self, value: list[str]) -> Status:
        if len(value) < 2:
            raise UnknownAssistentValue(
                "Please, enter the name and a phone number!")
        services.add_phone(
            self.user.id, name=value[0], phone_number=value[1], uow=SqlAlchemyUnitOfWork())
        return Status("Phone is added successfully!")

    def _handle_show(self, value) -> Status:
        contacts = services.get_all_contacts(
            self.user.id, SqlAlchemyUnitOfWork())
        message = ""
        for contact in contacts:
            message += str(contact) + "\n"

        return Status(message.rstrip())

    def _handle_delete(self, value: list[str]) -> Status:
        services.delete_contact(self.user.id, value[0], SqlAlchemyUnitOfWork())
        return Status("Contact is deleted successfully!")

    def _handle_search(self, value: list[str]) -> Status:
        contacts = services.search_contacts(
            self.user.id, value[0], SqlAlchemyUnitOfWork())
        if contacts:
            message = ""
            for c in contacts:
                message += str(c) + "\n"
            return Status(message.rstrip())
        return Status("No Results")

    def _handle_exit(self, value) -> Status:
        return Status("Good bye!")

    def _handle_help(self, value) -> Status:
        commands = [
            "ADD <name> <phone> [<email>, <birthday(2000-01-01)>]",
            "DELETE <name>",
            "SEARCH <text>",
            "ADDPHONE <name> <phone>",
            "SHOW ALL",
            "GOOD BYE",
            "CLOSE",
            "EXIT",
        ]
        return Status("\n".join(commands))

    def _handle_unknown(self, value) -> str:
        return "Incorrect Command!!!"
