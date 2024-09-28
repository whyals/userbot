import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from userbot.config import SP_CLIENT_ID, SP_CLIENT_SECRET

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SP_CLIENT_ID,
                                                           client_secret=SP_CLIENT_SECRET))

async def get_spotify_track_info(query):


    results = sp.search(q=query, type='track', limit=1)
    if results['tracks']['items']:

        track_info = results['tracks']['items'][0]
        track_name = track_info['name']
        artist_name = track_info['artists'][0]['name']
        album_name = track_info['album']['name'] if 'album' in track_info else None
        duration = track_info['duration_ms']
        spotify_url = track_info['external_urls']['spotify']
        preview_url = track_info['preview_url'] if 'preview_url' != 'https://None' in track_info else None
        album_image_url = track_info['album']['images'][0]['url']
        print(track_name, artist_name, album_name, duration, spotify_url, preview_url, album_image_url)

        return {
            'track_name': track_name,
            'artist_name': artist_name,
            'album_name': album_name,
            'duration_ms': duration,
            'spotify_link': spotify_url,
            'preview_url': preview_url,
            'album_image_url': album_image_url
        }
    else:
        return None
