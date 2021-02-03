import json
import os
import time

from flask import Flask, render_template, request, redirect, session, url_for
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from backend import request_functions
from backend import spotify_user_auth

app = Flask(__name__)
CORS(app)
# Set app secret
app.secret_key = os.environ['app_secret']


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
    return redirect(url_for('playlist_creation'))


@app.route('/selections', methods=['POST'])
def save_selections():
    response = request.form
    session['selections'] = response
    return redirect(url_for('auth'))


@app.route('/playlist')
def playlist_creation():
    pump_level = session['selections']['pumped']
    bpm = session['selections']['bpm']
    complete_playlist_data = request_functions.get_complete_playlist(session['auth_header'], [pump_level, bpm])
    time.sleep(5)
    return render_template('final.html', playlist_data=complete_playlist_data)


if __name__ == '__main__':
    app.run()
