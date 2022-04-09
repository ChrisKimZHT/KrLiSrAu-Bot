import datetime

from gacha_CEW import cew
from gacha_SW import sw
from gacha_WEW import wew
from pic_generate import gen_pic

last_run = datetime.datetime.now()
cool_down = 4  # 冷却时间


def func_gacha(typ):
    global last_run
    now = datetime.datetime.now()
    if (now - last_run).seconds >= cool_down:
        if typ == 1:
            string = f"[CQ:image,file=base64://{gen_pic(cew(0))}]"
        elif typ == 2:
            string = f"[CQ:image,file=base64://{gen_pic(cew(1))}]"
        elif typ == 3:
            string = f"[CQ:image,file=base64://{gen_pic(wew())}]"
        elif typ == 4:
            string = f"[CQ:image,file=base64://{gen_pic(sw())}]"
        else:
            string = "非法卡池"
        last_run = now
    else:
        string = f"冷却时间还有：{cool_down - (now - last_run).seconds}秒"
    return string
