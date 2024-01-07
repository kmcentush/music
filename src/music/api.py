import os
from typing import TYPE_CHECKING, Any

from spotipy.cache_handler import CacheFileHandler
from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from tqdm.auto import tqdm

# Define cache location
parent_dir = os.path.dirname(os.path.realpath(__file__))
GENERAL_CACHE_PATH = os.path.join(parent_dir, "general.cache")
USER_CACHE_PATH = os.path.join(parent_dir, "user.cache")

# Define scopes
SCOPES = "playlist-read-private,user-library-read"

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable


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


def _handle_next(
    client: "Spotify", func: "Callable", *args, limit: int | None = None, bar_description: str | None = None, **kwargs
) -> list[dict[str, Any]]:
    out = []
    with tqdm(desc=bar_description, total=limit) as bar:
        result = func(*args, **kwargs)
        bar.total = min(limit, result["total"]) if limit else result["total"]
        while result:
            out += result["items"]
            bar.update(len(result["items"]))
            if limit and len(out) >= limit:
                bar.n = limit
                out = out[:limit]
                break
            result = client.next(result) if result["next"] else None
        return out


def get_playlist_tracks(client: Spotify, id: str, limit: int | None = None) -> list[dict[str, Any]]:
    return _handle_next(client, client.playlist_items, id, limit=limit, bar_description="Getting playlist tracks")


def get_user_playlists(client: Spotify, limit: int | None = None) -> list[dict[str, Any]]:
    return _handle_next(client, client.current_user_playlists, limit=limit, bar_description="Getting user playlists")


def get_user_saved_tracks(client: Spotify, limit: int | None = None) -> list[dict[str, Any]]:
    return _handle_next(
        client, client.current_user_saved_tracks, limit=limit, bar_description="Getting user saved tracks"
    )


if __name__ == "__main__":
    # Authorize client to create cache
    client = get_user_client(open_browser=True)
    client.current_user()
