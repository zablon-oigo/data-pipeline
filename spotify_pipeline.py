from typing import Dict, Iterator

import dlt

from main import (
    get_albums,
    get_artist,
    get_artist_top_tracks_in_kenya,
    get_token,
    get_top_tracks_by_countries,
)


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


@dlt.resource(name="albums")
def spotify_album_data(artist_name: str) -> Iterator[Dict]:
    token = get_token()
    artist = get_artist(token, artist_name)
    if artist:
        albums = get_albums(token, artist["id"])
        for album in albums:
            yield album


@dlt.resource(name="track_metrics_by_country")
def spotify_track_metrics_data(artist_name: str) -> Iterator[Dict]:
    token = get_token()
    artist = get_artist(token, artist_name)
    if not artist:
        return
    artist_id = artist["id"]
    tracks = get_top_tracks_by_countries(token, artist_id)
    for track in tracks:
        yield {**track}


@dlt.resource(name="top_tracks_in_kenya")
def spotify_top_tracks_in_kenya(artist_name: str):
    token = get_token()
    artist = get_artist(token, artist_name)
    if not artist:
        return

    artist_id = artist["id"]
    tracks = get_artist_top_tracks_in_kenya(token, artist_id)

    for track in tracks:
        yield {
            "track_name": track["name"],
            "popularity": track["popularity"],
            "album_name": track["album"]["name"],
            "track_id": track["id"],
            "release_date": track["album"]["release_date"],
        }
