from userbot.config import YM_TOKEN
from yandex_music import ClientAsync

client = ClientAsync(YM_TOKEN)

async def get_yandex_music_url(query):
    await client.init()

    search_result = await client.search(query, type_="track")

    if not search_result.tracks:
        print("Песни не найдены.")
        return None

    track = search_result.tracks.results[0]
    # artists = ", ".join([artist.name for artist in track.artists])
    link = f"https://music.yandex.ru/track/{track.id}"
    # cover_url = ("https://" + track.cover_uri.replace("%%", "400x400") if track.cover_uri else None)

    print(link)
    return link
