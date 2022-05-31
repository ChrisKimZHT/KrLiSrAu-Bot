import os
from .gacha_module_cew import cew
from .gacha_module_sw import sw
from .gacha_module_wew import wew, set_ep, get_epinfo
from .gacha_module_genpic import gen_pic
from nonebot import on_command, CommandSession


@on_command("gacha", aliases=("gc", "抽卡"))
async def gacha(session: CommandSession):
    typ = session.current_arg_text.strip()
    try:
        typ = int(typ)
    except ValueError:
        return
    if typ == 1:
        string = f"[CQ:image,file=file:///{os.getcwd()}/temp/{await gen_pic(1, cew(0))}]"
    elif typ == 2:
        string = f"[CQ:image,file=file:///{os.getcwd()}/temp/{await gen_pic(2, cew(1))}]"
    elif typ == 3:
        string = f"[CQ:image,file=file:///{os.getcwd()}/temp/{await gen_pic(3, wew(), get_epinfo())}]"
    elif typ == 4:
        string = f"[CQ:image,file=file:///{os.getcwd()}/temp/{await gen_pic(4, sw())}]"
    else:
        string = "非法卡池"
    await session.send(string)


@on_command("ep", aliases="定轨")
async def ep(session: CommandSession):
    typ = session.current_arg_text.strip()
    try:
        typ = int(typ)
    except ValueError:
        return
    await session.send(set_ep(typ))
