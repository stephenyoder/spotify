import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials

artist_uri = 'spotify:artist:2YZyLoL8N0Wb9xBt1NhZWg'
# client_id = os.getenv('SPOTIPY_CLIENT_ID')
# client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
# print(client_id, client_secret)

spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = spotify.artist_albums(artist_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

#print(albums[0]['name'])
for album in albums:
    print(album['name'])