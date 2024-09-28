from PIL import Image, ImageDraw, ImageFont
import logging

from userbot.utils.fetch_images_func import fetch_image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def create_song_card(track_info, output_path):
    try:
        track_name = track_info['track_name']
        artist_name = track_info['artist_name']
        album_image_url = track_info['album_image_url']
    except KeyError as e:
        logger.error(f"Отсутствует ключ в track_info: {e}")
        raise


    background_color = (18, 18, 18)
    cover_width = 640
    cover_height = 640
    padding = 20
    card_width = cover_width + 2 * padding
    card_height = cover_height + 2 * padding + 140

    card = Image.new('RGB', (card_width, card_height), background_color)
    draw = ImageDraw.Draw(card)

    try:
        img = await fetch_image(album_image_url)
    except Exception as e:
        logger.error(f"Не удалось загрузить обложку альбома: {e}")
        raise

    img = img.resize((cover_width, cover_height), Image.Resampling.LANCZOS)
    img = img.convert("RGBA")


    mask = Image.new('L', img.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.rounded_rectangle([(0, 0), img.size], radius=80, fill=255)
    img.putalpha(mask)

    card.paste(img, (padding, padding), img)

    try:
        title_font = ImageFont.truetype("/Users/als/PycharmProjects/GPT_USERBOT/extra/SFProText-Heavy.ttf", 44)
        info_font = ImageFont.truetype("/Users/als/PycharmProjects/GPT_USERBOT/extra/SFProText-Regular.ttf", 34)
    except IOError:
        title_font = ImageFont.load_default(size=44)
        info_font = ImageFont.load_default(size=34)
        logger.warning("Не удалось загрузить шрифты")

    title_position = (padding, 50 + padding + cover_height)
    draw.text(title_position, track_name, fill="white", font=title_font)

    artist_album_position = (padding, 2 * padding + cover_height + 80)
    artist_album_text = f"{artist_name}"
    gray_color = (128, 128, 128)
    draw.text(artist_album_position, artist_album_text, fill=gray_color, font=info_font)


    card.save(output_path, format="PNG")
