from nonebot import on_command, require
from nonebot.plugin import PluginMetadata
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import MessageEvent, MessageSegment, Message
from .config import Config, whuteb_config
from .query_data import query_data
from .statistic import update_statistic, stat_figure, stat_text

require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler

__plugin_meta__ = PluginMetadata(
    name="武理电费",
    description="武汉理工大学电费监控",
    usage="""指令: eb
用法: eb [选项]
    空 - 等同于 eb now
    now - 查询当前电费
    stat - 查询电费统计""",
    config=Config,
    extra={
        "authors": "ChrisKim",
        "version": "1.0.1",
        "KrLiSrAu-Bot": True,
    }
)

eb = on_command("eb", priority=1, block=True)
eb_now = on_command(("eb", "now"), priority=1, block=True)
eb_stat = on_command(("eb", "stat"), priority=1, block=True)


@eb.handle()
async def _(matcher: Matcher, event: MessageEvent):
    if not check_config():
        await matcher.finish("未正确填写插件配置")
        return
    await query(matcher)


@eb_now.handle()
async def _(matcher: Matcher, event: MessageEvent):
    if not check_config():
        await matcher.finish("未正确填写插件配置")
        return
    await query(matcher)


async def query(matcher: Matcher):
    result = await query_data()
    if result["status"]:
        text = f"【电费查询】\n" \
               f"剩余电量: {result['remain']} kW·h\n" \
               f"累计电量: {result['total']} kW·h\n"
        if whuteb_config.klsa_whuteb_area != "mafangshan":
            text += f"\n查表时间: {result['time']}"
        if result['remain'] < 15.00:
            text += "\n[!] 电量不足，注意及时充值 [!]"
    else:
        text = "【电费查询】\n发生错误"
    await matcher.send(text)


@eb_stat.handle()
async def _(matcher: Matcher, event: MessageEvent, args: Message = CommandArg()):
    if not check_config():
        await matcher.finish("未正确填写插件配置")
        return
    arg_text = args.extract_plain_text()
    if arg_text == "text":
        txt = stat_text()
        await matcher.finish(txt)
    else:
        fig = stat_figure()
        await matcher.finish(MessageSegment.image(fig))


@scheduler.scheduled_job("cron", id="update_stat", hour="12", minute="0", second="0")
async def _():
    if not check_config():
        return
    await update_statistic()


def check_config() -> bool:
    return bool(len(whuteb_config.klsa_whuteb_account)) and bool(len(whuteb_config.klsa_whuteb_password))
