from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.params import CommandArg
from .config import config
from .chat_class import Chat
from typing import Optional
import time

chatgpt = on_command("chatgpt", aliases={"gpt", "chat", "对话"}, priority=1, block=True)

chat_data = {}
chat_setting = {}
help_msg = """ChatGPT - 基于OpenAI接口的聊天机器人
指令: chatgpt / gpt / chat / 对话
用法: <内容> / single <内容> / setting <内容> / reset / help
详情:
    chatgpt <内容> - 进行连续对话
    chatgpt single <内容> - 进行一次性对话
    chatgpt setting - 清除对话预设
    chatgpt setting <内容> - 设置对话预设
    chatgpt reset - 重置对话
"""


@chatgpt.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    args_text = args.extract_plain_text()
    user_id = event.user_id

    if args_text == "" or args_text == "help":
        await chatgpt.finish(help_msg)
    elif args_text == "reset":
        chat_data[user_id] = Chat(user_id, chat_setting.get(user_id))
        await chatgpt.finish("重置对话完成")
    elif args_text.startswith("setting"):
        message = args_text.split(" ", 1)[1]
        if message == "":
            chat_setting["user_id"] = None
            chat_data[user_id] = Chat(user_id, chat_setting.get(user_id))
            await chatgpt.finish("清除设定完成")
        else:
            chat_setting[user_id] = message
            chat_data[user_id] = Chat(user_id, chat_setting.get(user_id))
            chat_inst = chat_data[user_id]
            await chat(chat_inst, None)
    elif args_text.startswith("single"):
        message = args_text.split(" ", 1)[1]
        if message == "":
            await chatgpt.reject("内容不可为空")
        chat_inst = Chat(user_id)
        await chat(chat_inst, message)
    else:
        if user_id not in chat_data:
            chat_data[user_id] = Chat(user_id, chat_setting.get(user_id))
        chat_inst = chat_data[user_id]
        await chat(chat_inst, args_text)


def get_info_str(duration: float, usage: int, poped: bool) -> str:
    info_str = "计算耗时: %.2f sec\n单位数量: %d token(s)" % (duration, usage)
    if config.klsa_chat_kt_cost != -1:
        info_str += "\n消费金额: $%.6f" % (config.klsa_chat_kt_cost * usage / 1000)
    if poped:
        info_str += "\n[!] 最早的一次对话被删除"
    return info_str


async def chat(chat_inst: Chat, message: Optional[str]):
    if chat_inst.get_lock():
        await chatgpt.reject("上次请求还未完成，请稍后再试或强制创建新会话: chat create")
    await chatgpt.send("请求已发送，等待接口响应...")
    start_time = time.time()
    content, usage, poped = await chat_inst.chat(message)
    end_time = time.time()
    duration = end_time - start_time
    info_str = get_info_str(duration, usage, poped)
    result = MessageSegment.text(content) + MessageSegment.text("\n\n") + MessageSegment.text(info_str)
    await chatgpt.finish(result, at_sender=True)
