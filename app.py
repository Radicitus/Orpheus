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


@app.route('/complete/<mode>')
def complete_playlist(mode):
    complete_playlist_data = request_functions.get_complete_playlist(session['auth_header'], mode)
    print(complete_playlist_data)
    return render_template('complete_test.html')


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    credentials = json.load(open("credentials/credentials.txt", 'r+'))
    app.secret_key = credentials['app_secret']
    app.run()
