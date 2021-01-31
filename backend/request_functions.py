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
REC_LIMIT = {'limit': 30 }

'''
    Get Recommendations
'''
def get_recommendations(auth_token, genre_list):
    auth_header = spotify_user_auth.authorize(auth_token)
    genre_string = ','.join(genre_list)
    genre_param = quote(genre_string)
    limit = urlencode(REC_LIMIT)
    url = SPOTIFY_API_URL + "recommendations?"+limit+genre_param
    response = requests.get(url, headers=auth_header)
    print(response.json())
    return response.json()