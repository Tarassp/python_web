from abc import ABC, abstractmethod
from src.domain.address_book_model import AddressBook
from src.domain.user_model import User


class UserRepository(ABC):
    @abstractmethod
    def add(self, user: User):
        raise NotImplementedError

    @abstractmethod
    def get(self, user_id: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_token(self, token):
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email: str) -> User:
        raise NotImplementedError


class SqlAlchemyUserRepository(UserRepository):
    def __init__(self, session) -> None:
        self.session = session

    def add(self, user: User):
        self.session.add(user)

    def get(self, user_id: str) -> User:
        return self.session.query(User).filter_by(id=user_id).first()

    def find_by_email(self, email: str) -> User:
        return self.session.query(User).filter_by(email=email).first()

    def get_by_token(self, token):
        return self.session.query(User).filter_by(token_cookie=token).first()

    def list(self):
        return self.session.query(User).all()


class AddressBookRepository(ABC):
    @abstractmethod
    def add(self, address_book: AddressBook):
        raise NotImplementedError

    @abstractmethod
    def get(self, user_id: str) -> AddressBook:
        raise NotImplementedError


class SqlAlchemyAddressBookRepository(AddressBookRepository):
    def __init__(self, session) -> None:
        self.session = session

    def add(self, address_book: AddressBook):
        self.session.add(address_book)

    def get(self, user_id: str) -> AddressBook:
        return self.session.query(AddressBook).filter_by(user_id=user_id).first()

    def list(self):
        return self.session.query(AddressBook).all()
