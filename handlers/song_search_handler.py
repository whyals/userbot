from telethon import events

from utils.main_spotify_search_func import get_spotify_track_info
from utils.yandex_music_search_func import get_yandex_music_url
from utils.songlink_search import get_songlink_url
from utils.create_card_func import create_song_card
from utils.download_preview_song_func import download_preview

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


    track_info = await get_spotify_track_info(song_query)
    if track_info:
        track_title = track_info['track_name']
        track_artist = track_info['artist_name']
        spotify_link = track_info['spotify_link']
        yandex_link = await get_yandex_music_url(track_title)
        songlink_url = await get_songlink_url(spotify_link or yandex_link)

        text = f"Похоже, что вы искали:\n" \
               f"<b>{track_title}</b> - <b>{track_artist}</b>:\n"

        links = []
        if spotify_link:
            links.append(f"<b><a href='{spotify_link}'>Spotify</a></b>")
        if yandex_link:
            links.append(f"<b><a href='{yandex_link}'>Yandex</a></b>")
        if songlink_url:
            links.append(f"<b><a href='{songlink_url}'>Other</a></b>")

        text += " | ".join(links) + "\n"

        output_path = "card_1.jpg"
        await create_song_card(track_info, output_path)
        await client.send_file(event.chat_id, output_path, caption=text, parse_mode='html')
        if track_info['preview_url'] != None:
            audio_path = download_preview(track_info)
            await client.send_file(event.chat_id, audio_path, caption='__________________________', parse_mode='html',
                                   force_document=False,
                                   performer=track_info['artist_name'],
                                   title=track_info['track_name'])


        await event.edit(f"Ищу песню: {song_query}")
    else:
        await event.edit(f"Ищу песню: {song_query}")
        await event.reply("Песни не найдены.")
