import os
from typing import Any

from spotipy.cache_handler import CacheFileHandler
from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth

# Define cache location
parent_dir = os.path.dirname(os.path.realpath(__file__))
GENERAL_CACHE_PATH = os.path.join(parent_dir, "general.cache")
USER_CACHE_PATH = os.path.join(parent_dir, "user.cache")

# Define scopes
SCOPES = "playlist-read-private,user-library-read"


def _chunk_list(vals: list[Any], chunk_size: int) -> list[list[Any]]:
    return [vals[i : i + chunk_size] for i in range(0, len(vals), chunk_size)]


def get_general_client() -> Spotify:
    return Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            cache_handler=CacheFileHandler(cache_path=GENERAL_CACHE_PATH)
        )
    )


def get_user_client(open_browser: bool = False) -> Spotify:
    # Assumes environment variables `SPOTIPY_CLIENT_ID`, `SPOTIPY_CLIENT_SECRET`, and `SPOTIPY_REDIRECT_URI` are set.
    return Spotify(
        auth_manager=SpotifyOAuth(
            scope=SCOPES,
            cache_handler=CacheFileHandler(cache_path=USER_CACHE_PATH),
            redirect_uri="http://localhost:8501/callback",
            open_browser=open_browser,
        )
    )


def get_albums(client: Spotify, ids: list[str]) -> list[dict[str, Any]]:
    chunked_ids = _chunk_list(ids, chunk_size=50)  # limit per call; from Spotify documentation
    return sum([client.albums(ids)["albums"] for ids in chunked_ids], [])


def get_artists(client: Spotify, ids: list[str]) -> list[dict[str, Any]]:
    chunked_ids = _chunk_list(ids, chunk_size=50)  # limit per call; from Spotify documentation
    return sum([client.artists(ids)["artists"] for ids in chunked_ids], [])


def get_tracks(client: Spotify, ids: list[str]) -> list[dict[str, Any]]:
    chunked_ids = _chunk_list(ids, chunk_size=50)  # limit per call; from Spotify documentation
    return sum([client.tracks(ids)["tracks"] for ids in chunked_ids], [])


def get_playlist_tracks(client: Spotify, id: str) -> list[dict[str, Any]]:
    tracks = []
    result = client.playlist_items(id)
    while result:
        tracks += result["items"]
        result = client.next(result) if result["next"] else None
    return tracks


def get_user_playlists(client: Spotify) -> list[dict[str, Any]]:
    playlists = []
    result = client.current_user_playlists()
    while result:
        playlists += result["items"]
        result = client.next(result) if result["next"] else None
    return playlists


if __name__ == "__main__":
    # Authorize client to create cache
    client = get_user_client(open_browser=True)
    client.current_user()
