from music.models import Album, Artist, Track


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
    assert {artist}

    # Read
    artists = Artist.read_all()
    assert artist in artists

    # Read ID
    artist2 = Artist.read_id(artist.id)
    assert artist == artist2
    artist.pkey = artist2.pkey  # get pkey

    # Update
    artist.name = "name2"
    artist.update()
    artist3 = Artist.read_id(artist.id)
    assert artist.name == artist3.name

    # Delete
    artist.delete()
    artists3 = Artist.read_all()
    assert artist not in artists3


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
