# Import the YouTubeMusicAPI module
import YouTubeMusicAPI

import os
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import google.auth
from googleapiclient.errors import HttpError


# Load OAuth 2.0 client secrets
CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'youtube'
API_VERSION = 'v3'

# Scopes required for accessing YouTube data
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

youtube = None

def init_yt():
    # Authenticate and create credentials
    credentials = None
    if os.path.exists('token.json'):
        credentials = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES, redirect_uri='http://localhost:8080/')
            credentials = flow.run_local_server(port=8080, prompt="consent", authorization_prompt_message="")
        with open('token.json', 'w') as token:
            token.write(credentials.to_json())

    global youtube
    youtube = build(API_NAME, API_VERSION, credentials=credentials)

def get_video_id(query):
    # Call the search function with the query
    result = YouTubeMusicAPI.search(query)

    # Check if a result was found
    if result:
        # Print the retrieved result
        return result['id']
    else:
        # Print a message if no result was found
        raise Exception("The video id crapped itself")
    



def add_video_to_playlist(playlist_id, video_id):
    try:
        # Add a video to the playlist
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {
                        "kind": "youtube#video",
                        "videoId": video_id
                    }
                }
            }
        )
        response = request.execute()
        print(f"Video {video_id} added to playlist {playlist_id}")
    except HttpError as e:
        print(f"An error occurred: {e}")

