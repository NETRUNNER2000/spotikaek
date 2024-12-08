import os
from flask import Flask, Response, redirect, request, session, url_for, jsonify

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False
app.config['JSONIFY_MIMETYPE'] = 'application/json'

app.config['SECRET_KEY'] = os.urandom(64)

client_id = "eae52e4eba8d4f839ab7da4a487e766a"
client_secret = "fc7859d88a924b7ca6c7e7e5c7de3f4a"
redirect_uri = "http://localhost:5000/callback"
scope="playlist-read-private"

cache_handler = FlaskSessionCacheHandler(session)
sp_auth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=False
)

sp = Spotify(auth_manager=sp_auth)

@app.route('/')
def home():
    if not sp_auth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_auth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('get_playlist'))

@app.route('/callback')
def callback():
    sp_auth.get_access_token(request.args['code'])
    return redirect(url_for('get_playlist'))

@app.route('/get_playlist', methods=['GET'])
def get_playlist():
    if not sp_auth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_auth.get_authorize_url()
        return redirect(auth_url)
    tracks = []
    results = sp.playlist_items('1GAh4L312KvuPG2UgwJ9wU')
    while results:
        for item in results['items']:
            track = item['track']
            if track:  # Ensure it's a valid track
                track_name = track['name']
                artist_name = track['artists'][0]['name']
                tracks.append(f'{track_name} {artist_name}')
        # Get next page of results
        results = sp.next(results) if results['next'] else None
    #playlist_html = '<br>'.join(f'{track_name} - {artist_name}' for track_name, artist_name in tracks)
    data = {"message": "This is a JSON response", "status": "success"}
    response = jsonify(tracks)
    response.headers['Content-Type'] = 'application/json; charset=utf-8'  # Ensure correct header
    return response

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)