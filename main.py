import base64
import os
from typing import Dict, List

from dotenv import load_dotenv
from requests import get, post

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
base_url = "https://api.spotify.com/v1"
auth_url = "https://accounts.spotify.com/api/token"


def get_token() -> str:
    auth_bytes = f"{client_id}:{client_secret}".encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type": "client_credentials"}
    resp = post(f"{auth_url}", headers=headers, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]


def get_auth_headers(token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def get_artist(token: str, name: str) -> Dict:
    url = f"{base_url}/search?q={name}&type=artist&limit=1"
    resp = get(url, headers=get_auth_headers(token))
    resp.raise_for_status()
    artists = resp.json().get("artists", {}).get("items", [])
    return artists[0] if artists else None


def get_artist_top_tracks_in_kenya(token, artist_id):
    url = f"{base_url}/artists/{artist_id}/top-tracks?country=KE"
    headers = get_auth_headers(token)
    result = get(url, headers=headers)
    result.raise_for_status()
    json_result = result.json()["tracks"]
    return json_result


def get_albums(token: str, artist_id: str) -> List[Dict]:
    url = f"{base_url}/artists/{artist_id}/albums"
    headers = get_auth_headers(token)
    albums = []
    params = {"include_groups": "album,single,compilation", "limit": 50, "offset": 0}

    while True:
        resp = get(url, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        items = data.get("items", [])

        for album in items:
            albums.append(
                {
                    "album_id": album["id"],
                    "album_name": album["name"],
                    "release_date": album["release_date"],
                    "total_tracks": album["total_tracks"],
                    "album_type": album["album_type"],
                    "artist_id": artist_id,
                }
            )

        if not data.get("next"):
            break
        params["offset"] += params["limit"]

    return albums


def get_top_tracks_by_countries(
    token: str, artist_id: str, countries: List[str] = None
) -> List[Dict]:

    if countries is None:
        countries = ["US", "GB", "ZA", "NG", "DE", "BR", "IN", "FR", "JP", "CA"]

    headers = get_auth_headers(token)
    all_tracks = []

    for country in countries:
        url = f"{base_url}/artists/{artist_id}/top-tracks?country={country}"
        resp = get(url, headers=headers)
        resp.raise_for_status()
        tracks = resp.json()["tracks"]

        for track in tracks:
            all_tracks.append(
                {
                    "country": country,
                    "track_name": track["name"],
                    "track_id": track["id"],
                    "popularity": track["popularity"],
                    "album_name": track["album"]["name"],
                    "release_date": track["album"]["release_date"],
                }
            )

    return all_tracks
