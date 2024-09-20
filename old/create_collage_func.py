from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO


def create_collage(images, titles_and_artists, output_path):
    if not images or not titles_and_artists:
        raise ValueError("Нет изображений или названий.")

    background_color = (18, 18, 18)
    cover_width = 120
    cover_height = 120
    spacing = 20
    collage_width = cover_width + 2 * spacing + 400
    collage_height = len(images) * (cover_height + spacing) + spacing

    collage = Image.new('RGB', (collage_width, collage_height), background_color)
    draw = ImageDraw.Draw(collage)

    cover_positions = [(spacing, spacing + i * (cover_height + spacing)) for i in range(len(images))]
    text_x_position = cover_width + 2 * spacing

    try:
        font = ImageFont.truetype("/System/Library/Fonts/SF-Pro-Display-Regular.otf", 24)
    except IOError:
        font = ImageFont.load_default()

    for i, (img_url, (title, artist)) in enumerate(zip(images, titles_and_artists)):

        img = Image.open(BytesIO(requests.get(img_url).content))
        img = img.resize((cover_width, cover_height), Image.Resampling.LANCZOS)
        img = img.convert("RGBA")

        mask = Image.new('L', img.size, 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.rounded_rectangle([(0, 0), img.size], radius=20, fill=255)
        img.putalpha(mask)

        collage.paste(img, cover_positions[i], img)

        text_position = (text_x_position, cover_positions[i][1])
        text = f"{title}\n{artist}"
        draw.text(text_position, text, fill="white", font=font)

    collage.save(output_path)
    pass
