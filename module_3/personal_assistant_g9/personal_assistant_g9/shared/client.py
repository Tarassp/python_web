from abc import ABC, abstractmethod
from shared.cli_command import CLICommand
from shared.parser import CLIParser
from shared.service import Service


class Client(ABC):
    @property
    @abstractmethod
    def message(self) -> str:
        ...

    @abstractmethod
    def create_service(self) -> Service:
        ...

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
            # except:
            #     print("Type 'help' to see the commands.")
