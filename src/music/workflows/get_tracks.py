from typing import TYPE_CHECKING

from music import api
from music.models import Track
from music.workflows.utils import create_new

if TYPE_CHECKING:
    from spotipy.client import Spotify


def get_tracks(client: "Spotify") -> list[Track]:
    # Get tracks
    tracks_dicts = api.get_user_saved_tracks(client)

    return [Track.from_spotify(t) for t in tracks_dicts]


def main():
    # Get client
    client = api.get_user_client()

    # Get and save tracks
    tracks = get_tracks(client)
    create_new(Track, tracks)


if __name__ == "__main__":
    main()
