import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import webbrowser
from json.decoder import JSONDecodeError
import spotipy.util as util

SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = 'https://www.google.com/callback/'

# Get the username from terminal
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET))
scope = 'user-read-private user-read-playback-state user-modify-playback-state'
username = '54sbqjpjdmhua20l5w55xcvsq'


#erase cache and prompt for user permission
try:
    token = util.prompt_for_user_token(username, scope, client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI)
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username)
    
spot = spotipy.Spotify(auth=token)
user = spot.current_user()
# print(json.dumps(user, sort_keys=True, indent=4))

display_name = user['display_name']
follower = user['followers']['total']

print("Bienvenidos a spotipy %s" % display_name)
while True:
    choice = input("Press 0 to search for an artist, any other key to exit ")
    if choice == '0':
        search_query = input("What artist do ya wanna search for? ")
        results = spot.search(search_query, 1, 0, 'artist')
        # print(json.dumps(results, sort_keys=True, indent=4))

        # Artist details
        artist = results['artists']['items'][0]
        artist_id = artist['id']
        print("%s is a %s artist" % (artist['name'], artist['genres'][0]))
        webbrowser.open(artist['images'][0]['url'])

        # Album details
        track_uri = []
        track_art = []
        track_num = 0

        album = spot.artist_albums(artist_id)
        album = album['items']
        for item in album:
            print("\nALBUM: " + item['name'])
            album_id = item['id']
            album_art = item['images'][0]['url']

            track_results = spot.album_tracks(album_id)
            track_results = track_results['items']

            for track_item in track_results:
                print(track_num, track_item['name'])
                track_uri.append(track_item['uri'])
                track_art.append(album_art)
                track_num += 1

        while True:
            song_selection = input("Enter song number to see album art. Press x to exit ")
            if song_selection == 'x': break
            else:
                webbrowser.open(track_art[int(song_selection)])
    else: break
