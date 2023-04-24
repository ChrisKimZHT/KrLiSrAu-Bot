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
        respounce = requests.post(url=api, json=data, headers=headers)
        return respounce.json()

    def _append_assistant_message(self, message: str) -> None:
        self.messages.append({
            "role": "assistant",
            "content": message,
        })

    def _append_user_message(self, message: str) -> None:
        self.messages.append({
            "role": "user",
            "content": message,
        })

    async def chat(self, message: str) -> (str, int):
        self._append_user_message(message)
        try:
            resp = await self._request_api()
        except Exception as e:
            self.messages.pop()  # 若错误则还原
            return f"网络请求错误: {e}", 0

        try:
            content = resp["choices"][0]["message"]["content"]
            usage = resp["usage"]["total_tokens"]
        except Exception as e:
            self.messages.pop()  # 若错误则还原
            return f"解析响应错误: {e}", 0

        self._append_assistant_message(content)
        return content, usage
