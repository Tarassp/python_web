from __future__ import annotations
from sqlalchemy import create_engine, String, Text, ForeignKey, Table, Column, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from scrapy.utils.project import get_project_settings
from datetime import date


class Base(DeclarativeBase):
    ...


def db_connect():
    return create_engine(get_project_settings().get("DB_CONNECTION"))


def create_tables(engine):
    Base.metadata.create_all(engine)


class Author(Base):
    __tablename__ = "authors"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    birthdate: Mapped[date] = mapped_column(Date)
    bio: Mapped[str] = mapped_column(Text)
    quotes: Mapped[list["Quote"]] = relationship(back_populates="author")


association_table = Table(
    "association_table",
    Base.metadata,
    Column("quote_id", ForeignKey("quotes.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Quote(Base):
    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    tags: Mapped[list[Tag]] = relationship(secondary=association_table, back_populates="quotes")
    author_name: Mapped[str] = mapped_column(ForeignKey('authors.name'))
    author: Mapped["Author"] = relationship(back_populates="quotes")

    def __repr__(self):
        return f"Quote(id={self.id!r}, text={self.text!r}, author_id={self.author!r}"


class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))
    quotes: Mapped[list[Quote]] = relationship(secondary=association_table, back_populates="tags")

    def __repr__(self):
        return f"Tag(id={self.id!r}, name={self.name!r}, quotes={self.quotes!r})"

