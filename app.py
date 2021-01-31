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






@app.route('/recs/<mode>')
def hardcode_get_recs(mode):
    recs_data = request_functions.get_recommendations(session['auth_header'], mode, ['classical', 'jazz','funk'])
    return render_template('rec_list_test.html', recs=recs_data['tracks'])


@app.route('/createPlaylist/' , methods=['POST', 'GET'])
def create_playlist():
    #user_data = request_functions.get_user_info(session['user_auth'])
    print('createPlaylist')
    playlist_data = request_functions.create_playlist(session['auth_header'], session['user_data']['id'])
    return "heh"


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
