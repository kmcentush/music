from typing import TYPE_CHECKING

from music import api
from music.models import Album, Track

if TYPE_CHECKING:
    from spotipy.client import Spotify


def get_albums(client: "Spotify", ids: set[str]) -> list[Track]:
    # Get albums
    albums_dicts = api.get_albums(client, ids)

    return [Album.from_spotify(a) for a in albums_dicts]


def main():
    # Get client
    client = api.get_general_client()

    # Get tracks and album IDs
    tracks = Track.read_many()
    album_ids = {t.album_id for t in tracks}

    # Get existing albums
    existing_albums = Album.read_many()
    existing_albums_ids = {a.id for a in existing_albums}

    # Get and save new artists
    new_album_ids = album_ids - existing_albums_ids
    albums = get_albums(client, new_album_ids)
    Album.create_many(albums)


if __name__ == "__main__":
    main()
