import json
import requests
from urllib.parse import urlencode, quote

from backend import spotify_user_auth
API_VERSION = "v1/"
SPOTIFY_API_URL = "https://api.spotify.com/"+API_VERSION

with open("../credentials/credentials.txt", "r") as f:
    credentials = json.load(f)

SPOTIFY_AUTH_BASE_URL = "https://accounts.spotify.com/{}"
SPOTIFY_AUTH_URL = SPOTIFY_AUTH_BASE_URL.format('authorize')
SPOTIFY_TOKEN_URL = SPOTIFY_AUTH_BASE_URL.format('api/token')

'''
    Common Parameters
'''
REC_LIMIT = {'limit': 30}
TARGET_TEMPO = {'target_tempo': 152}

'''
    Get Recommendations
'''

def get_recommendations(auth_token, mode, genre_list):

    auth_header = spotify_user_auth.authorize(auth_token)
    genre_string = ','.join(genre_list)
    genre_param = quote(genre_string)
    rec_url = "recommendations?"
    artist_url = urlencode({'seed_artists': '7ENzCHnmJUr20nUjoZ0zZ1'})
    genre_url = urlencode({'seed_genres': genre_param})
    track_url = urlencode({'seed_tracks': '0rFHElzeddB9ymDjgpBENX'})
    limit_url = urlencode(REC_LIMIT)
    query = '&'.join([limit_url, artist_url, genre_url, track_url])
    url = ''.join([SPOTIFY_API_URL, rec_url, query])
    print(url)
    print(auth_header)
    response = requests.get(url, headers=auth_header)
    print(response.json())
    return response.json()


'''
    POST - Create Playlist
'''
