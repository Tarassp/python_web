from abc import ABC, abstractmethod
from shared.cli_command import CLICommand


class Parser(ABC):
    @abstractmethod
    def get_command(self) -> CLICommand:
        ...

    @abstractmethod
    def get_value(self) -> list[str]:
        ...


class CLIParser(Parser):
    def __init__(self, string: str, reserved_command=CLICommand.NONE):
        self._line_parameters = string.split()
        self.quantity_words_in_command = 0
        self.reserved_command = reserved_command

    def get_command(self) -> CLICommand:
        if self.reserved_command is not CLICommand.NONE:
            return self.reserved_command

        for i in reversed(range(CLICommand.max_command_words)):
            raw_command = " ".join(self._line_parameters[: i + 1])
            command = CLICommand(raw_command)
            if command is not CLICommand.UNKNOWN:
                self.quantity_words_in_command = len(raw_command.split())
                return command
        return CLICommand.UNKNOWN

    def get_value(self) -> list[str]:
        value = self._line_parameters[self.quantity_words_in_command :]
        return value
