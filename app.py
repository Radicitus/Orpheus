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
    auth_header = spotify_user_auth.authorize(auth_token)
    session['user_auth'] = auth_token

    return redirect(url_for('index'))


@app.route('/top_artist')
def top_artists():
    auth = request_functions.get_top_artist(session['auth header'])
    print(auth)

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    credentials = json.load(open("credentials/credentials.txt", 'r+'))
    app.secret_key = credentials['app_secret']
    app.run()
