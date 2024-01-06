import os
from typing import Any

from spotipy.cache_handler import CacheFileHandler
from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyClientCredentials  # SpotifyOAuth

# Define cache location
parent_dir = os.path.dirname(os.path.realpath(__file__))
GENERAL_CACHE_PATH = os.path.join(parent_dir, "general.cache")
USER_CACHE_PATH = os.path.join(parent_dir, "user.cache")

# Define scopes
SCOPES = "playlist-read-private,user-library-read"


def _get_general_client() -> Spotify:
    return Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            cache_handler=CacheFileHandler(cache_path=GENERAL_CACHE_PATH)
        )
    )


# def _get_user_client() -> Spotify:
#     # Assumes environment variables `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`, and `SPOTIPY_REDIRECT_URI` are set.
#     return Spotify(
#         auth_manager=SpotifyOAuth(
#             scope=SCOPES, cache_handler=CacheFileHandler(cache_path=USER_CACHE_PATH), open_browser=False
#         )
#     )


def get_albums(client: Spotify, ids: list[str]) -> list[dict[str, Any]]:
    return client.albums(ids)["albums"]


def get_artists(client: Spotify, ids: list[str]) -> list[dict[str, Any]]:
    return client.artists(ids)["artists"]
