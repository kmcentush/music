from typing import TYPE_CHECKING

from music import api
from music.models import Track

if TYPE_CHECKING:
    from music.models import BaseModel
    from spotipy.client import Spotify


def create_new(cls: type["BaseModel"], objs: list["BaseModel"]):
    existing = cls.read_many([o.id for o in objs])
    new = set(objs) - set(existing)
    if len(new) > 0:
        cls.create_many(new)


def get_tracks(client: "Spotify") -> list[Track]:
    # Get tracks
    tracks_dicts = api.get_user_saved_tracks(client)

    return [Track.from_spotify(t["track"]) for t in tracks_dicts]


def main():
    # Get client
    client = api.get_user_client()

    # Get and save tracks
    tracks = get_tracks(client)
    create_new(Track, tracks)


if __name__ == "__main__":
    main()
