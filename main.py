from youtubequery import *
from spotifyquery import *
from kaekemail import *
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

if __name__ == "__main__":

    spotify_playlist_id = os.getenv("SPOTIFY_PLAYLIST_ID")
    YT_PLAYLIST_ID = os.getenv("YOUTUBE_PLAYLIST_ID")
    logging = ""
    print('Initialising..')
    # Load data from disk into dict
    # dict stores video IDs that are stored on yt
    with open("data.json", "r") as file:
        loaded_dict = json.load(file)
    logging += "Imported JSON data\n"
    print('Imported JSON data')

    # Load spotify playlist 
    spotify_playlist_items = get_spotify_playlist_tracks(spotify_playlist_id)
    logging += "Loaded data from Spotify: \n"
    print('Loaded Spotify data')
    # Find items that arent in dictionary
    items_to_add = []

    for song in spotify_playlist_items[:100]:
        if loaded_dict.get(song) is None:
            items_to_add.append(song)

    logging += "Found the following missing items: \n" + str(items_to_add) + "\n\n"
    print('Missing tracks found')
    # Foreach missing video id, get video ID 
    # and add to youtube playlist
    # add to dict
    import time
    init_yt()
    total_added_tracks = 0
    for missing in items_to_add:
        video_id = str(get_video_id(missing))
        total_added_tracks += 1
        logging += 'Adding {0} with video ID: {1}\n'.format(missing, video_id)
        print('Adding {0} with video ID: {1}'.format(missing, video_id))
        add_video_to_playlist(YT_PLAYLIST_ID, video_id)
        time.sleep(1)
        loaded_dict[missing] = video_id

    # write dict to disk
    with open("data.json", "w") as file:
        json.dump(loaded_dict, file)
    logging += "Saved data to json"
    print('Saved data to JSON')
    
    send_success_email(total_added_tracks, logging)
    print('\nVerification email sent. \n\nShutting down')

