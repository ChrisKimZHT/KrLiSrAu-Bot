import requests
import time
from .config import config


class Chat:
    def __init__(self, user: int, model: str = config.klsa_chat_model):
        self.user = user
        self.model = model
        self.messages = []
        self.create_time = time.time()

    async def _request_api(self) -> dict:
        api = config.klsa_chat_api_url
        data = {
            "model": self.model,
            "messages": self.messages,
        }
        headers = {
            "Authorization": "Bearer " + config.klsa_chat_api_key
        }
        try:
            respounce = requests.post(url=api, json=data, headers=headers)
        except Exception as e:
            return {
                "role": "error",
                "content": f"网络请求错误\n{e}"
            }
        try:
            resp_json = respounce.json()
            self._append_message(resp_json["choices"][0])
            return resp_json["choices"][0]["message"]
        except Exception as e:
            return {
                "role": "error",
                "content": f"解析响应错误\n{e}"
            }

    def _append_message(self, message: dict) -> None:
        self.messages.append(message)

    def _append_user_message(self, message: str) -> None:
        self.messages.append({
            "role": "user",
            "content": message,
        })

    async def chat(self, message: str) -> str:
        self._append_user_message(message)
        result = await self._request_api()
        if result["role"] == "error":
            self.messages.pop()  # 若错误则还原
        return result["content"]
