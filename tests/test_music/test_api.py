from typing import TYPE_CHECKING

import pytest
from music import api

if TYPE_CHECKING:
    from spotipy.client import Spotify


@pytest.fixture(scope="module")
def client() -> "Spotify":
    return api._get_general_client()


def test_get_artist(client: "Spotify"):
    artist_uris = [
        "spotify:artist:2CIMQHirSU0MQqyYHq0eOx",
        "spotify:artist:57dN52uHvrHOxijzpIgu3E",
        "spotify:artist:1vCWHaC5f2uS3yhpwWbIA6",
    ]
    artists = api.get_artists(client, artist_uris)
    assert len(artists) == 3
