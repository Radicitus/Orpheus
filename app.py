from flask import Flask, render_template, request, redirect, session, url_for
import json
import os
from backend import spotify_user_auth
from backend import request_functions

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/auth')
def auth():
    return redirect(spotify_user_auth.AUTH_URL)


@app.route('/callback/')
def callback():
    auth_token = request.args['code']
    session['user_auth'] = auth_token
    session['auth_header'] = spotify_user_auth.authorize(auth_token)
    return redirect(url_for('index'))


@app.route('/top/tracks/<mode>')
def top_tracks(mode):
    track_data = request_functions.get_top_tracks_id(session['auth_header'], mode)
    return
@app.route('/top/genres/<mode>')
def top_genres(mode):
    genre_data = request_functions.get_top_genres(session['auth_header'], mode)
    # artist_data = request_functions.get_top_artist_id(session['user_auth'], mode)
    return genre_data

@app.route('/top/artists/<mode>')
def top_artists(mode):
    top_artists = request_functions.get_top_artist_id(session['auth_header'], mode)
    return top_artists

@app.route('/recs/<mode>')
def hardcode_get_recs(mode):
    top_tracks = request_functions.get_top_tracks_id(session['auth_header'], mode)
    top_artists = request_functions.get_top_artist_id(session['auth_header'], mode)
    top_genres = request_functions.get_top_genres(session['auth_header'], mode)

    print(f'showing top_artists {top_artists}')
    print(f'showing top tracks{top_tracks}')
    print(f'showing top genres {top_genres}')

    recs_data = request_functions.get_recommendations(session['auth_header'], mode, top_artists, top_genres, top_tracks)
    return render_template('rec_list_test.html', recs=recs_data['tracks'])


@app.route('/createPlaylist/', methods=['POST', 'GET'])
def create_playlist():
    #user_data = request_functions.get_user_info(session['user_auth'])
    print('createPlaylist')
    playlist_data = request_functions.create_playlist(session['auth_header'], session['user_data']['id'])
    session['playlist_data'] = playlist_data.json()
    return "heh"

@app.route('/addToPlaylist/', methods=['POST', 'GET'])
def add_to_playlist():
    print('addToPlaylist')
    playlist_data = request_functions.add_to_playlist(session['auth_header'],
                                                      session['playlist_data'],
                                                      session['recs_data'])
    return "added songs hell yeah"

@app.route('/user/')
def get_user():
    user_data = request_functions.get_user_info(session['auth_header'])
    session['user_data'] = user_data
    return render_template('get_user_test.html', user=user_data)




if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    credentials = json.load(open("credentials/credentials.txt", 'r+'))
    app.secret_key = credentials['app_secret']
    app.run()
