from nonebot.adapters.onebot.v11 import MessageSegment
import aiohttp
from PIL import Image
from io import BytesIO
import random
from .config import setu_config


def random_color() -> tuple:
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


class Setu:
    def __init__(self, tags: list, r18: bool = False):
        self.status = False
        self.pid = 0
        self.page = 0
        self.uid = 0
        self.title = ""
        self.author = ""
        self.r18 = r18
        self.width = 0
        self.height = 0
        self.tags = tags
        self.ext = ""
        self.time = 0
        self.url = ""

    async def _request_api(self):
        api = "https://api.lolicon.app/setu/v2"
        data = {
            "r18": self.r18,
            "tag": self.tags,
            "size": [setu_config.klsa_setu_default_size],
            "proxy": setu_config.klsa_setu_proxy_url,
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=api, json=data) as resp:
                resp_dict = await resp.json()
                if len(resp_dict["_data"]):  # API返回长度>0
                    return resp_dict["_data"][0]
                return None

    async def get_data(self) -> bool:
        setu_data = await self._request_api()
        if setu_data is None:  # 若获取失败
            return False
        self.pid = setu_data["pid"]
        self.page = setu_data["p"]
        self.uid = setu_data["uid"]
        self.title = setu_data["title"]
        self.author = setu_data["author"]
        self.r18 = setu_data["r18"]
        self.width = setu_data["width"]
        self.height = setu_data["height"]
        self.tags = setu_data["tags"]
        self.ext = setu_data["ext"]
        self.time = setu_data["uploadDate"]
        self.url = setu_data["urls"][setu_config.klsa_setu_default_size]
        self.status = True
        return True

    async def info_message(self) -> MessageSegment:
        text = f"""{self.title} - {self.author}
UID: {self.uid}
PID: {self.pid} (p{self.page})
URL: {setu_config.klsa_setu_prefix_url}{self.url}"""
        return MessageSegment.text(text)

    async def pic_message(self, obfuscate: bool = False) -> MessageSegment:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.url) as resp:
                byte_image = await resp.read()
                if obfuscate:  # 修改四个角的像素，随机颜色
                    image = Image.open(BytesIO(byte_image))
                    image.putpixel((0, 0), random_color())
                    image.putpixel((0, image.height - 1), random_color())
                    image.putpixel((image.width - 1, 0), random_color())
                    image.putpixel((image.width - 1, image.height - 1), random_color())
                    obfuscated_byte_image = BytesIO()
                    image.save(obfuscated_byte_image, format="PNG")
                    return MessageSegment.image(obfuscated_byte_image)
                return MessageSegment.image(byte_image)
