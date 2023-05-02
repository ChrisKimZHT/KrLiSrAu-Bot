from nonebot import on_command
from nonebot.plugin import PluginMetadata
from .moyu import mo_yu
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="摸鱼办",
    description="查询节假日信息",
    usage="""指令: moyu / 摸鱼
用法: moyu - 查询节假日信息""",
    config=Config,
    extra={
        "authors": "ChrisKim",
        "version": "1.0.4",
        "KrLiSrAu-Bot": True,
    }
)

moyu = on_command("moyu", aliases={"摸鱼"}, priority=1, block=True)


@moyu.handle()
async def handle_moyu():
    result = mo_yu()
    await moyu.finish(result)
