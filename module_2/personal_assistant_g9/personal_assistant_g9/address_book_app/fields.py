from datetime import datetime
from shared.assistant_exceptions import (
    IncorrectDateFormat,
    IncorrectDataFormat,
    IncorrectPhoneFormat,
    IncorrectEmailFormat,
)
import re


class Field:
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        if self._validate(new_value):
            self._value = new_value
        else:
            self._throw_exeption()

    def _validate(self, value: str) -> bool:
        return True

    def _throw_exeption(self) -> None:
        raise IncorrectDataFormat()

    def __init__(self, value: str) -> None:
        self._value = value if self._validate(value) else self._throw_exeption()

    def __contains__(self, other):
        if isinstance(other, str):
            return other.lower() in self._value.lower()
        return False

    def __str__(self) -> str:
        return self._value or "Incorrect value"


class Address(Field):
    def __str__(self) -> str:
        return "Address: " + super().__str__()


class Name(Field):
    def __str__(self) -> str:
        return "Name: " + super().__str__()


class Email(Field):
    def _validate(self, value: str) -> bool:
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        return re.fullmatch(regex, value) != None

    def _throw_exeption(self) -> None:
        raise IncorrectEmailFormat()

    def __str__(self) -> str:
        return "Email: " + super().__str__()


class Phone(Field):
    def _validate(self, value: str) -> bool:
        pattern = re.compile(r"^(?:\+?38)?[0]\d{9}$")
        return pattern.search(value) != None

    def _throw_exeption(self) -> None:
        raise IncorrectPhoneFormat()

    def __str__(self) -> str:
        return "Phone: " + super().__str__()


class Birthday(Field):
    @property
    def datetime(self) -> datetime:
        return datetime.strptime(self._value, "%d/%m/%Y")

    def _validate(self, value: str) -> bool:
        try:
            datetime.strptime(value, "%d/%m/%Y")
            return True
        except:
            return False

    def _throw_exeption(self) -> None:
        raise IncorrectDateFormat()

    def __str__(self) -> str:
        return "Birthday: " + super().__str__()
