from typing import TYPE_CHECKING

from music import api
from music.models import Features, Track

if TYPE_CHECKING:
    from spotipy.client import Spotify


def get_features(client: "Spotify", ids: set[str]) -> list[Track]:
    # Get features
    features_dicts = api.get_features(client, ids)

    return [Features.from_spotify(f) for f in features_dicts]


def main():
    # Get client
    client = api.get_general_client()

    # Get tracks and track IDs
    tracks = Track.read_many()
    track_ids = {t.id for t in tracks}

    # Get existing features
    existing_features = Features.read_many()
    existing_features_ids = {f.id for f in existing_features}

    # Get and save new features
    new_features_ids = track_ids - existing_features_ids
    features = get_features(client, new_features_ids)
    Features.create_many(features)


if __name__ == "__main__":
    main()
