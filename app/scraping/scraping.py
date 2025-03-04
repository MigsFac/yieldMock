import requests
import os
from googleapiclient.discovery import build
import hashlib
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
CSE_ID = os.getenv("CSE_ID")


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
                img_hash = hashlib.md5(img_url.encode()).hexdigest()
                if img_hash not in collected_images:
                    collected_images.add(img_hash)
                    image_urls.append(img_url)
        if len(image_urls) >= total_images:
            break

    return image_urls[:total_images]


collected_images = set()
search_query = ["富士山", "富士山 写真", "富士山 遠景", "富士山 雪", "富士山 山梨"]
img_urls = []
for query in search_query:
    img_urls.extend(google_image_search(query))

if not os.path.exists("fujisan_images"):
    os.makedirs("fujisan_images")

for i, img_url in enumerate(img_urls):
    try:
        img_data = requests.get(img_url).content
        with open(f"fujisan_images/fujisan_{i}.jpg", "wb") as f:
            f.write(img_data)
        print(f"fujisan_{i}.jpg saved")
    except Exception as e:
        print(f"Failed to download {img_url}: {e}")
