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
REC_URL_FRAG = "recommendations?"
TARGET_TEMPO = {'target_tempo': 152}

USER_READ_PRIVATE = "user-read-private"

'''
    Helper
'''

def get_personalized_data(auth_token, mode, option):
    auth_header = spotify_user_auth.authorize(auth_token)
    url = ''.join([SPOTIFY_API_URL,f'me/top/{option}/'])
    response = requests.get(url, headers=auth_header)
    return response.json()

'''
    Get top Tracks
'''

def get_top_tracks_id(auth_token,mode):
    track_id_data = get_personalized_data(auth_token, mode, 'tracks')['items']
    all_track_id = []
    for i in track_id_data:
        all_track_id.append(i['id'])
    return all_track_id
'''
    Get top Artists
'''

def get_top_artist_id(auth_token,mode):
    artist_id_data = get_personalized_data(auth_token, mode, 'artists')
    all_artist_id = []
    for i in artist_id_data['items']:
        all_artist_id.append(i['id'])
    return all_artist_id

'''
    Get Top Genres
'''

def get_top_genres(auth_token,mode):
    genre_data = get_personalized_data(auth_token, mode, 'artists')
    all_genres = []
    for i in genre_data['items']:
        all_genres.extend(i['genres'])
    genre_set = set(all_genres)
    top_5 = sorted(genre_set, key=lambda x: all_genres.count(x), reverse=True)[0:5]
    return top_5

'''
    Get Recommendations
'''

def get_recommendations(auth_token, mode, genre_list):

    auth_header = spotify_user_auth.authorize(auth_token)
    genre_string = ','.join(genre_list)
    genre_param = quote(genre_string)

    artist_url = urlencode({'seed_artists': '7ENzCHnmJUr20nUjoZ0zZ1'})
    genre_url = urlencode({'seed_genres': genre_param})
    track_url = urlencode({'seed_tracks': '0rFHElzeddB9ymDjgpBENX'})
    tempo_url = urlencode(TARGET_TEMPO) #update this at some point to incorporate mode
    limit_url = urlencode(REC_LIMIT)
    query = '&'.join([limit_url, artist_url, genre_url, track_url,tempo_url])
    url = ''.join([SPOTIFY_API_URL, REC_URL_FRAG, query])
    print(url)
    print(auth_header)
    response = requests.get(url, headers=auth_header)
    print(response.json())
    return response.json()


'''
    GET - Get User Information
'''
def get_user_info(auth_token):
    auth_header = spotify_user_auth.authorize(auth_token, [USER_READ_PRIVATE])

    url = ''.join([SPOTIFY_API_URL, 'me'])
    response = requests.get(url, headers=auth_header)
    print(response.json())
    return response.json()

'''
    POST - Create Playlist
'''
def create_rec_playlist(auth_token, rec_json):
    auth_header = spotify_user_auth.authorize(auth_token, [USER_READ_PRIVATE])





