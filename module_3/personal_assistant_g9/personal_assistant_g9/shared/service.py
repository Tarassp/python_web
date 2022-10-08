from abc import ABC, abstractmethod
from shared.cli_command import CLICommand
from shared.status import Status


class Service(ABC):
    @abstractmethod
    def handle(self, command: CLICommand, value: list[str]) -> Status:
        ...