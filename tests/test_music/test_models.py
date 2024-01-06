from music.models import Album, Artist


def test_artist():
    # Create
    artist = Artist(id="id", name="name", uri="uri", genres=["genre1", "genre2"])
    artist.create()

    # Read
    artists = Artist.read()
    assert artist in artists

    # Read ID
    artist2 = Artist.read_id(artist.id)
    assert artist == artist2

    # Update
    # TODO

    # Delete
    artist.delete()
    artists2 = Artist.read()
    assert artist not in artists2


def test_album():
    # Create
    album = Album(
        id="id",
        name="name",
        uri="uri",
        album_type="single",
        total_tracks=1,
        release_date="2023-12",
        release_date_precision="month",
        artist_ids=["a", "b"],
        track_ids=["a", "b"],
        genres=["genre1", "genre2"],
        label="label",
    )
    album.create()

    # Read
    albums = Album.read()
    assert album in albums

    # Read ID
    album2 = Album.read_id(album.id)
    assert album == album2

    # Update
    # TODO

    # Delete
    album.delete()
    albums2 = Artist.read()
    assert album not in albums2
