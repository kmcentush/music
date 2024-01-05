from music.models import Artist


def test_artist():
    # Create
    artist = Artist(id="id", name="name", uri="uri", genres=["genre1", "genre2"])
    artist.create()

    # Read
    artists = Artist.read()
    assert len(artists) == 1
    assert artist in artists

    # Read ID
    artist2 = Artist.read_id(artist.id)
    assert artist == artist2

    # Update
    # TODO

    # Delete
    artist.delete()
    artists2 = Artist.read()
    assert len(artists2) == 0
