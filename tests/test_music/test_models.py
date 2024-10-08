from music.models import Album, Artist, Features, Track


def test_artist():
    # From Spotify
    artist_dict = {
        "genres": ["canadian electronic", "complextro", "edm", "electro house", "pop dance", "progressive house"],
        "id": "2CIMQHirSU0MQqyYHq0eOx",
        "name": "deadmau5",
        "uri": "spotify:artist:2CIMQHirSU0MQqyYHq0eOx",
    }
    artist = Artist.from_spotify(artist_dict)
    assert artist.model_dump(exclude={"pkey", "create_ts", "update_ts"}) == {
        "id": "2CIMQHirSU0MQqyYHq0eOx",
        "name": "deadmau5",
        "uri": "spotify:artist:2CIMQHirSU0MQqyYHq0eOx",
        "genres": ["canadian electronic", "complextro", "edm", "electro house", "pop dance", "progressive house"],
    }

    # Create
    artist.create()

    # Hash
    assert {artist}  # type: ignore[reportUnhashable]

    # Read
    artists = Artist.read_all()
    assert artist in artists

    # Read ID
    read_artist = Artist.read_id(artist.id)
    assert artist == read_artist
    artist.pkey = read_artist.pkey  # get pkey

    # Update
    artist.name = "name2"
    artist.update()
    read_artist2 = Artist.read_id(artist.id)
    assert artist.name == read_artist2.name

    # Spoof new artist
    artist2 = artist.model_copy()
    artist2.pkey = None
    artist2.id = "new_artist"

    # Upsert
    artist.upsert()
    artist2.upsert()
    artists2 = Artist.read_all()
    assert artist in artists2
    assert artist2 in artists2
    read_artist3 = Artist.read_id(artist2.id)
    artist2.pkey = read_artist3.pkey  # get pkey

    # Delete
    artist.delete()
    artist2.delete()
    artists3 = Artist.read_all()
    assert artist not in artists3
    assert artist2 not in artists3


def test_album():
    # No need to test CRUD; Artist already does that

    # From Spotify
    album_dict = {
        "album_type": "album",
        "artists": [{"id": "4tZwfgrHOc3mvqYlEYSvVi"}],
        "genres": [],
        "id": "382ObEPsp2rxGrnsizN5TX",
        "label": "Walt Disney Records",
        "name": "TRON: Legacy Reconfigured",
        "release_date": "2011-01-01",
        "release_date_precision": "day",
        "total_tracks": 2,
        "tracks": {
            "items": [{"id": "4lteJuSjb9Jt9W1W7PIU2U"}, {"id": "66uVqkmHAc0MBUzoPhIypN"}],
        },
        "uri": "spotify:album:382ObEPsp2rxGrnsizN5TX",
    }
    album = Album.from_spotify(album_dict)
    assert album.model_dump(exclude={"pkey", "create_ts", "update_ts"}) == {
        "id": "382ObEPsp2rxGrnsizN5TX",
        "name": "TRON: Legacy Reconfigured",
        "uri": "spotify:album:382ObEPsp2rxGrnsizN5TX",
        "album_type": "album",
        "total_tracks": 2,
        "release_date": "2011-01-01",
        "release_date_precision": "day",
        "artist_ids": ["4tZwfgrHOc3mvqYlEYSvVi"],
        "track_ids": ["4lteJuSjb9Jt9W1W7PIU2U", "66uVqkmHAc0MBUzoPhIypN"],
        "genres": [],
        "label": "Walt Disney Records",
    }


def test_track():
    # No need to test CRUD; Artist already does that

    # From Spotify
    track_dict = {
        "album": {"id": "0lw68yx3MhKflWFqCsGkIs"},
        "artists": [{"id": "12Chz98pHFMPJEknJQMWvI"}],
        "disc_number": 1,
        "duration_ms": 366213,
        "explicit": False,
        "id": "7ouMYWpwJ422jRcDASZB7P",
        "name": "Knights of Cydonia",
        "track_number": 11,
        "uri": "spotify:track:7ouMYWpwJ422jRcDASZB7P",
    }
    track = Track.from_spotify(track_dict)
    assert track.model_dump(exclude={"pkey", "create_ts", "update_ts"}) == {
        "id": "7ouMYWpwJ422jRcDASZB7P",
        "name": "Knights of Cydonia",
        "uri": "spotify:track:7ouMYWpwJ422jRcDASZB7P",
        "album_id": "0lw68yx3MhKflWFqCsGkIs",
        "artist_ids": ["12Chz98pHFMPJEknJQMWvI"],
        "disc_number": 1,
        "track_number": 11,
        "duration_ms": 366213,
        "explicit": False,
    }


def test_track_features():
    # No need to test CRUD; Artist already does that

    # From Spotify
    features_dict = {
        "danceability": 0.366,
        "energy": 0.963,
        "key": 11,
        "loudness": -5.301,
        "mode": 0,
        "speechiness": 0.142,
        "acousticness": 0.000273,
        "instrumentalness": 0.0122,
        "liveness": 0.115,
        "valence": 0.211,
        "tempo": 137.114,
        "id": "7ouMYWpwJ422jRcDASZB7P",
        "time_signature": 4,
    }
    features = Features.from_spotify(features_dict)
    assert features.model_dump(exclude={"pkey", "create_ts", "update_ts"}) == {
        "id": "7ouMYWpwJ422jRcDASZB7P",
        "acousticness": 0.000273,
        "danceability": 0.366,
        "energy": 0.963,
        "instrumentalness": 0.0122,
        "key": 11,
        "liveness": 0.115,
        "loudness": -5.301,
        "mode": 0,
        "speechiness": 0.142,
        "tempo": 137.114,
        "time_signature": 4,
        "valence": 0.211,
    }
