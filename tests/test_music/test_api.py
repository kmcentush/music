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
    album_ids = ["382ObEPsp2rxGrnsizN5TX", "1A2GTWGtFfWp7KSQTwWOyo", "2noRn2Aes5aoNVsU6iWThc"]
    albums = api.get_albums(general_client, album_ids)
    assert len(albums) == 3


def test_get_artists(general_client: "Spotify"):
    artist_ids = ["2CIMQHirSU0MQqyYHq0eOx", "57dN52uHvrHOxijzpIgu3E", "1vCWHaC5f2uS3yhpwWbIA6"]
    artists = api.get_artists(general_client, artist_ids)
    assert len(artists) == 3


def test_get_tracks(general_client: "Spotify"):
    track_ids = ["7ouMYWpwJ422jRcDASZB7P", "4VqPOruhp5EdPBeR92t6lQ", "2takcwOaAZWiXQijPHIx7B"]
    tracks = api.get_tracks(general_client, track_ids)
    assert len(tracks) == 3


def test_get_playlist_tracks(general_client: "Spotify"):
    playlist_id = "3cEYpjA9oz9GiPac4AsH4n"
    tracks = api.get_playlist_tracks(general_client, playlist_id)
    assert len(tracks) > 0


def test_get_user_playlists(user_client: "Spotify"):
    playlists = api.get_user_playlists(user_client)
    assert len(playlists) > 0
