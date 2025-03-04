import requests
import os
from googleapiclient.discovery import build
import hashlib
from dotenv import load_dotenv
from io import BytesIO
import time
from PIL import Image
from datetime import datetime, timezone, timedelta

load_dotenv()
API_KEY = os.getenv("API_KEY")
CSE_ID = os.getenv("CSE_ID")


def get_image_hash(image_url):
    try:
        response = requests.get(image_url, timeout=5)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        image = image.convert("RGB")
        img_hash = hashlib.md5(image.tobytes()).hexdigest()
        return img_hash
    except Exception as e:
        print(f"Error processing {image_url}: {e}")
        return None


def google_image_search(query, total_images=100, per_page=10):
    service = build("customsearch", "v1", developerKey=API_KEY)

    image_urls = []

    for start in range(1, min(total_images, 91), per_page):

        res = (
            service.cse()
            .list(q=query, cx=CSE_ID, searchType="image", num=per_page, start=start)
            .execute()
        )

        if "items" in res:
            for item in res["items"]:
                img_url = item["link"]
                img_hash = get_image_hash(img_url)

                if img_hash not in collected_images:
                    collected_images.add(img_hash)
                    image_urls.append(img_url)
        if len(image_urls) >= total_images:
            break

    return image_urls[:total_images]


collected_images = set()
search_query = ["風景写真"]
save_DIR = "dataset/mountain"
save_fileName = "mountain"
img_urls = []
for query in search_query:
    img_urls.extend(google_image_search(query))

if not os.path.exists(save_DIR):
    os.makedirs(save_DIR)

for i, img_url in enumerate(img_urls):
    try:
        img_data = requests.get(img_url).content
        now = datetime.now()
        timestamp = now.strftime("%y%m%d%H%M%S") + f"{now.microsecond // 1000:03d}"
        with open(f"{save_DIR}/{save_fileName}_{timestamp}.jpg", "wb") as f:
            f.write(img_data)
        print(f"{save_fileName}_{timestamp}.jpg saved")
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")
