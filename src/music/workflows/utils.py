from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from music.models import BaseModel


def create_new(cls: type["BaseModel"], objs: list["BaseModel"]):
    existing = cls.read_many([o.id for o in objs])
    new = set(objs) - set(existing)
    if len(new) > 0:
        cls.create_many(new)
