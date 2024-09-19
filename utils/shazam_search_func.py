from shazamio import Shazam

async def search_song_on_shazam(term):
    shazam = Shazam()
    result = await shazam.search_track(query=term, limit=1)
    if result:
        hits = result.get('tracks', {}).get('hits', [])
        return [{
            'title': hit['heading']['title'],
            'artist': hit['heading']['subtitle'],
            'image': hit['images']['default'],
            'url': hit['share']['href'],
            'apple_music_url': hit['stores'].get('apple', {}).get('actions', [{}])[0].get('uri')
        } for hit in hits]
    else:
        return "Ошибка при поиске песни"
