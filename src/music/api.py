import os
from datetime import datetime
from typing import TYPE_CHECKING, Any

from spotipy.cache_handler import CacheFileHandler
from spotipy.client import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from tqdm.auto import tqdm

if TYPE_CHECKING:  # pragma: no cover
    from collections.abc import Callable, Collection

# Define cache location
parent_dir = os.path.dirname(os.path.realpath(__file__))
GENERAL_CACHE_PATH = os.path.join(parent_dir, "general.cache")
USER_CACHE_PATH = os.path.join(parent_dir, "user.cache")

# Define scopes
SCOPES = "playlist-read-private,user-library-read"


def _chunk_list(vals: "Collection[Any]", chunk_size: int) -> list[list[Any]]:
    list_vals = list(vals)
    return [list_vals[i : i + chunk_size] for i in range(0, len(list_vals), chunk_size)]


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


def _handle_chunked_ids(
    func: "Callable",
    total: int,
    chunked_ids: list[list[str]],
    key: str | None = None,
    *args,
    bar_description: str | None = None,
    **kwargs,
) -> list[dict[str, Any]]:
    items = []
    with tqdm(total=total, desc=bar_description) as bar:
        for ids in chunked_ids:
            new_items = func(ids, *args, **kwargs)
            if key is not None:
                new_items = new_items[key]
            items += new_items
            bar.update(len(new_items))
    return items


def _handle_next(
    client: "Spotify",
    func: "Callable",
    *args,
    limit: int | None = None,
    bar_description: str | None = None,
    early_break: "Callable | None" = None,
    **kwargs,
) -> list[dict[str, Any]]:
    # Get first result
    items = []
    result = func(*args, **kwargs)
    with tqdm(desc=bar_description, total=limit) as bar:
        # Update bar total
        bar.total = min(limit, result["total"]) if limit else result["total"]

        # Handle result
        while result:
            # Get items and update bar progress
            new_items = result["items"]
            items += new_items
            bar.update(len(new_items))

            # Maybe break
            num_items = len(items)
            if limit is not None and num_items >= limit:
                bar.n = limit
                items = items[:limit]
                break
            if early_break is not None and early_break(items):
                bar.total = num_items
                bar.n = num_items
                break

            # Get next result
            result = client.next(result) if result["next"] else None

        return items


def get_albums(client: Spotify, ids: "Collection[str]") -> list[dict[str, Any]]:
    chunked_ids = _chunk_list(ids, chunk_size=20)  # limit per call; from Spotify documentation
    return _handle_chunked_ids(
        client.albums, total=len(ids), chunked_ids=chunked_ids, key="albums", bar_description="Getting albums"
    )


def get_artists(client: Spotify, ids: "Collection[str]") -> list[dict[str, Any]]:
    chunked_ids = _chunk_list(ids, chunk_size=50)  # limit per call; from Spotify documentation
    return _handle_chunked_ids(
        client.artists, total=len(ids), chunked_ids=chunked_ids, key="artists", bar_description="Getting artists"
    )


def get_tracks(client: Spotify, ids: "Collection[str]") -> list[dict[str, Any]]:
    chunked_ids = _chunk_list(ids, chunk_size=50)  # limit per call; from Spotify documentation
    return _handle_chunked_ids(
        client.tracks, total=len(ids), chunked_ids=chunked_ids, key="tracks", bar_description="Getting tracks"
    )


def get_playlist_tracks(client: Spotify, id: str, limit: int | None = None) -> list[dict[str, Any]]:
    return _handle_next(client, client.playlist_items, id, limit=limit, bar_description="Getting playlist tracks")


def get_user_playlists(client: Spotify, limit: int | None = None) -> list[dict[str, Any]]:
    return _handle_next(client, client.current_user_playlists, limit=limit, bar_description="Getting user playlists")


def get_user_saved_tracks(
    client: Spotify, limit: int | None = None, since: "datetime | None" = None
) -> list[dict[str, Any]]:
    # Break early when `since` is specified
    def early_break(tracks: list[dict[str, Any]]) -> bool:
        oldest_track = tracks[-1]
        oldest_dt = datetime.fromisoformat(oldest_track["added_at"].replace("Z", "+00:00"))
        return oldest_dt < since  # type: ignore[operator]  # function is only called when `since` is not None

    # Get tracks
    tracks = _handle_next(
        client,
        client.current_user_saved_tracks,
        limit=limit,
        early_break=early_break if since is not None else None,
        bar_description="Getting user saved tracks",
    )

    # Maybe filter
    if since is not None:
        # Determine what to exclude; since things are ordered newest -> oldest, start from the end
        keep_through = -1
        for i in range(1, len(tracks) + 1):
            track = tracks[-i]
            track_dt = datetime.fromisoformat(track["added_at"].replace("Z", "+00:00"))
            if track_dt < since:
                keep_through -= 1
            else:  # things are ordered so we can break early
                break

        # Filter
        if keep_through < -1:
            tracks = tracks[0 : keep_through + 1]

    return tracks


def get_features(client: Spotify, ids: "Collection[str]") -> list[dict[str, Any]]:
    chunked_ids = _chunk_list(ids, chunk_size=100)  # limit per call; from Spotify documentation
    return _handle_chunked_ids(
        client.audio_features, total=len(ids), chunked_ids=chunked_ids, bar_description="Getting features"
    )


if __name__ == "__main__":
    # Authorize client to create cache
    client = get_user_client(open_browser=True)
    client.current_user()
