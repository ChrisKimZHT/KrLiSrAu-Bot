import datetime
import os
from gacha_CEW import cew
from gacha_SW import sw
from gacha_WEW import wew, ep, get_epinfo
from gacha_genpic import gen_pic

last_run = datetime.datetime.now()
cool_down = 4  # 冷却时间


def func_gacha(typ):
    global last_run
    now = datetime.datetime.now()
    if (now - last_run).seconds >= cool_down:
        if typ == 1:
            string = f"[CQ:image,file=file:///{os.getcwd()}/temp/{gen_pic(1, cew(0))}]"
        elif typ == 2:
            string = f"[CQ:image,file=file:///{os.getcwd()}/temp/{gen_pic(2, cew(1))}]"
        elif typ == 3:
            string = f"[CQ:image,file=file:///{os.getcwd()}/temp/{gen_pic(3, wew(), get_epinfo())}]"
        elif typ == 4:
            string = f"[CQ:image,file=file:///{os.getcwd()}/temp/{gen_pic(4, sw())}]"
        else:
            string = "非法卡池"
        last_run = now
    else:
        string = f"冷却时间还有：{cool_down - (now - last_run).seconds}秒"
    return string


def func_ep(typ):
    return ep(typ)
