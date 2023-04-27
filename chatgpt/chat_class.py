import aiohttp
import time
from .config import chatgpt_config
from typing import Optional


class Chat:
    def __init__(self, user: int, setting: str = None, model: str = chatgpt_config.klsa_chat_model):
        self.user = user
        self.setting = setting
        self.respose_to_setting = None
        self.model = model
        self.messages = []
        self.create_time = time.time()
        self.lock = False

    def _create_actual_message(self) -> list:
        """
        获得实际的消息列表，包含预设与对预设的回复
        :return: 实际消息列表
        """
        result = []
        if self.setting is not None:
            result.append({
                "role": "user",
                "content": self.setting
            })
        if self.respose_to_setting is not None:
            result.append({
                "role": "assistant",
                "content": self.respose_to_setting
            })
        result += self.messages
        return result

    async def _request_api(self) -> dict:
        """
        异步请求OpenAI接口
        :return: OpenAI接口返回的JSON
        """
        api = chatgpt_config.klsa_chat_api_url
        data = {
            "model": self.model,
            "messages": self._create_actual_message(),
        }
        headers = {
            "Authorization": "Bearer " + chatgpt_config.klsa_chat_api_key
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url=api, json=data, headers=headers) as resp:
                return await resp.json()

    def _append_assistant_message(self, message: str) -> None:
        """
        添加机器人的回复
        :param message: 机器人的回复
        :return: 无
        """
        self.messages.append({
            "role": "assistant",
            "content": message,
        })

    def _append_user_message(self, message: str) -> None:
        """
        添加用户的消息
        :param message: 用户的消息
        :return: 无
        """
        self.messages.append({
            "role": "user",
            "content": message,
        })

    def get_lock(self) -> bool:
        """
        获得锁状态，若上锁则说明上次请求还未完成，此时无法进行新的请求
        :return: 锁状态
        """
        return self.lock

    def pop_back(self) -> bool:
        """
        删除最后一次对话
        :return: 无
        """
        if len(self.messages) < 2:
            return False
        self.messages.pop()
        self.messages.pop()
        return True

    def pop_front(self) -> bool:
        """
        删除最早一次对话
        :return: 无
        """
        if len(self.messages) < 2:
            return False
        self.messages.pop(0)
        self.messages.pop(0)
        return True

    def history_len(self) -> int:
        """
        获得历史对话数量（一问一答算1次）
        :return: 历史对话数量
        """
        return len(self.messages) // 2

    async def chat(self, message: Optional[str]) -> (str, int, bool):
        """
        进行一次对话
        :param message: 用户的消息，若为None则代表进行预设初始化
        :return: (回答内容, 消耗token数量, 是否删除了最早的一次对话)
        """
        content = ""  # 回答内容
        usage = 0  # 消耗token数量
        poped = False  # 是否删除了最早的一次对话

        if self.lock:
            content = "上次请求还未完成，请稍后再试"
            return content, usage, poped

        try:
            self.lock = True

            if message is None:
                if self.setting is None:
                    content = "若要初始化预设，请先设定预设"
                    raise
            else:
                self._append_user_message(message)

            try:
                resp = await self._request_api()
            except Exception as e:
                content = f"网络请求错误: {e}"
                self.messages.pop()  # 若错误则还原
                raise

            try:
                content = resp["choices"][0]["message"]["content"]
                usage = resp["usage"]["total_tokens"]
            except Exception as e:
                content = f"解析响应错误: {e}"
                self.messages.pop()  # 若错误则还原
                raise

            # 如果达到token限制，则删除最早的一次对话
            if usage >= chatgpt_config.klsa_chat_token_limit and self.history_len():
                self.pop_front()
                poped = True

            # 如果为预设初始化，则设置预设回复
            if message is None:
                self.respose_to_setting = content
            else:
                self._append_assistant_message(content)
        finally:
            self.lock = False
            return content, usage, poped
