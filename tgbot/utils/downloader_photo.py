import random
import requests


def download_photo_from_url(url: str):
    """
    Download photo from url
    :param url:  on image to download
    :return: str path to downloaded image
    """
    rand_int = random.randint(0, 1000000)
    r = requests.get(url, stream=True, verify=False)
    if r.status_code == 200:
        with open(f"tgbot/utils/images/{rand_int}.jpg", 'wb') as f:
            for chunk in r:
                f.write(chunk)
        return f"tgbot/utils/images/{rand_int}.jpg"
    else:
        return False
