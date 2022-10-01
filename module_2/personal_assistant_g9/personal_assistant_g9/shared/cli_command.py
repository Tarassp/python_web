from enum import Enum, unique


@unique
class CLICommand(Enum):
    SELECT = ["choose"]
    SELECTREQUEST = ["select"]
    ADD = ["add"]
    CHANGE = ["change"]
    DELETE = ["delete"]
    SEARCH = ["search"]
    SEARCHSELECTING = ["search selecting"]
    SHOWSELECTED = ["selected"]
    SHOW = ["show all"]
    LOAD = ["load"]
    SAVE = ["save"]
    HELP = ["help"]
    UNKNOWN = ["unknown"]
    EXIT = ["exit", "close", "good bye"]
    NONE = ["none"]

    # AddressBookCommand
    ADDPHONE = ["add phone"]
    SETEMAIL = ["set email"]
    SETADDRESS = ["set address"]
    SETBIRTHDAY = ["set birthday"]
    PHONE = ["phone"]

    # NotesCommand
    TAGS = ["tags"]
    SEARCHBYTAG = ["search tag"]
    SORTBYTAGS = ["sort tags"]

    @classmethod
    def _missing_(cls, value: str):
        for item in cls.__members__.values():
            if value.lower() in item.value:
                return item
        else:
            return cls.UNKNOWN

    @classmethod
    @property
    def max_command_words(cls) -> int:
        return 2
