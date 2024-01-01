from typing import Any

from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyClientCredentials  # SpotifyOAuth

# Define scopes
# SCOPES = "playlist-read-private,user-library-read"


def _get_general_client() -> Spotify:
    return Spotify(client_credentials_manager=SpotifyClientCredentials())


# def _get_user_client() -> Spotify:
#     # Assumes environment variables `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`, and `SPOTIPY_REDIRECT_URI` are set.
#     return Spotify(auth_manager=SpotifyOAuth(scope=SCOPES, open_browser=False))


def get_artists(client: Spotify, ids: list[str]) -> list[dict[str, Any]]:
    return client._get("artists/?ids=" + ",".join(ids))["artists"]
