from nonebot import on_command
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import Message, MessageEvent, MessageSegment
import requests
from cairosvg import svg2png

ghcontribute = on_command("ghcontribute", aliases={"ghc"}, priority=1)


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
        resp = requests.get(api)
        png = svg2png(bytestring=resp.text.strip(), output_height=512, background_color="#FFFFFF")
        return png
    except Exception:
        return f"ERROR"
