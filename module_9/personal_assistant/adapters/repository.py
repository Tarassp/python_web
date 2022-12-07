import abc
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import config
from domain import model


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, product: model.AddressBook):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, user_id) -> model.AddressBook:
        raise NotImplementedError

    # @abc.abstractmethod
    # def delete(self, user_id) -> model.AddressBook:
    #     raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, product):
        self.session.add(product)

    def get(self, user_id):
        return self.session.query(model.AddressBook).filter_by(user_id=user_id).first()
