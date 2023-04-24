from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.params import CommandArg
from .config import config
from .chat_class import Chat
import time

chatgpt = on_command("chatgpt", aliases={"gpt", "chat"}, priority=1, block=True)

chat_data = {}


@chatgpt.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    args_text = args.extract_plain_text()
    user_id = event.user_id

    if args_text == "":
        await chatgpt.reject("内容不可为空")
    elif args_text == "reset" or args_text == "r":
        chat_data[user_id] = Chat(user_id)
        await chatgpt.finish("重置对话完成")
    elif args_text.startswith("single ") or args_text.startswith("s "):
        message = args_text.split(" ", 1)[1]
        if message == "":
            await chatgpt.reject("内容不可为空")
        chat_inst = Chat(user_id)
        await chat(chat_inst, message)
    else:
        if user_id not in chat_data:
            chat_data[user_id] = Chat(user_id)
        chat_inst = chat_data[user_id]
        await chat(chat_inst, args_text)


def get_info_str(duration: float, usage: int, poped: bool) -> str:
    info_str = "计算耗时: %.2f sec\n单位数量: %d token(s)" % (duration, usage)
    if config.klsa_chat_kt_cost != -1:
        info_str += "\n消费金额: $%.6f" % (config.klsa_chat_kt_cost * usage / 1000)
    if poped:
        info_str += "\n[!] 最早的一次对话被删除"
    return info_str


async def chat(chat_inst: Chat, message: str):
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
