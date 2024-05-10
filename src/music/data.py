import os
from typing import TYPE_CHECKING

from sqlmodel import Session, SQLModel, create_engine

if TYPE_CHECKING:
    from sqlalchemy.engine import Engine


def _get_engine() -> "Engine":
    db_file = "test_data.db" if os.getenv("TEST", None) is not None else "data.db"
    parent_dir = os.path.dirname(os.path.realpath(__file__))
    db_path = os.path.abspath(os.path.join(parent_dir, "..", "..", db_file))
    db_url = f"sqlite:///{db_path}"
    return create_engine(db_url, echo=False)  # toggle to enable SQL statement logging


def get_session() -> Session:
    engine = _get_engine()
    return Session(engine, expire_on_commit=False)


def create_db():
    engine = _get_engine()
    SQLModel.metadata.create_all(engine)


if __name__ == "__main__":
    import music.models  # noqa: F401  # import models before creating database

    create_db()
