import aiohttp

async def get_songlink_url(song_url):
    api_url = f"https://api.song.link/v1-alpha.1/links?url={song_url}"

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            if response.status == 200:
                data = await response.json()
                print(data) # что возвращает сонглинк
                # yandex_link = data.get('linksByPlatform', {}).get('yandex', {}).get('url')
                songlink_url = data.get('pageUrl')

                return  songlink_url
            else:
                text = await response.text()
                print(f"Ответ сервера: {text}")
                return None
