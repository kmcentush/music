from datetime import datetime, timezone
from typing import TYPE_CHECKING

from music import api
from music.models import Track

if TYPE_CHECKING:
    from spotipy.client import Spotify


def get_tracks(client: "Spotify", since: datetime) -> list[Track]:
    # Get tracks
    tracks_dicts = api.get_user_saved_tracks(client, since=since)

    return [Track.from_spotify(t["track"]) for t in tracks_dicts]


def main():
    # Get client
    client = api.get_user_client()

    # Get tracks since specified date
    since = datetime(year=2024, month=1, day=1, tzinfo=timezone.utc)
    tracks = get_tracks(client, since)

    # Save new tracks
    existing_tracks = Track.read_many([t.id for t in tracks])
    new_tracks = set(tracks) - set(existing_tracks)
    Track.create_many(new_tracks)


if __name__ == "__main__":
    main()
