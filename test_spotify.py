import pytest

from spotify_pipeline import get_artist, get_token


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
