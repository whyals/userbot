from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import requests
from io import BytesIO


async def create_song_card(track_info, output_path):

    track_name = track_info['track_name']
    artist_name = track_info['artist_name']
    album_name = track_info['album_name']
    album_image_url = track_info['album_image_url']

    track_name_pix = len(track_name) * 154
    artist_album_pix = (len(artist_name) + 3 + len(album_name)) * 65

    background_color = (18, 18, 18)
    cover_width = 640
    cover_height = 640
    card_width = cover_width + 2 * 80 + max(3500, track_name_pix, artist_album_pix)
    card_height = cover_height + 160

    card = Image.new('RGB', (card_width, card_height), background_color)
    draw = ImageDraw.Draw(card)

    img = Image.open(BytesIO(requests.get(album_image_url).content))
    img = img.resize((cover_width, cover_height), Image.Resampling.LANCZOS)
    img = img.convert("RGBA")

    mask = Image.new('L', img.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle([(0, 0), img.size], radius=80, fill=255)
    img.putalpha(mask)

    card.paste(img, (80, 80), img)

    title_font = ImageFont.truetype("/Users/als/PycharmProjects/GPT_USERBOT/extra/SFProText-Heavy.ttf", 200)  # Шрифт для названия трека
    info_font = ImageFont.truetype("/Users/als/PycharmProjects/GPT_USERBOT/extra/SFProText-Regular.ttf", 120)  # Шрифт для артиста и альбома

    text_x_position = cover_width + 200
    title_position = (text_x_position, 140)
    draw.text(title_position, track_name, fill="white", font=title_font)


    text_img = Image.new('RGBA', card.size, (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_img)


    artist_album_position = (text_x_position, 430)
    artist_album_text = f"{artist_name} • {album_name}"
    text_draw.text(artist_album_position, artist_album_text, fill=(255, 255, 255, 255), font=info_font)


    transparency = 150
    text_img = ImageEnhance.Brightness(text_img).enhance(transparency / 255)

    card = Image.alpha_composite(card.convert('RGBA'), text_img)

    card.save(output_path, format="PNG")
