from presentation_layer.cli.cli_command import CLICommand
from presentation_layer.cli.parser import CLIParser
from presentation_layer.cli.cli_handlers import AddressBookService
from domain.model import User


class Client:

    def __init__(self, user: User) -> None:
        self.user = user

    @property
    def message(self) -> str:
        return "Welcome to Address Book App!\nEnter the command or type 'help' to see the list of commands: "

    def create_service(self) -> AddressBookService:
        return AddressBookService(self.user)

    def run(self):
        service = self.create_service()
        hint = self.message
        reserved_command = CLICommand.NONE

        while True:
            line = input(hint)
            try:
                parser = CLIParser(line, reserved_command)
                command = parser.get_command()
                value = parser.get_value()

                status = service.handle(command, value)

                if status.response:
                    print(status.response)

                if status.request:
                    hint = status.request.message
                    reserved_command = status.request.command
                    continue

                match command:
                    case CLICommand.EXIT:
                        break
                    case _:
                        reserved_command = CLICommand.NONE
                        hint = "Enter your command: "
            except Exception as e:
                print(e)
