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

def get_personalized_data(auth_header, mode, option):
    # auth_header = spotify_user_auth.authorize(auth_header)
    url = ''.join([SPOTIFY_API_URL,f'me/top/{option}/'])
    response = requests.get(url, headers=auth_header)
    return response.json()

'''
    Get top Tracks - 2 tracks
'''

def get_top_tracks_id(auth_header,mode):
    track_id_data = get_personalized_data(auth_header, mode, 'tracks')['items']
    all_track_id = []
    for i in track_id_data:
        all_track_id.append(i['id'])
    print(all_track_id)
    return all_track_id[:2]

'''
    Get top Artists - just one
'''

def get_top_artist_id_and_genres(auth_header,mode):
    artist_id_data = get_personalized_data(auth_header, mode, 'artists')
    all_artist_id = []
    all_genres = []
    for i in artist_id_data['items']:
        all_artist_id.append(i['id'])
        all_genres.extend(i['genres'])
    genre_set = set(all_genres)
    print(all_artist_id)
    top_5 = sorted(genre_set, key=lambda x: all_genres.count(x), reverse=True)[0:5]
    print(top_5)
    return [all_artist_id[0],top_5[3:]]

'''
    Get Top Genres - 2 genres (This is commented out to save API calls)
'''

# def get_top_genres(auth_header,mode):
#     genre_data = get_personalized_data(auth_header, mode, 'artists')
#     all_genres = []
#     for i in genre_data['items']:
#         all_genres.extend(i['genres'])
#     genre_set = set(all_genres)
#     top_5 = sorted(genre_set, key=lambda x: all_genres.count(x), reverse=True)[0:5]
#     print(top_5)
#     return top_5[3:]

'''
    Get Recommendations
'''

def get_recommendations(auth_header, mode, artist_list, genre_list, track_list):
    
    auth_header = auth_header
    genre_string = ','.join(genre_list)
    track_list = ','.join(track_list)

    artist_url = urlencode({'seed_artists': artist_list})
    genre_url = urlencode({'seed_genres': genre_string})
    track_url = urlencode({'seed_tracks': track_list})
    tempo_url = urlencode(TARGET_TEMPO) #update this at some point to incorporate mode
    limit_url = urlencode(REC_LIMIT)
    query = '&'.join([limit_url, artist_url, genre_url, track_url, tempo_url])
    url = ''.join([SPOTIFY_API_URL, REC_URL_FRAG, query])
    print(url)
    print(auth_header)
    response = requests.get(url, headers=auth_header)
    print(response.json())
    return response.json()

'''
    Handle everything
'''

def handle_everything():
    pass

'''
    GET - Get User Information
'''
def get_user_info(auth_header):
    auth_header = auth_header

    url = ''.join([SPOTIFY_API_URL, 'me'])
    print(url)
    response = requests.get(url, headers=auth_header)
    print(response.json())
    return response.json()


'''
    POST - Create Playlist
'''
def create_playlist(auth_header, user_id):
    auth_header = auth_header
    body = json.dumps({
        "name": "very cool music i super promise",
        "description": "read the title",
        "public": True
        })
    url = ''.join([SPOTIFY_API_URL, 'users/', user_id, '/playlists'])
    print(url)
    response = requests.post(url, headers=auth_header, data=body)
    print(response)
    print(response.json())
    return response


'''
    POST - Add Recommendations to Playlist
'''
def add_to_playlist(auth_header, rec_list, playlist_id):
    auth_header = auth_header
    uri_list = []
    for rec in rec_list:
        uri_list.append(rec['uri'])

    body = json.dumps({
        'uris': uri_list
    })

    url = ''.join([SPOTIFY_API_URL, 'playlists/', playlist_id, '/tracks'])
    response = requests.post(url, headers=auth_header, data=body)
    print('add_to_playlist: {}'.format(url))
    print(response.json())
    return response


'''
    
'''


def get_complete_playlist(auth_header, mode):
    '''

    :param auth_header:
    :param mode:
    :return:
    '''
    #Retrieve the user's top artists, genres, and tracks
    artist_and_genre = get_top_artist_id_and_genres(auth_header, mode)
    artist_list = artist_and_genre[0]
    genre_list = artist_and_genre[1]
    track_list = get_top_tracks_id(auth_header, mode)

    #Get recommended songs based on the above lists
    rec_data = get_recommendations(auth_header, mode, artist_list, genre_list, track_list)

    #Get the user's ID
    user = get_user_info(auth_header)

    #Create a playlist for user
    playlist_data = create_playlist(auth_header, user['id'])

    #Add recommended songs to playlist
    finished_playlist_data = add_to_playlist(auth_header, rec_data['tracks'], playlist_data.json()['id'])


    return str(playlist_data.json())


def build_playlist():
    return None