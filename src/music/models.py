import os
from typing import TYPE_CHECKING

from sqlmodel import JSON, Column, Field, Session, SQLModel, create_engine, select

if TYPE_CHECKING:  # pragma: no cover
    from sqlalchemy.engine import Engine
    from typing_extensions import Self


def _get_engine() -> "Engine":
    db_file = "test_data.db" if os.getenv("TEST", None) is not None else "data.db"
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    db_path = os.path.abspath(os.path.join(parent_dir, "..", "..", db_file))
    db_url = f"sqlite:///{db_path}"
    return create_engine(db_url, echo=False)  # toggle to enable SQL statement logging


def get_session():
    engine = _get_engine()
    return Session(engine, expire_on_commit=False)


def create_db():
    engine = _get_engine()
    SQLModel.metadata.create_all(engine)


class Table(SQLModel):
    pkey: int | None = Field(default=None, primary_key=True)
    id: str  # TODO: enforce unique

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

    def create(self):
        with get_session() as session:
            session.add(self)
            session.commit()

    @classmethod
    def read(cls) -> list["Self"]:
        with get_session() as session:
            statement = select(cls)
            results = session.exec(statement)
            return list(results)

    @classmethod
    def read_id(cls, id: str) -> "Self":
        with get_session() as session:
            statement = select(cls).where(cls.id == id)
            results = session.exec(statement)
            return results.one()

    def delete(self):
        with get_session() as session:
            cls = self.__class__
            statement = select(cls).where(cls.id == self.id)
            results = session.exec(statement)
            obj = results.one()
            session.delete(obj)
            session.commit()


class Artist(Table, table=True):  # type: ignore[call-arg]  # this started happening in SQLModel 0.0.14: https://github.com/tiangolo/sqlmodel/discussions/732
    name: str
    uri: str
    genres: list[str] = Field(sa_column=Column(JSON))


if __name__ == "__main__":
    create_db()
