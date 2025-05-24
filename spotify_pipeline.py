from typing import Dict, Iterator

import dlt

from main import get_artist, get_token


@dlt.resource(name="artists")
def spotify_artist_data(artist_name: str) -> Iterator[Dict]:
    token = get_token()
    artist = get_artist(token, artist_name)
    if artist:
        yield {
            "id": artist["id"],
            "name": artist["name"],
            "genres": artist["genres"],
            "followers": artist["followers"]["total"],
            "popularity": artist["popularity"],
        }
