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
    return redirect(url_for('index'))






@app.route('/recs/<mode>')
def hardcode_get_recs(mode):
    recs_data = request_functions.get_recommendations(session['user_auth'], mode, ['classical', 'jazz','funk'])
    return render_template('rec_list_test.html', recs=recs_data['tracks'])

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    credentials = json.load(open("credentials/credentials.txt", 'r+'))
    app.secret_key = credentials['app_secret']
    app.run()
