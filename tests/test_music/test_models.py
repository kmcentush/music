from music.models import Album, Artist


def test_artist():
    # Create
    artist = Artist(id="id", name="name", uri="uri", genres=["genre1", "genre2"])
    artist.create()
    artist.pkey = 3

    # Read
    artists = Artist.read()
    assert artist in artists

    # Read ID
    artist2 = Artist.read_id(artist.id)
    assert artist == artist2

    # Update
    artist.name = "name2"
    artist.update()
    artist3 = Artist.read_id(artist.id)
    assert artist.id == artist3.id
    assert artist.name == artist3.name

    # Delete
    artist.delete()
    artists3 = Artist.read()
    assert artist not in artists3


def test_album():
    # No need to test CRUD, as Artist already does that
    Album(
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
