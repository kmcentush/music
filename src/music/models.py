from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from music.data import get_session
from sqlmodel import JSON, Column, Field, SQLModel, UniqueConstraint, select

if TYPE_CHECKING:  # pragma: no cover
    from typing_extensions import Self


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


class BaseModel(SQLModel):
    __table_args__ = (UniqueConstraint("id"),)
    pkey: int | None = Field(default=None, primary_key=True)
    id: str
    name: str
    uri: str
    create_ts: datetime | None = None
    update_ts: datetime | None = None

    def __eq__(self, other):
        return type(self) == type(other) and self.id == other.id

    def create(self):
        assert self.pkey is None
        self.create_ts = _utc_now()
        self.update_ts = self.create_ts
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

    def update(self):
        assert self.pkey is not None
        self.update_ts = _utc_now()
        with get_session() as session:
            session.add(self)
            session.commit()

    def delete(self):
        assert self.pkey is not None
        with get_session() as session:
            session.delete(self)
            session.commit()


class Album(BaseModel, table=True):  # type: ignore[call-arg]  # this started happening in SQLModel 0.0.14: https://github.com/tiangolo/sqlmodel/discussions/732
    album_type: str
    total_tracks: int
    release_date: str
    release_date_precision: str
    artist_ids: list[str] = Field(sa_column=Column(JSON))
    track_ids: list[str] = Field(sa_column=Column(JSON))
    genres: list[str] = Field(sa_column=Column(JSON))
    label: str

    @classmethod
    def from_spotify(cls, item: dict[str, Any]) -> "Self":
        item["artist_ids"] = [a["id"] for a in item["artists"]]
        item["track_ids"] = [t["id"] for t in item["tracks"]["items"]]
        return cls(**item)


class Artist(BaseModel, table=True):  # type: ignore[call-arg]  # this started happening in SQLModel 0.0.14: https://github.com/tiangolo/sqlmodel/discussions/732
    genres: list[str] = Field(sa_column=Column(JSON))

    @classmethod
    def from_spotify(cls, item: dict[str, Any]) -> "Self":
        return cls(**item)


class Track(BaseModel, table=True):  # type: ignore[call-arg]  # this started happening in SQLModel 0.0.14: https://github.com/tiangolo/sqlmodel/discussions/732
    album_id: str
    artist_ids: list[str] = Field(sa_column=Column(JSON))
    disc_number: int
    track_number: int
    duration_ms: int
    explicit: bool

    @classmethod
    def from_spotify(cls, item: dict[str, Any]) -> "Self":
        item["album_id"] = item["album"]["id"]
        item["artist_ids"] = [a["id"] for a in item["artists"]]
        return cls(**item)
