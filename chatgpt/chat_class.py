import aiohttp
import time
from .config import chatgpt_config
from typing import Optional


class ChatResult:
    """
    对话结果
    """

    def __init__(self):
        self.is_error = False
        self.create_time = int(time.time())
        self.finish_time = 0
        self.content = ""
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.poped = False
        self.original_resp = None

    def set_content(self, resp: dict) -> None:
        """
        写入内容
        :param resp: OpenAI API响应
        :return:
        """
        self.finish_time = int(time.time())
        self.original_resp = resp
        self.content = resp["choices"][0]["message"]["content"]
        self.prompt_tokens = resp["usage"]["prompt_tokens"]
        self.completion_tokens = resp["usage"]["completion_tokens"]
        if resp["usage"]["total_tokens"] >= chatgpt_config.klsa_chat_token_limit:
            self.poped = True

    def set_error(self, errstr: str) -> None:
        """
        设置为错误
        :param errstr: 错误信息
        :return:
        """
        self.is_error = True
        self.content = errstr

    def is_poped(self) -> bool:
        """
        获得是否因为超过额度而被删除
        :return: 是否因为超过额度而被删除
        """
        return self.poped

    def get_error(self) -> bool:
        """
        获得是否为错误
        :return: 是否为错误
        """
        return self.is_error

    def get_original_resp(self) -> dict:
        """
        获得原始的OpenAI API响应
        :return: OpenAI API响应
        """
        return self.original_resp

    def get_content_str(self) -> str:
        """
        获得回应内容
        :return: 回答内容
        """
        return self.content

    def get_info_str(self) -> str:
        """
        获得请求详情
        :return: 请求详情字符串
        """
        info_str = "计算耗时: %.2f sec\n单位数量: %d token(s)" % (
            self.finish_time - self.create_time, self.prompt_tokens + self.completion_tokens)
        if chatgpt_config.klsa_chat_prompt_token_cost != -1 and chatgpt_config.klsa_chat_completion_token_cost != -1:
            info_str += "\n消费金额: $%.6f" % (chatgpt_config.klsa_chat_prompt_token_cost * self.prompt_tokens / 1000 +
                                               chatgpt_config.klsa_chat_completion_token_cost * self.completion_tokens / 1000)
        if self.poped:
            info_str += "\n[!] 最早的一次对话被删除"
        return info_str


class ChatInst:
    """
    对话实例
    """

    def __init__(self, user: int, model: str = chatgpt_config.klsa_chat_model):
        self.user = user
        self.model = model
        self.messages = []
        self.create_time = time.time()
        self.last_use_time = time.time()
        self.lock = False
        self.preset = []

    async def _request_api(self) -> dict:
        """
        异步请求OpenAI接口
        :return: OpenAI接口返回的JSON
        """
        api = chatgpt_config.klsa_chat_api_url
        data = {
            "model": self.model,
            "messages": self.preset + self.messages,
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

    def _refresh_last_use_time(self) -> None:
        """
        刷新最后使用时间
        :return: 无
        """
        self.last_use_time = time.time()

    def get_message_list(self) -> list:
        """
        获得消息列表
        :return: 消息列表
        """
        return self.messages

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

    def get_creat_time(self) -> int:
        """
        获得创建时间
        :return: 创建时间戳
        """
        return int(self.create_time)

    def get_last_use_time(self) -> int:
        """
        获得最后使用时间
        :return: 最后使用时间戳
        """
        return int(self.last_use_time)

    async def init_preset(self, preset: str) -> ChatResult:
        """
        初始化预设
        :param preset: 预设内容
        :return: 初始化结果
        """
        chat_result = ChatResult()

        if self.lock:
            chat_result.set_error("上次请求还未完成，请稍后再试")
            return chat_result

        self.preset.append({
            "role": "user",
            "content": preset,
        })

        try:
            self.lock = True
            self._refresh_last_use_time()

            try:
                resp = await self._request_api()
            except Exception as e:
                chat_result.set_error(f"网络请求错误: {e}")
                self.preset.pop()  # 若错误则还原
                raise

            try:
                chat_result.set_content(resp)
            except Exception as e:
                chat_result.set_error(f"解析响应错误: {e}")
                self.preset.pop()  # 若错误则还原
                raise

            self.preset.append({
                "role": "assistant",
                "content": chat_result.get_content_str(),
            })

        finally:
            self.lock = False
            return chat_result

    async def chat(self, message: str) -> ChatResult:
        """
        进行一次对话
        :param message: 用户的消息，若为None则代表进行预设初始化
        :return: ChatResult对象
        """
        chat_result = ChatResult()

        if self.lock:
            chat_result.set_error("上次请求还未完成，请稍后再试")
            return chat_result

        try:
            self.lock = True
            self._refresh_last_use_time()
            self._append_user_message(message)

            try:
                resp = await self._request_api()
            except Exception as e:
                chat_result.set_error(f"网络请求错误: {e}")
                self.messages.pop()  # 若错误则还原
                raise

            try:
                chat_result.set_content(resp)
            except Exception as e:
                chat_result.set_error(f"解析响应错误: {e}")
                self.messages.pop()  # 若错误则还原
                raise

            # 如果达到token限制，则删除最早的一次对话
            if chat_result.is_poped():
                self.pop_front()

            self._append_assistant_message(chat_result.get_content_str())

        finally:
            self.lock = False
            return chat_result


class ChatUser:
    """
    对话用户
    """

    def __init__(self, user: int):
        self.user = user
        self.instance = ChatInst(user)
        self.preset = []

    def get_instance(self) -> ChatInst:
        """
        获得对话实例
        :return: 对话实例
        """
        return self.instance

    async def reset_instance(self, preset_idx: int = -1) -> Optional[ChatResult]:
        """
        重置对话实例
        :param preset_idx: 预设索引
        :return: ChatResult对象
        """
        self.instance = ChatInst(self.user)
        if 0 <= preset_idx < len(self.preset):
            return await self.instance.init_preset(self.preset[preset_idx])
        return

    def add_presets(self, preset: str) -> None:
        """
        添加预设
        :param preset: 预设文字
        :return:
        """
        self.preset.append(preset)

    def del_presets(self, idx: int) -> None:
        """
        删除预设
        :param idx: 预设索引
        :return:
        """
        if 0 <= idx < len(self.preset):
            self.preset.pop(idx)

    def get_presets(self) -> list:
        """
        获得预设
        :return: 预设列表
        """
        return self.preset
