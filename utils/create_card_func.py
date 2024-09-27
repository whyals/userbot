import uuid
import os
import logging
import asyncio

from utils.main_spotify_search_func import get_spotify_track_info
from utils.yandex_music_search_func import get_yandex_music_url
from utils.songlink_search import get_songlink_url
from utils.create_card_func import create_song_card

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def song_search_handler(event, client):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        song_query = reply_message.text
        logger.info(f"Ишу {song_query}")
    elif event.pattern_match and event.pattern_match.group(1):
        song_query = event.pattern_match.group(1)
        logger.info(f"Ищу{song_query}")
    else:
        await event.reply("Пожалуйста, ответьте на сообщение или введите текст для поиска песни.")
        return


    await event.edit(f"Ищу песню: {song_query}")

    track_info = await get_spotify_track_info(song_query)
    if track_info:
        track_title = track_info['track_name']
        track_artist = track_info['artist_name']
        spotify_link = track_info['spotify_url']

        yandex_link, songlink_url = await asyncio.gather(
            get_yandex_music_url(track_title),
            get_songlink_url(spotify_link)
        )

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

        output_path = f"card_{uuid.uuid4()}.jpg"

        await create_song_card(track_info, output_path)
        logger.info(f"Карточка песни {output_path} создана.")
        await client.send_file(event.chat_id, output_path, caption=text, parse_mode='html')
        logger.info(f"Файл {output_path} отправлен.")

        os.remove(output_path)
        logger.info(f"Временный файл {output_path} удалён.")
    else:
        await event.reply("Песни не найдены.")
