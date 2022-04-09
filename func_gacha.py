from gacha_CEW import cew
from gacha_SW import sw
from gacha_WEW import wew, ep
from pic_generate import gen_pic


def func_gacha(typ, cnt):
    string = ""
    if 1 <= typ <= 4 and (cnt == 1 or cnt == 10):
        if typ == 1:
            string = f"[CQ:image,file=base64://{gen_pic(cew(0))}]"
        elif typ == 2:
            string = f"[CQ:image,file=base64://{gen_pic(cew(1))}]"
        elif typ == 3:
            string = f"[CQ:image,file=base64://{gen_pic(wew())}]"
        elif typ == 4:
            string = f"[CQ:image,file=base64://{gen_pic(sw())}]"
    elif typ == 0 and (0 <= cnt <= 2):
        string = ep(cnt) + "\n"
    else:
        string = "非法参数"
    return string
