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
    if args.extract_plain_text() == "":
        await chatgpt.finish("内容不可为空")

    # 创建新对话
    if args.extract_plain_text() == "create":
        chat_data[event.user_id] = Chat(event.user_id)
        await chatgpt.finish("已创建新对话")

    # 检查是否有历史对话
    if event.user_id not in chat_data:
        await chatgpt.finish("无历史对话可用，请先创建对话: chat create")

    # 开始对话
    chat_inst = chat_data[event.user_id]
    start_time = time.time()
    await chatgpt.send("请求已发送，等待接口响应")
    content, usage, poped = await chat_inst.chat(args.extract_plain_text())
    end_time = time.time()

    # 计算消费
    info_str = "\n\n计算耗时: %.2f sec\n单位数量: %d token(s)" % (end_time - start_time, usage)
    if config.klsa_chat_kt_cost != -1:
        info_str += "\n消费金额: $%.6f" % (config.klsa_chat_kt_cost * usage / 1000)
    if poped:
        info_str += "\n[!] 最早的一次对话被删除"

    # 发送结果
    result = MessageSegment.text(content) + MessageSegment.text(info_str)
    await chatgpt.finish(result, at_sender=True)
