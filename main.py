import os
from requests import post, get
from typing import Iterator, Dict, List
from dotenv import load_dotenv
import base64

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token() -> str:
    auth_bytes = f"{client_id}:{client_secret}".encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    resp = post("https://accounts.spotify.com/api/token", headers=headers, data=data)
    resp.raise_for_status()
    return resp.json()["access_token"]

def get_auth_headers(token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token}"}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_headers(token)
    query = f"?q={artist_name}&type=artist&limit=1"
    query_url = url + query
    result = get(query_url, headers=headers)
    result.raise_for_status()
    json_result = result.json()["artists"]["items"]
    
    if not json_result:
        print("No artist with this name exists...")
        return None

    return json_result[0]



def get_artist_top_tracks_in_kenya(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=KE"
    headers = get_auth_headers(token)
    result = get(url, headers=headers)
    result.raise_for_status()
    json_result = result.json()["tracks"]
    return json_result


token = get_token()
artist = search_for_artist(token, "Simmy")
if artist:
    artist_id = artist["id"]
    songs = get_artist_top_tracks_in_kenya(token, artist_id)

    for idx, song in enumerate(songs):
        print(f"{idx + 1}. {song['name']}")