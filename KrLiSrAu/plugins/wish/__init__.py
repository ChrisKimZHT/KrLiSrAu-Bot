import os
from .character_event_wish import cew
from .standard_wish import sw
from .weapon_event_wish import wew, set_ep, get_epinfo
from .picture_generator import gen_pic
from nonebot import on_command, CommandSession


@on_command("wish", aliases=("gacha", "gc", "祈愿", "抽卡"))
async def wish(session: CommandSession):
    typ = session.current_arg_text.strip()
    try:
        typ = int(typ)
    except ValueError:
        return
    if typ == 1:
        result = await gen_pic(1, await cew(False))
    elif typ == 2:
        result = await gen_pic(2, await cew(True))
    elif typ == 3:
        result = await gen_pic(3, await wew(), await get_epinfo())
    elif typ == 4:
        result = await gen_pic(4, await sw())
    else:
        return
    await session.send(f"[CQ:image,file=base64://{result}]")


@on_command("ep", aliases="定轨")
async def ep(session: CommandSession):
    typ = session.current_arg_text.strip()
    try:
        typ = int(typ)
    except ValueError:
        return
    result = await set_ep(typ)
    await session.send(result)
