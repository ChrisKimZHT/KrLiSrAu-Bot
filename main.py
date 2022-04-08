from gacha_CEW import cew
from gacha_SW import sw
from gacha_WEW import wew, ep


def func_gacha(typ, cnt):
    string = ""
    if 1 <= typ <= 4 and (cnt == 1 or cnt == 10):
        if typ == 1:
            string += "角色活动祈愿\n"
            for i in range(0, cnt):
                string += cew(0) + "\n"
        elif typ == 2:
            string += "角色活动祈愿-2\n"
            for i in range(0, cnt):
                string += cew(1) + "\n"
        elif typ == 3:
            string += "武器活动祈愿\n"
            for i in range(0, cnt):
                string += wew() + "\n"
        elif typ == 4:
            string += "常驻祈愿\n"
            for i in range(0, cnt):
                string += sw() + "\n"
    elif typ == 0 and (0 <= cnt <= 2):
        string += ep(cnt) + "\n"
    else:
        string += "非法参数"
    return string


print(func_gacha(1, 10))
