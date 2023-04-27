from nonebot import on_command
from nonebot.plugin import PluginMetadata
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment
import aiohttp
from cairosvg import svg2png

__plugin_meta__ = PluginMetadata(
    name="GitHub贡献查询",
    description="查询指定用户GitHub贡献图",
    usage="""指令: ghcontribute / ghc
用法: ghcontribute <用户名> - 查询指定用户的GitHub贡献图""",
    extra={
        "authors": "ChrisKim",
        "version": "1.0.2",
        "KrLiSrAu-Bot": True,
    }
)

ghcontribute = on_command("ghcontribute", aliases={"ghc"}, priority=1, block=True)


@ghcontribute.handle()
async def _(event: MessageEvent, args: Message = CommandArg()):
    msg = await req_api(args.extract_plain_text())
    if msg == "ERROR":
        await ghcontribute.finish(MessageSegment.text(msg))
    else:
        await ghcontribute.finish(MessageSegment.image(msg))


async def req_api(user: str) -> str:
    api = f"https://ghchart.rshah.org/{user}"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url=api) as resp:
                byte_img = await resp.read()
                png = svg2png(bytestring=byte_img, output_height=512, background_color="#FFFFFF")
                return png
    except Exception:
        return f"ERROR"
