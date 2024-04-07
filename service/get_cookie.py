import asyncio
import json
import os
from io import BytesIO

from DrissionPage import WebPage, ChromiumOptions
from PIL import Image

from config import red_book_url, is_headless


async def get_red_book_cookie():
    if is_headless:
        page = WebPage(chromium_options=ChromiumOptions().headless())
    else:
        page = WebPage()
    page.get(red_book_url)
    try:
        qr_code = page.ele("@class=qrcode-img").src()
        # 保存临时文件到本地，弹出二维码
        image = Image.open(BytesIO(qr_code))
        image.show()
        print("请扫描二维码")

        while True:
            if page.url != red_book_url:
                image.close()
                break
            else:
                await asyncio.sleep(1)

        cookie = page.cookies(as_dict=True)
    except Exception as e:
        cookie = page.cookies(as_dict=True)

    now_path = os.path.abspath(os.path.dirname(__file__))
    save_path = os.path.join(now_path, "../data/cookie.json")
    with open(save_path, "w") as f:
        cookie_json = json.dumps(cookie)
        # 增加一个domian字段
        cookie_json = cookie_json.__add__(f', "domain": "{red_book_url}"')
        f.write(cookie_json)
