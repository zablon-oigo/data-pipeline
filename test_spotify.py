import pytest

from spotify_pipeline import get_artist, get_token, get_top_tracks_by_countries


@pytest.fixture
def token():
    return get_token()


def test_token_is_valid(token):
    assert isinstance(token, str)
    assert len(token) > 0


def test_get_artist_success(token):
    artist = get_artist(token, "Sauti Sol")
    assert artist is not None
    assert "id" in artist
    assert artist["name"].lower() == "sauti sol"


def test_get_top_tracks_by_country(token):
    artist = get_artist(token, "Sauti Sol")
    tracks = get_top_tracks_by_countries(token, artist["id"], countries=["KE"])
    assert isinstance(tracks, list)
    assert len(tracks) > 0
    assert "track_name" in tracks[0]
