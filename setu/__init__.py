from nonebot import on_command
from nonebot.params import CommandArg, Command
from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment, Bot
from .setu_class import Setu
from .withdraw import add_withdraw_job
from .cooldown import check_cd, update_cd

setu = on_command("setu", aliases={"涩图"}, priority=1)


@setu.handle()
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    if not await check_cd(event.user_id):
        await setu.finish("冷却时间中", at_sender=True)
    tags = args.extract_plain_text().split(" ")
    if len(tags) == 0:
        my_setu = Setu([])
    elif tags[-1].lower() == "r18":
        my_setu = Setu(tags[:-1], True)
    else:
        my_setu = Setu(tags)
    if not await my_setu.get_data():
        await setu.finish("获取数据错误", at_sender=True)
    await setu.send(await my_setu.info_message(), at_sender=True)
    pic_msginfo = await setu.send(await my_setu.pic_message())
    await add_withdraw_job(bot, **pic_msginfo)
    await update_cd(event.user_id)
