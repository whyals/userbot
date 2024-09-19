import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import SP_CLIENT_ID, SP_CLIENT_SECRET

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SP_CLIENT_ID,
                                                           client_secret=SP_CLIENT_SECRET))

async def get_spotify_track_url(song_title, artist_name=None):
    query = song_title
    if artist_name:
        query += f' {artist_name}'

    results = sp.search(q=query, type='track', limit=5)

    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_name = track['name']
        track_url = track['external_urls']['spotify']
        artist_name = track['artists'][0]['name']
        print (track_url)
        return f"{track_url}"
    else:
        return None
