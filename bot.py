from telethon.sync import TelegramClient, events
from telethon.errors import MessageTooLongError
import openai
import requests
from langdetect import detect
from PIL import Image
from io import BytesIO
import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import ssl
import certifi
import aiohttp
import asyncio
from pydub import AudioSegment
from mutagen.mp4 import MP4, MP4Cover


API_ID = '...'
API_HASH = '...'
SESSION_NAME = '...'


openai.api_key = '...'

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id='',
                                                           client_secret=''))

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


async def send_long_message(client, chat_id, message):
    MAX_MESSAGE_LENGTH = 4096
    for i in range(0, len(message), MAX_MESSAGE_LENGTH):
        part = message[i:i+MAX_MESSAGE_LENGTH]
        await client.send_message(chat_id, part)

# это как будто не трогать, и так норм работает
def get_spotify_track_url(song_title, artist_name=None):
    query = song_title
    if artist_name:
        query += f' {artist_name}'

    results = sp.search(q=query, type='track', limit=1)

    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_name = track['name']
        track_url = track['external_urls']['spotify']
        artist_name = track['artists'][0]['name']
        return f"{track_url}"
    else:
        return None


# разобраться в том хламе что он возвращает и мб перейти на другой апи который распознает музыку из файла
def search_song_on_shazam(term):
    url = "https://shazam.p.rapidapi.com/search"
    querystring = {"term": term, "locale": "en-US", "offset": "0", "limit": "5"}
    headers = {
        "x-rapidapi-key": "...",
        "x-rapidapi-host": "shazam.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json().get('tracks', {}).get('hits', [])
    else:
        return f"Ошибка при поиске песни: {response.status_code}"


def create_collage(images, output_path):
    if not images:
        return

    num_images = len(images)
    image_objects = [Image.open(BytesIO(requests.get(url).content)) for url in images]

    if num_images == 1:
        collage = image_objects[0]
    elif num_images == 2:
        width, height = image_objects[0].size
        collage = Image.new('RGB', (width * 2, height))
        collage.paste(image_objects[0], (0, 0))
        collage.paste(image_objects[1], (width, 0))
    elif num_images == 3:
        width, height = image_objects[0].size
        collage = Image.new('RGB', (width * 3, height))
        collage.paste(image_objects[0], (0, 0))
        collage.paste(image_objects[1], (width, 0))
        collage.paste(image_objects[2], (width * 2, 0))
    elif num_images == 4:
        width, height = image_objects[0].size
        collage = Image.new('RGB', (width * 2, height * 2))
        for i, img in enumerate(image_objects):
            x = (i % 2) * width
            y = (i // 2) * height
            collage.paste(img, (x, y))
    elif num_images == 5:
        width, height = image_objects[0].size
        small_width, small_height = int(width * 0.67), int(height * 0.67)

        collage_width = width * 2
        collage_height = int(height * 1.67)

        collage = Image.new('RGB', (collage_width, collage_height))

        collage.paste(image_objects[0], (0, 0))
        collage.paste(image_objects[1], (width, 0))

        collage.paste(image_objects[2].resize((small_width, small_height)), (0, height))
        collage.paste(image_objects[3].resize((small_width, small_height)), (small_width, height))
        collage.paste(image_objects[4].resize((small_width, small_height)), (2 * small_width, height))

    collage.save(output_path)

# тут надо переделать потому что очень тупо а вообще найти апишку для яндкс музыки
async def get_yandex_music_link(spotify_url):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    api_url = f"https://api.song.link/v1-alpha.1/links?url={spotify_url}"

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, ssl=ssl_context) as response:
            if response.status == 200:
                data = await response.json()
                yandex_link = data.get('linksByPlatform', {}).get('yandex', {}).get('url')
                return yandex_link
            else:
                text = await response.text()
                print(f"Ответ сервера: {text}")
                return None

'''
хотелось бы добавить скачку но потом и более качественно
def download_song(spotify_url):
    url = "https://spotify-downloader9.p.rapidapi.com/downloadSong"
    querystring = {"songId": spotify_url}

    headers = {
        "x-rapidapi-key": "...",
        "x-rapidapi-host": "spotify-downloader9.p.rapidapi.com"
    }
    
    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            download_link = data['data']['downloadLink']
            cover_url = data['data']['cover']
            return download_link, cover_url
        else:
            return None, None
    else:
        return None, None
'''

'''
def convert_mp3_to_m4a(mp3_file, m4a_file):
    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(m4a_file, format="mp4")

def add_cover_to_m4a(m4a_file, cover_url):
    cover_data = requests.get(cover_url).content
    audio = MP4(m4a_file)
    audio['covr'] = [MP4Cover(cover_data, imageformat=MP4Cover.FORMAT_JPEG)]
    audio.save()
'''

'''
@client.on(events.NewMessage(pattern=r'\?download (.+)'))
async def download_handler(event):
    spotify_url = event.pattern_match.group(1)

    download_link, cover_url = download_song(spotify_url)
    if download_link:
        file_response = requests.get(download_link)

        if file_response.status_code == 200:
            mp3_file = 'track.mp3'
            m4a_file = 'track.m4a'


            with open(mp3_file, 'wb') as f:
                f.write(file_response.content)

            convert_mp3_to_m4a(mp3_file, m4a_file)

            if cover_url:
                add_cover_to_m4a(m4a_file, cover_url)


            await client.send_file(event.chat_id, m4a_file, caption="Вот ваш трек в формате M4A с обложкой!")

            os.remove(mp3_file)
            os.remove(m4a_file)
        else:
            await event.reply("Ошибка при загрузке файла.")
    else:
        await event.reply("Не удалось получить ссылку на загрузку.")
'''


# тут по хорошему бы добавить опцию вывода цены
@client.on(events.NewMessage(pattern=r'\?ask (.+)'))
async def handler(event):
    question = event.pattern_match.group(1)
    await event.edit(f"Вопрос: {question}\nОбрабатывается...")

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": "system", "content": "Ты помощник, отвечающий на вопросы."},
            {"role": "user", "content": question}
        ]
    )
    answer = response['choices'][0]['message']['content']

    try:
        await event.edit(f"Вопрос: {question}\nОтвет: {answer}")
    except MessageTooLongError:
        await send_long_message(client, event.chat_id, f"Вопрос: {question}\nОтвет: {answer}")


# тут по хорошему тоже пересмотреть весь алгоритм, уверен можно упростить
@client.on(events.NewMessage(pattern=r'\?song(?: (.+))?'))
async def song_search_handler(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        song_query = reply_message.text
    elif event.pattern_match.group(1):
        song_query = event.pattern_match.group(1)
    else:
        await event.reply("Пожалуйста, ответьте на сообщение или введите текст для поиска песни.")
        return

    await event.edit(f"Ищу песню: {song_query}\nОбрабатывается...")

    songs = search_song_on_shazam(song_query)
    if songs:
        images = [song['track']['share']['image'] for song in songs]
        collage_path = 'collage.jpg'
        create_collage(images, collage_path)

        song_list = ""
        for i, song in enumerate(songs):
            track_title = song['track']['title']
            track_artist = song['track']['subtitle']
            spotify_link = get_spotify_track_url(track_title, track_artist)

            if spotify_link:
                yandex_link = await get_yandex_music_link(spotify_link)
                if yandex_link:
                    song_list += f"{i + 1}. <b>{track_title}</b> - <b>{track_artist}</b>:\n" \
                                 f"<b><a href='{spotify_link}'>Spotify</a></b> | " \
                                 f"<b><a href='{yandex_link}'>Yandex</a></b> | " \
                                 f"<b><a href='{yandex_link}'>Other</a></b>\n"

                else:
                    song_list += f"{i + 1}. <b>{track_title}</b> - <b>{track_artist}</b>:\n" \
                                 f"<b><a href='{spotify_link}'>Spotify</a></b> | " \
                                 "Yandex: ссылка не найдена | " \
                                 f"<b><a href='{spotify_link}'>Other</a></b>\n"
            else:
                song_list += f"{i + 1}. <b>{track_title}</b> - <b>{track_artist}</b>:\n" \
                             "Ссылки не найдены\n"
        await event.edit(f"Ищу песню: {song_query}")
        await client.send_file(event.chat_id, collage_path, caption=f"Найденные песни:\n{song_list}", parse_mode='html')
    else:
        await event.edit(f"Ищу песню: {song_query}")
        await event.reply("Песни не найдены.")

''' найти бы бесплатный хороший переводчик без ограничений...
def translate_text(text):
    try:
        lang = detect(text)

        if lang == 'ru':
            prompt = f"Переведи на английский язык: {text}"
        else:
            prompt = f"Переведи на русский язык: {text}"

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "Ты профессиональный переводчик."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']

    except Exception as e:
        return f"Ошибка при определении языка или переводе: {e}"


@client.on(events.NewMessage(pattern=r'\?tr(?: (.+))?'))
async def translate_handler(event):
    if event.is_reply:
        reply_message = await event.get_reply_message()
        original_text = reply_message.text
        translated_text = translate_text(original_text)

        await event.edit(f"Перевод: {translated_text}")

    elif event.pattern_match.group(1):
        original_text = event.pattern_match.group(1)
        translated_text = translate_text(original_text)

        await event.edit(f"Оригинал: {original_text}\nПеревод: {translated_text}")

    else:
        await event.edit("Пожалуйста, ответьте на сообщение или введите текст для перевода после комманды ?tr.")
        return


client.start()
client.run_until_disconnected()
#подробные коментарии будут позже
