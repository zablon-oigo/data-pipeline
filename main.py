import os
from requests import post, get
from dotenv import load_dotenv
import base64

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    result.raise_for_status()
    token = result.json()["access_token"]
    return token

def get_auth_headers(token):
    return {"Authorization": "Bearer " + token}

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