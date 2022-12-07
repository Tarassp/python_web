from enum import Enum, unique


@unique
class CLICommand(Enum):
    ADD = ["add"]
    ADDPHONE = ["add phone"]
    SETEMAIL = ["set email"]
    SETADDRESS = ["set address"]
    SETBIRTHDAY = ["set birthday"]
    PHONE = ["phone"]
    DELETE = ["delete"]
    SEARCH = ["search"]
    SHOW = ["show all"]
    HELP = ["help"]
    EXIT = ["exit", "close", "good bye"]
    UNKNOWN = ["unknown"]
    NONE = ["none"]

    @classmethod
    def _missing_(cls, value: str):
        for item in cls.__members__.values():
            if value.lower() in item.value:
                return item
        return cls.UNKNOWN

    @classmethod
    @property
    def max_command_words(cls) -> int:
        return 2
