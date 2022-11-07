from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment
import requests
from .config import config


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
            "size": [config.klsa_setu_default_size],
            "proxy": config.klsa_setu_proxy_url,
        }
        respounce = requests.post(url=api, json=data)
        resp_dict = respounce.json()
        if len(resp_dict["data"]):  # API返回长度>0
            return resp_dict["data"][0]
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
        self.url = setu_data["urls"][config.klsa_setu_default_size]
        self.status = True
        return True

    async def info_message(self) -> MessageSegment:
        text = f"""{self.title}
{self.author}
UID: {self.uid}
PID: {self.pid} ({self.page})
URL: {config.klsa_setu_prefix_url}{self.url}"""
        return MessageSegment.text(text)

    async def pic_message(self) -> MessageSegment:
        respounce = requests.get(url=self.url)
        byte_pic = respounce.content.strip()
        return MessageSegment.image(byte_pic)
