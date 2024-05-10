from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

from sqlalchemy import insert, update
from sqlmodel import JSON, Column, Field, SQLModel, UniqueConstraint, col, select

from music.data import get_session

if TYPE_CHECKING:
    from collections.abc import Iterable

    from typing_extensions import Self


def _utc_now() -> datetime:
    return datetime.now(tz=timezone.utc)


class BaseModel(SQLModel):
    __table_args__ = (UniqueConstraint("id"),)
    pkey: int | None = Field(default=None, primary_key=True)
    id: str = Field(index=True)
    create_ts: datetime | None = None
    update_ts: datetime | None = None

    def __hash__(self) -> int:
        return hash(f"{type(self)}(id={self.id})")

    def __eq__(self, other) -> bool:
        return type(self) == type(other) and self.id == other.id

    def create(self):
        return self.create_many([self])

    @classmethod
    def create_many(cls, objs: "Iterable[Self]"):
        now = _utc_now()
        to_insert = []
        for obj in objs:
            assert obj.pkey is None
            obj.create_ts = now
            obj.update_ts = now
            to_insert.append(obj.model_dump())
        if len(to_insert) > 0:
            with get_session() as session:
                session.execute(insert(cls), to_insert)
                session.commit()

    @classmethod
    def read_all(cls) -> list["Self"]:
        return cls.read_many()

    @classmethod
    def read_id(cls, id: str) -> "Self":
        return cls.read_many([id])[0]

    @classmethod
    def read_many(cls, ids: "Iterable[str] | None" = None) -> list["Self"]:
        with get_session() as session:
            statement = select(cls)
            if ids is not None:
                statement = statement.where(col(cls.id).in_(ids))
            results = session.exec(statement)
            return list(results)

    def update(self):
        return self.update_many([self])

    @classmethod
    def update_many(cls, objs: "Iterable[Self]"):
        now = _utc_now()
        to_update = []
        for obj in objs:
            assert obj.pkey is not None
            obj.update_ts = now
            to_update.append(obj.model_dump())
        if len(to_update) > 0:
            with get_session() as session:
                session.execute(update(cls), to_update)
                session.commit()

    def delete(self):
        cls = self.__class__
        assert self.pkey is not None
        with get_session() as session:
            statement = select(cls).where(cls.id == self.id)
            results = session.exec(statement)
            obj = results.one()
            session.delete(obj)
            session.commit()


class Named(BaseModel):
    name: str
    uri: str


class Album(Named, table=True):
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


class Artist(Named, table=True):
    genres: list[str] = Field(sa_column=Column(JSON))

    @classmethod
    def from_spotify(cls, item: dict[str, Any]) -> "Self":
        return cls(**item)


class Track(Named, table=True):
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


class Features(BaseModel, table=True):
    acousticness: float
    danceability: float
    energy: float
    instrumentalness: float
    key: int
    liveness: float
    loudness: float
    mode: int
    speechiness: float
    tempo: float
    time_signature: int
    valence: float

    @classmethod
    def from_spotify(cls, item: dict[str, Any]) -> "Self":
        return cls(**item)
