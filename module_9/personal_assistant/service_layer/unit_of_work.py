from __future__ import annotations
import abc
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from adapters.orm import metadata

import config
from adapters import repository

# DEFAULT_SESSION_FACTORY = sessionmaker(
#     bind=create_engine(config.get_sqlite_uri())
# )


def DEFAULT_SESSION_FACTORY():
    engine = create_engine(config.get_sqlite_uri())
    metadata.create_all(engine)
    return sessionmaker(bind=engine)

session = DEFAULT_SESSION_FACTORY()()

class AbstractUnitOfWork(abc.ABC):
    repository: repository.AbstractRepository

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


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY()):
        self.session_factory = session_factory

    def __enter__(self):
        # self.session = self.session_factory()
        self.repository = repository.SqlAlchemyRepository(session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        # self.session.expunge_all()
        # self.session.close()

    def commit(self):
        session.commit()

    def rollback(self):
        session.rollback()
