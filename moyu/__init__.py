from nonebot import on_command, require, get_bot
from nonebot.plugin import PluginMetadata
from .moyu import mo_yu
from .config import Config, moyu_config

__plugin_meta__ = PluginMetadata(
    name="摸鱼办",
    description="查询节假日信息",
    usage="""指令: moyu / 摸鱼
用法: moyu - 查询节假日信息""",
    config=Config,
    extra={
        "authors": "ChrisKim",
        "version": "1.1.1",
        "KrLiSrAu-Bot": True,
    }
)

moyu = on_command("moyu", aliases={"摸鱼"}, priority=1, block=True)


@moyu.handle()
async def handle_moyu():
    result = mo_yu()
    await moyu.finish(result)


if moyu_config.klsa_moyu_schedule:
    require("nonebot_plugin_apscheduler")
    from nonebot_plugin_apscheduler import scheduler


    @scheduler.scheduled_job("cron", hour=moyu_config.klsa_moyu_schedule_hour,
                             minute=moyu_config.klsa_moyu_schedule_minute, id="moyu")
    async def _():
        bot = get_bot()
        result = mo_yu()
        for group in moyu_config.klsa_moyu_schedule_group:
            await bot.call_api("send_group_msg", group_id=group, message=result)
        for user in moyu_config.klsa_moyu_schedule_user:
            await bot.call_api("send_private_msg", user_id=user, message=result)
