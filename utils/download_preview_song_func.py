import requests
from pydub import AudioSegment
from mutagen.mp4 import MP4, MP4Cover
import os


def download_preview(data: dict, output_file: str = "output.m4a"):

    mp3_response = requests.get(data['preview_url'], stream=True)

    if mp3_response.status_code != 200:
        print(f"Ошибка загрузки MP3 файла: {mp3_response.status_code}")
        return None

    mp3_file_path = 'temp.mp3'

    with open(mp3_file_path, 'wb') as mp3_file:
        for chunk in mp3_response.iter_content(chunk_size=1024):
            if chunk:
                mp3_file.write(chunk)

    if mp3_response.headers.get('Content-Type') != 'audio/mpeg':
        print("Загруженный файл не является MP3")
        return None

    try:
        audio = AudioSegment.from_mp3(mp3_file_path)
    except Exception as e:
        print(f"Ошибка при декодировании MP3: {e}")
        return None

    m4a_file_path = output_file
    audio.export(m4a_file_path, format="mp4")

    cover_response = requests.get(data['album_image_url'], stream=True)
    cover_data = cover_response.content

    audio_file = MP4(m4a_file_path)
    audio_file['\xa9nam'] = data['track_name']
    audio_file['\xa9ART'] = data['artist_name']
    audio_file['\xa9alb'] = data['album_name']

    audio_file['covr'] = [MP4Cover(cover_data, imageformat=MP4Cover.FORMAT_JPEG)]

    audio_file.save()

    print(f"M4A файл успешно создан: {m4a_file_path}")

    os.remove(mp3_file_path)

    return m4a_file_path
