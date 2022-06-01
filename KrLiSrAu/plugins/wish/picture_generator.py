import datetime
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

# 图片素材加载
# 物品字典
item_dict = {
    # 限定五星角色
    "魈": [Image.open("resource/wish/character/魈.png").convert(mode="RGBA").resize((120, 384)), 5, True, "风"],
    "夜兰": [Image.open("resource/wish/character/夜兰.png").convert(mode="RGBA").resize((120, 384)), 5, True, "水"],
    "神里绫华": [Image.open("resource/wish/character/神里绫华.png").convert(mode="RGBA").resize((120, 384)), 5, True, "冰"],
    "神里绫人": [Image.open("resource/wish/character/神里绫人.png").convert(mode="RGBA").resize((120, 384)), 5, True, "水"],
    "温迪": [Image.open("resource/wish/character/温迪.png").convert(mode="RGBA").resize((120, 384)), 5, True, "风"],
    # 限定五星武器
    "若水": [Image.open("resource/wish/weapon/若水.png").convert(mode="RGBA").resize((95, 304)), 5, False, "弓箭"],
    "雾切之回光": [Image.open("resource/wish/weapon/雾切之回光.png").convert(mode="RGBA").resize((95, 304)), 5, False, "单手剑"],
    "无工之剑": [Image.open("resource/wish/weapon/无工之剑.png").convert(mode="RGBA").resize((95, 304)), 5, False, "双手剑"],
    "波乱月白经津": [Image.open("resource/wish/weapon/波乱月白经津.png").convert(mode="RGBA").resize((95, 304)), 5, False, "单手剑"],
    "终末嗟叹之诗": [Image.open("resource/wish/weapon/终末嗟叹之诗.png").convert(mode="RGBA").resize((95, 304)), 5, False, "弓箭"],
    # 常驻五星角色
    "刻晴": [Image.open("resource/wish/character/刻晴.png").convert(mode="RGBA").resize((120, 384)), 5, True, "雷"],
    "莫娜": [Image.open("resource/wish/character/莫娜.png").convert(mode="RGBA").resize((120, 384)), 5, True, "水"],
    "七七": [Image.open("resource/wish/character/七七.png").convert(mode="RGBA").resize((120, 384)), 5, True, "冰"],
    "迪卢克": [Image.open("resource/wish/character/迪卢克.png").convert(mode="RGBA").resize((120, 384)), 5, True, "火"],
    "琴": [Image.open("resource/wish/character/琴.png").convert(mode="RGBA").resize((120, 384)), 5, True, "风"],
    # 常驻五星武器
    "阿莫斯之弓": [Image.open("resource/wish/weapon/阿莫斯之弓.png").convert(mode="RGBA").resize((95, 304)), 5, False, "弓箭"],
    "天空之翼": [Image.open("resource/wish/weapon/天空之翼.png").convert(mode="RGBA").resize((95, 304)), 5, False, "弓箭"],
    "四风原典": [Image.open("resource/wish/weapon/四风原典.png").convert(mode="RGBA").resize((95, 304)), 5, False, "法器"],
    "天空之卷": [Image.open("resource/wish/weapon/天空之卷.png").convert(mode="RGBA").resize((95, 304)), 5, False, "法器"],
    "和璞鸢": [Image.open("resource/wish/weapon/和璞鸢.png").convert(mode="RGBA").resize((95, 304)), 5, False, "长柄"],
    "天空之脊": [Image.open("resource/wish/weapon/天空之脊.png").convert(mode="RGBA").resize((95, 304)), 5, False, "长柄"],
    "狼的末路": [Image.open("resource/wish/weapon/狼的末路.png").convert(mode="RGBA").resize((95, 304)), 5, False, "双手剑"],
    "天空之傲": [Image.open("resource/wish/weapon/天空之傲.png").convert(mode="RGBA").resize((95, 304)), 5, False, "双手剑"],
    "天空之刃": [Image.open("resource/wish/weapon/天空之刃.png").convert(mode="RGBA").resize((95, 304)), 5, False, "单手剑"],
    "风鹰剑": [Image.open("resource/wish/weapon/风鹰剑.png").convert(mode="RGBA").resize((95, 304)), 5, False, "单手剑"],
    # 常驻四星角色
    "云堇": [Image.open("resource/wish/character/云堇.png").convert(mode="RGBA").resize((120, 384)), 4, True, "岩"],
    "九条裟罗": [Image.open("resource/wish/character/九条裟罗.png").convert(mode="RGBA").resize((120, 384)), 4, True, "雷"],
    "五郎": [Image.open("resource/wish/character/五郎.png").convert(mode="RGBA").resize((120, 384)), 4, True, "岩"],
    "早柚": [Image.open("resource/wish/character/早柚.png").convert(mode="RGBA").resize((120, 384)), 4, True, "风"],
    "托马": [Image.open("resource/wish/character/托马.png").convert(mode="RGBA").resize((120, 384)), 4, True, "火"],
    "烟绯": [Image.open("resource/wish/character/烟绯.png").convert(mode="RGBA").resize((120, 384)), 4, True, "火"],
    "罗莎莉亚": [Image.open("resource/wish/character/罗莎莉亚.png").convert(mode="RGBA").resize((120, 384)), 4, True, "冰"],
    "辛焱": [Image.open("resource/wish/character/辛焱.png").convert(mode="RGBA").resize((120, 384)), 4, True, "火"],
    "砂糖": [Image.open("resource/wish/character/砂糖.png").convert(mode="RGBA").resize((120, 384)), 4, True, "风"],
    "迪奥娜": [Image.open("resource/wish/character/迪奥娜.png").convert(mode="RGBA").resize((120, 384)), 4, True, "冰"],
    "重云": [Image.open("resource/wish/character/重云.png").convert(mode="RGBA").resize((120, 384)), 4, True, "冰"],
    "诺艾尔": [Image.open("resource/wish/character/诺艾尔.png").convert(mode="RGBA").resize((120, 384)), 4, True, "岩"],
    "班尼特": [Image.open("resource/wish/character/班尼特.png").convert(mode="RGBA").resize((120, 384)), 4, True, "火"],
    "菲谢尔": [Image.open("resource/wish/character/菲谢尔.png").convert(mode="RGBA").resize((120, 384)), 4, True, "雷"],
    "凝光": [Image.open("resource/wish/character/凝光.png").convert(mode="RGBA").resize((120, 384)), 4, True, "岩"],
    "行秋": [Image.open("resource/wish/character/行秋.png").convert(mode="RGBA").resize((120, 384)), 4, True, "水"],
    "北斗": [Image.open("resource/wish/character/北斗.png").convert(mode="RGBA").resize((120, 384)), 4, True, "雷"],
    "香菱": [Image.open("resource/wish/character/香菱.png").convert(mode="RGBA").resize((120, 384)), 4, True, "火"],
    "安柏": [Image.open("resource/wish/character/安柏.png").convert(mode="RGBA").resize((120, 384)), 4, True, "火"],
    "雷泽": [Image.open("resource/wish/character/雷泽.png").convert(mode="RGBA").resize((120, 384)), 4, True, "雷"],
    "凯亚": [Image.open("resource/wish/character/凯亚.png").convert(mode="RGBA").resize((120, 384)), 4, True, "冰"],
    "芭芭拉": [Image.open("resource/wish/character/芭芭拉.png").convert(mode="RGBA").resize((120, 384)), 4, True, "水"],
    "丽莎": [Image.open("resource/wish/character/丽莎.png").convert(mode="RGBA").resize((120, 384)), 4, True, "雷"],
    # 常驻四星武器
    "弓藏": [Image.open("resource/wish/weapon/弓藏.png").convert(mode="RGBA").resize((95, 304)), 4, False, "弓箭"],
    "祭礼弓": [Image.open("resource/wish/weapon/祭礼弓.png").convert(mode="RGBA").resize((95, 304)), 4, False, "弓箭"],
    "绝弦": [Image.open("resource/wish/weapon/绝弦.png").convert(mode="RGBA").resize((95, 304)), 4, False, "弓箭"],
    "西风猎弓": [Image.open("resource/wish/weapon/西风猎弓.png").convert(mode="RGBA").resize((95, 304)), 4, False, "弓箭"],
    "昭心": [Image.open("resource/wish/weapon/昭心.png").convert(mode="RGBA").resize((95, 304)), 4, False, "法器"],
    "祭礼残章": [Image.open("resource/wish/weapon/祭礼残章.png").convert(mode="RGBA").resize((95, 304)), 4, False, "法器"],
    "流浪乐章": [Image.open("resource/wish/weapon/流浪乐章.png").convert(mode="RGBA").resize((95, 304)), 4, False, "法器"],
    "西风秘典": [Image.open("resource/wish/weapon/西风秘典.png").convert(mode="RGBA").resize((95, 304)), 4, False, "法器"],
    "西风长枪": [Image.open("resource/wish/weapon/西风长枪.png").convert(mode="RGBA").resize((95, 304)), 4, False, "长柄"],
    "匣里灭辰": [Image.open("resource/wish/weapon/匣里灭辰.png").convert(mode="RGBA").resize((95, 304)), 4, False, "长柄"],
    "雨裁": [Image.open("resource/wish/weapon/雨裁.png").convert(mode="RGBA").resize((95, 304)), 4, False, "双手剑"],
    "祭礼大剑": [Image.open("resource/wish/weapon/祭礼大剑.png").convert(mode="RGBA").resize((95, 304)), 4, False, "双手剑"],
    "钟剑": [Image.open("resource/wish/weapon/钟剑.png").convert(mode="RGBA").resize((95, 304)), 4, False, "双手剑"],
    "西风大剑": [Image.open("resource/wish/weapon/西风大剑.png").convert(mode="RGBA").resize((95, 304)), 4, False, "双手剑"],
    "匣里龙吟": [Image.open("resource/wish/weapon/匣里龙吟.png").convert(mode="RGBA").resize((95, 304)), 4, False, "单手剑"],
    "祭礼剑": [Image.open("resource/wish/weapon/祭礼剑.png").convert(mode="RGBA").resize((95, 304)), 4, False, "单手剑"],
    "笛剑": [Image.open("resource/wish/weapon/笛剑.png").convert(mode="RGBA").resize((95, 304)), 4, False, "单手剑"],
    "西风剑": [Image.open("resource/wish/weapon/西风剑.png").convert(mode="RGBA").resize((95, 304)), 4, False, "单手剑"],
    # 三星武器
    "弹弓": [Image.open("resource/wish/weapon/弹弓.png").convert(mode="RGBA").resize((95, 304)), 3, False, "弓箭"],
    "神射手之誓": [Image.open("resource/wish/weapon/神射手之誓.png").convert(mode="RGBA").resize((95, 304)), 3, False, "弓箭"],
    "鸦羽弓": [Image.open("resource/wish/weapon/鸦羽弓.png").convert(mode="RGBA").resize((95, 304)), 3, False, "弓箭"],
    "翡玉法球": [Image.open("resource/wish/weapon/翡玉法球.png").convert(mode="RGBA").resize((95, 304)), 3, False, "法器"],
    "讨龙英杰谭": [Image.open("resource/wish/weapon/讨龙英杰谭.png").convert(mode="RGBA").resize((95, 304)), 3, False, "法器"],
    "魔导绪论": [Image.open("resource/wish/weapon/魔导绪论.png").convert(mode="RGBA").resize((95, 304)), 3, False, "法器"],
    "黑缨枪": [Image.open("resource/wish/weapon/黑缨枪.png").convert(mode="RGBA").resize((95, 304)), 3, False, "长柄"],
    "以理服人": [Image.open("resource/wish/weapon/以理服人.png").convert(mode="RGBA").resize((95, 304)), 3, False, "长柄"],
    "沐浴龙血的剑": [Image.open("resource/wish/weapon/沐浴龙血的剑.png").convert(mode="RGBA").resize((95, 304)), 3, False, "单手剑"],
    "铁影阔剑": [Image.open("resource/wish/weapon/铁影阔剑.png").convert(mode="RGBA").resize((95, 304)), 3, False, "单手剑"],
    "飞天御剑": [Image.open("resource/wish/weapon/飞天御剑.png").convert(mode="RGBA").resize((95, 304)), 3, False, "单手剑"],
    "黎明神剑": [Image.open("resource/wish/weapon/黎明神剑.png").convert(mode="RGBA").resize((95, 304)), 3, False, "单手剑"],
    "冷刃": [Image.open("resource/wish/weapon/冷刃.png").convert(mode="RGBA").resize((95, 304)), 3, False, "单手剑"]
}
# 页面背景
page_background = Image.open("resource/wish/misc/background.jpg").convert(mode="RGBA")
# 物品背景
item_background = Image.open("resource/wish/misc/bg.png").convert(mode="RGBA").resize((95, 390))
item_background_2 = Image.open("resource/wish/misc/bg2.png").convert(mode="RGBA").resize((95, 390))
item_background_3 = Image.open("resource/wish/misc/bg3.png").convert(mode="RGBA").resize((95, 338))
# 物品边框
item_shadow_3 = Image.open("resource/wish/misc/shadow-3.png").convert(mode="RGBA").resize((186, 588))
item_shadow_4 = Image.open("resource/wish/misc/shadow-4.png").convert(mode="RGBA").resize((186, 588))
item_shadow_5 = Image.open("resource/wish/misc/shadow-5.png").convert(mode="RGBA").resize((186, 588))
# 角色基础蒙版
basic_character_mask = Image.open("resource/wish/character/basic_mask.png")
# 角色元素
elements = {
    "水": Image.open("resource/wish/misc/水.png").convert(mode="RGBA").resize((55, 55)),
    "火": Image.open("resource/wish/misc/火.png").convert(mode="RGBA").resize((55, 55)),
    "草": Image.open("resource/wish/misc/草.png").convert(mode="RGBA").resize((55, 55)),
    "风": Image.open("resource/wish/misc/风.png").convert(mode="RGBA").resize((55, 55)),
    "雷": Image.open("resource/wish/misc/雷.png").convert(mode="RGBA").resize((55, 55)),
    "冰": Image.open("resource/wish/misc/冰.png").convert(mode="RGBA").resize((55, 55)),
    "岩": Image.open("resource/wish/misc/岩.png").convert(mode="RGBA").resize((55, 55))
}
# 武器类型
weapon_type = {
    "单手剑": Image.open("resource/wish/misc/单手剑.png").convert(mode="RGBA"),
    "双手剑": Image.open("resource/wish/misc/双手剑.png").convert(mode="RGBA"),
    "长柄": Image.open("resource/wish/misc/长柄.png").convert(mode="RGBA"),
    "弓箭": Image.open("resource/wish/misc/弓箭.png").convert(mode="RGBA"),
    "法器": Image.open("resource/wish/misc/法器.png").convert(mode="RGBA")
}
# 星级
grade = {
    3: Image.open("resource/wish/misc/s-3.png").convert(mode="RGBA").resize((75, 20)),
    4: Image.open("resource/wish/misc/s-4.png").convert(mode="RGBA").resize((75, 20)),
    5: Image.open("resource/wish/misc/s-5.png").convert(mode="RGBA").resize((75, 20))
}


# 图片生成
async def gen_pic(wish_typ: int, result_list: list, ep_info: list = None) -> str:
    # 函数启动时间
    start_time = datetime.datetime.now()
    # 获取背景
    result_pic = page_background.copy()
    # 将十个结果依次嵌入页面背景
    for i in range(0, 10):
        res = result_list[i][0]
        # 嵌入物品边框
        if item_dict[res][1] == 3:
            result_pic.paste(item_shadow_3, (6 + 95 * i, -20), item_shadow_3)
        elif item_dict[res][1] == 4:
            result_pic.paste(item_shadow_4, (6 + 95 * i, -20), item_shadow_4)
        elif item_dict[res][1] == 5:
            result_pic.paste(item_shadow_5, (6 + 95 * i, -20), item_shadow_5)
    for i in range(0, 10):
        res = result_list[i][0]
        # 嵌入物品背景
        result_pic.paste(item_background, (53 + 95 * i, 100), item_background)
        result_pic.paste(item_background_2, (53 + 95 * i, 100), item_background_2)
        if item_dict[res][1] == 5:
            result_pic.paste(item_background_3, (53 + 95 * i, 128), item_background_3)
        # 嵌入物品图片
        if item_dict[res][2]:
            # 获取角色图片
            item = item_dict[res][0]
            # 读入基础蒙版
            mask = basic_character_mask.copy()
            # 基础蒙版与角色立绘透明度合成
            mask = Image.composite(mask, Image.new("L", item.size, "black"), item.split()[-1].convert("L"))
            # 嵌入角色立绘
            result_pic.paste(item, (41 + 95 * i, 92), mask)
            # 嵌入角色元素
            element = elements[item_dict[res][3]]
            result_pic.paste(element, (74 + 95 * i, 375), element)
            # 嵌入角色星级
            star = grade[item_dict[res][1]]
            result_pic.paste(star, (64 + 95 * i, 438), star)
        else:
            # 获取武器图片
            item = item_dict[res][0]
            # 嵌入武器阴影
            result_pic.paste(Image.new("RGBA", item.size, (47, 51, 50)), (58 + 95 * i, 150), item)
            # 嵌入武器立绘
            result_pic.paste(item, (52 + 95 * i, 145), item)
            # 嵌入武器类型
            typ = weapon_type[item_dict[res][3]]
            result_pic.paste(typ, (69 + 95 * i, 368), typ)
            # 嵌入武器星级
            star = grade[item_dict[res][1]]
            result_pic.paste(star, (64 + 95 * i, 438), star)
    # 字体
    font = ImageFont.truetype("resource/wish/font/zh-cn.ttf", 20)
    # 新建文字图层
    text_overlay = Image.new('RGBA', result_pic.size, (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_overlay)
    # 添加顶栏文字
    if wish_typ == 1:
        text_draw.text((10, 10), f"{start_time.strftime('%Y/%m/%d %H:%M:%S')} 角色活动祈愿", font=font)
    elif wish_typ == 2:
        text_draw.text((10, 10), f"{start_time.strftime('%Y/%m/%d %H:%M:%S')} 角色活动祈愿-2", font=font)
    elif wish_typ == 3:
        text_draw.text((10, 10), f"{start_time.strftime('%Y/%m/%d %H:%M:%S')} 武器活动祈愿  "
                                 f"定轨: {ep_info[0]}  命定值: {ep_info[1]} ", font=font)
    else:
        text_draw.text((10, 10), f"{start_time.strftime('%Y/%m/%d %H:%M:%S')} 常驻祈愿", font=font)
    # 添加底栏文字
    count_text = ""
    for i in range(0, 10):
        # 如果是三星就停止
        if item_dict[result_list[i][0]][1] == 3:
            break
        # 添加抽数
        count_text += f"{result_list[i][0]}[{result_list[i][1]}] "
    text_draw.text((10, 568), count_text, font=font)
    # 添加KrLiSrAu水印
    text_draw.text((565, 568), "https://github.com/ChrisKimZHT/KrLiSrAu-Bot", font=font)
    # 合成文字图层
    result_pic = Image.alpha_composite(result_pic, text_overlay)
    # 创建二进制数据
    buffer = BytesIO()
    # 储存图片
    result_pic.save(buffer, format="PNG")
    buffer_byte = buffer.getvalue()
    # base64编码
    base64_pic = base64.b64encode(buffer_byte).decode("ascii")
    return base64_pic
