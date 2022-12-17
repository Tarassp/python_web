from __future__ import annotations
import abc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from src.adapters.orm import Base

from src.adapters.repository import AddressBookRepository, SqlAlchemyAddressBookRepository
from src.adapters.repository import UserRepository, SqlAlchemyUserRepository
from config import config


class AbstractUnitOfWork(abc.ABC):
    addressBooks: AddressBookRepository
    users: UserRepository

    def __enter__(self) -> AbstractUnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, object):
        raise NotImplementedError


def DEFAULT_SESSION_FACTORY():
    engine = create_engine(config.app_config.SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory()()

    def __enter__(self):
        self.session = self.session_factory  # type: Session
        self.addressBooks = SqlAlchemyAddressBookRepository(self.session)
        self.users = SqlAlchemyUserRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        # self.session.close()

    def delete(self, object):
        self.session.delete(object)

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
