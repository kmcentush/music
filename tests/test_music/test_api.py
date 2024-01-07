from datetime import datetime, timezone
from typing import TYPE_CHECKING

import pytest
from music import api

if TYPE_CHECKING:
    from spotipy.client import Spotify


@pytest.fixture(scope="module")
def general_client() -> "Spotify":
    return api.get_general_client()


@pytest.fixture(scope="module")
def user_client() -> "Spotify":
    return api.get_user_client()


def test_get_albums(general_client: "Spotify"):
    album_ids = ["382ObEPsp2rxGrnsizN5TX", "1A2GTWGtFfWp7KSQTwWOyo"]
    albums = api.get_albums(general_client, album_ids)
    assert len(albums) == 2


def test_get_artists(general_client: "Spotify"):
    artist_ids = ["2CIMQHirSU0MQqyYHq0eOx", "57dN52uHvrHOxijzpIgu3E"]
    artists = api.get_artists(general_client, artist_ids)
    assert len(artists) == 2


def test_get_tracks(general_client: "Spotify"):
    track_ids = ["7ouMYWpwJ422jRcDASZB7P", "4VqPOruhp5EdPBeR92t6lQ"]
    tracks = api.get_tracks(general_client, track_ids)
    assert len(tracks) == 2


def test_get_playlist_tracks(general_client: "Spotify"):
    playlist_id = "3cEYpjA9oz9GiPac4AsH4n"
    tracks = api.get_playlist_tracks(general_client, playlist_id, limit=2)
    assert len(tracks) == 2


def test_get_user_playlists(user_client: "Spotify"):
    playlists = api.get_user_playlists(user_client, limit=2)
    assert len(playlists) == 2


def test_get_user_saved_tracks(user_client: "Spotify"):
    # Limit
    tracks = api.get_user_saved_tracks(user_client, limit=32)
    assert len(tracks) == 32

    # Since
    since = datetime(year=2024, month=1, day=1, tzinfo=timezone.utc)
    tracks2 = api.get_user_saved_tracks(user_client, since=since)
    assert len(tracks2) > 0
