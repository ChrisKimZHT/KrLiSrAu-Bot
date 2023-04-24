import aiohttp
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
        async with aiohttp.ClientSession() as session:
            async with session.post(url=api, json=data, headers=headers) as resp:
                return await resp.json()

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

    async def chat(self, message: str) -> (str, int, bool):
        content = ""  # 回答内容
        usage = 0  # 消耗token数量
        poped = False  # 是否删除了最早的一次对话

        self._append_user_message(message)

        try:
            resp = await self._request_api()
        except Exception as e:
            content += f"网络请求错误: {e}"
            self.messages.pop()  # 若错误则还原
            return content, usage, poped

        try:
            content += resp["choices"][0]["message"]["content"]
            usage = resp["usage"]["total_tokens"]
        except Exception as e:
            content += f"解析响应错误: {e}"
            self.messages.pop()  # 若错误则还原
            return content, usage, poped

        # 如果达到token限制，则删除最早的一次对话
        if usage >= config.klsa_chat_token_limit and len(self.messages) >= 2:
            self.messages.pop(0)
            self.messages.pop(0)
            poped = True

        self._append_assistant_message(content)

        return content, usage, poped
