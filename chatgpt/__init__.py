from nonebot import on_command
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from nonebot.params import CommandArg
from nonebot.rule import to_me
from .chat_class import Chat

chatgpt = on_command("chatgpt", rule=to_me(), aliases={"gpt", "chat"}, priority=1, block=True)

chat_data = {}


@chatgpt.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    if args.extract_plain_text == "":
        await chatgpt.finish("内容不可为空", at_sender=True)
        return

    # 创建新对话
    if args.extract_plain_text() == "create":
        chat_data[event.user_id] = Chat(event.user_id)
        await chatgpt.finish("已创建新对话", at_sender=True)
        return

    # 检查是否有历史对话
    if event.user_id not in chat_data:
        await chatgpt.finish("无历史对话可用，请先创建对话: /chat create", at_sender=True)
        return

    # 开始对话
    chat_inst = chat_data[event.user_id]
    await chatgpt.send("请求已发送，等待响应...")
    result = await chat_inst.chat(args.extract_plain_text())
    await chatgpt.finish(result, at_sender=True)
