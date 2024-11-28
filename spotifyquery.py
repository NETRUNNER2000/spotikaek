import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Spotify API credentials
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")  # Redirect URI for OAuth


# Step 1: Fetch songs from Spotify playlist
def get_spotify_playlist_tracks(playlist_id):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="playlist-read-private"
    ))
    
    tracks = []
    results = sp.playlist_items(playlist_id)
    
    while results:
        for item in results['items']:
            track = item['track']
            tracks.append(
                track['name'] + " " +
                track['artists'][0]['name']
            )
        results = sp.next(results)
    
    return tracks