import functools
import operator
from typing import TYPE_CHECKING

from music import api
from music.models import Artist, Track

if TYPE_CHECKING:
    from spotipy.client import Spotify


def get_artists(client: "Spotify", ids: set[str]) -> list[Artist]:
    # Get artists
    artists_dicts = api.get_artists(client, ids)

    return [Artist.from_spotify(a) for a in artists_dicts]


def main():
    # Get client
    client = api.get_general_client()

    # Get tracks and artist IDs
    tracks = Track.read_many()
    artist_ids = set(functools.reduce(operator.iadd, [t.artist_ids for t in tracks], []))

    # Get existing artists
    existing_artists = Artist.read_many()
    existing_artist_ids = {a.id for a in existing_artists}

    # Get and save new artists
    new_artist_ids = artist_ids - existing_artist_ids
    artists = get_artists(client, new_artist_ids)
    Artist.create_many(artists)


if __name__ == "__main__":
    main()
