from telethon import events

from utils.shazam_search_func import search_song_on_shazam
from utils.spotify_search_func import get_spotify_track_url
from utils.yandex_music_search_func import get_yandex_music_url
from utils.songlink_search import get_songlink_url
from utils.create_collage_func import create_collage


@events.register(events.NewMessage(pattern=r'\?song(?: (.+))?'))
async def song_search_handler(client, event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        song_query = reply_message.text
    elif event.pattern_match.group(1):
        song_query = event.pattern_match.group(1)
    else:
        await event.reply("Пожалуйста, ответьте на сообщение или введите текст для поиска песни.")
        return

    await event.edit(f"Ищу песню: {song_query}\nОбрабатывается...")

    songs = await search_song_on_shazam(song_query)
    if songs:
        images = [song['image'] for song in songs]
        titles_and_artists = [(song['title'], song['artist']) for song in songs]
        collage_path = 'collage.jpg'

        create_collage(images, titles_and_artists, collage_path)

        song_list = ""
        for i, song in enumerate(songs):
            track_title = song['title']
            track_artist = song['artist']

            spotify_link = await get_spotify_track_url(track_title, track_artist)
            yandex_link = await get_yandex_music_url(track_title)
            songlink_url = await get_songlink_url(spotify_link or yandex_link)

            if spotify_link and yandex_link and songlink_url:
                song_list += f"{i + 1}. <b>{track_title}</b> - <b>{track_artist}</b>:\n" \
                             f"<b><a href='{spotify_link}'>Spotify</a></b> | " \
                             f"<b><a href='{yandex_link}'>Yandex</a></b> | " \
                             f"<b><a href='{songlink_url}'>Other</a></b>\n"
            elif spotify_link and songlink_url:
                song_list += f"{i + 1}. <b>{track_title}</b> - <b>{track_artist}</b>:\n" \
                             f"<b><a href='{spotify_link}'>Spotify</a></b> | " \
                             f"<b><a href='{songlink_url}'>Other</a></b>\n"
            elif yandex_link and songlink_url:
                song_list += f"{i + 1}. <b>{track_title}</b> - <b>{track_artist}</b>:\n" \
                             f"<b><a href='{yandex_link}'>Yandex</a></b> | " \
                             f"<b><a href='{songlink_url}'>Other</a></b>\n"
            else:
                song_list += f"{i + 1}. <b>{track_title}</b> - <b>{track_artist}</b>:\n" \
                             f"<b><a href='{songlink_url}'>Other</a></b>\n"
        await event.edit(f"Ищу песню: {song_query}")
        await client.send_file(event.chat_id, collage_path, caption=f"Найденные песни:\n{song_list}", parse_mode='html')
    else:
        await event.edit(f"Ищу песню: {song_query}")
        await event.reply("Песни не найдены.")
