import requests
from io import BytesIO
from PIL import Image

async def fetch_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))
