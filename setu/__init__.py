from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageEvent, Bot
from nonebot.adapters.onebot.v11.helpers import autorevoke_send, Cooldown, CooldownIsolateLevel
from nonebot.plugin import PluginMetadata
from .setu_class import Setu, setu_config
from .config import setu_config, Config

__plugin_meta__ = PluginMetadata(
    name="涩图",
    description="发送随机涩图",
    usage="""指令: setu / 涩图
用法: setu [标签...] [R18]
    [标签...] - 指定标签，多个标签用空格分隔
    [R18] - 指定是否为R18，默认为否""",
    config=Config,
    extra={
        "authors": "ChrisKim",
        "version": "2.0.2",
        "KrLiSrAu-Bot": True,
    }
)

setu = on_command("setu", aliases={"涩图"}, priority=1, block=True)


@setu.handle(parameterless=[
    Cooldown(
        cooldown=setu_config.klsa_setu_cooldown_time,
        prompt="冷却时间中",
        isolate_level=CooldownIsolateLevel.USER
    )
])
async def _(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    # 标签处理器
    tags = args.extract_plain_text().split(" ")
    if len(tags) == 0:
        my_setu = Setu([])
    elif tags[-1].lower() == "r18":
        my_setu = Setu(tags[:-1], True)
    else:
        my_setu = Setu(tags)

    # 获取数据
    if not await my_setu.get_data():
        await setu.finish("获取数据错误", at_sender=True)

    # 发送文字信息
    try:
        await setu.send(await my_setu.info_message(), at_sender=True)
    except Exception as e:
        await setu.finish(f"发送信息错误\n{e}", at_sender=True)

    # 发送图片信息
    try:
        if (my_setu.r18 and setu_config.klsa_setu_send_nsfw) or (not my_setu.r18 and setu_config.klsa_setu_send_sfw):
            message = await my_setu.pic_message(setu_config.klsa_setu_obfuscate)
            await autorevoke_send(bot, event, message=message, revoke_interval=setu_config.klsa_setu_withdraw_interval)
    except Exception as e:
        await setu.finish(f"发送图片错误\n{e}", at_sender=True)
