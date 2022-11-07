from nonebot import on_command
from nonebot.params import CommandArg, Command
from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment, Bot
from .setu_class import Setu
from .withdraw import add_withdraw_job

setu = on_command("setu", aliases={"涩图"}, priority=1)


@setu.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    tags = args.extract_plain_text().split(" ")
    if len(tags) == 0:
        my_setu = Setu([])
    elif tags[-1].lower() == "r18":
        my_setu = Setu(tags[:-1], True)
    else:
        my_setu = Setu(tags)
    if not await my_setu.get_data():
        await setu.finish("获取数据错误")
    await setu.send(await my_setu.info_message(), at_sender=True)
    msg_info = await setu.send(await my_setu.pic_message())
    await add_withdraw_job(bot, **msg_info)
