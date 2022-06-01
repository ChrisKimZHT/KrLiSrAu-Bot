from random import randint

# 结果字典
five_star_up = \
    ["夜兰", "魈"]
len_five_star_up = len(five_star_up)
five_star_standard = \
    ["刻晴", "莫娜", "七七", "迪卢克", "琴"]
len_five_star_standard = len(five_star_standard)
four_star_up = \
    ["烟绯", "诺艾尔", "芭芭拉"]
len_four_star_up = len(four_star_up)
four_star_character = \
    ["云堇", "九条裟罗", "五郎", "早柚", "托马", "罗莎莉亚", "辛焱", "砂糖", "迪奥娜", "重云",
     "班尼特", "菲谢尔", "凝光", "行秋", "北斗", "香菱", "雷泽"]
len_four_star_character = len(four_star_character)
four_star_weapon = \
    ["弓藏", "祭礼弓", "绝弦", "西风猎弓", "昭心", "祭礼残章", "流浪乐章", "西风秘典", "西风长枪", "匣里灭辰",
     "雨裁", "祭礼大剑", "钟剑", "西风大剑", "匣里龙吟", "祭礼剑", "笛剑", "西风剑"]
len_four_star_weapon = len(four_star_weapon)
three_star = \
    ["弹弓", "神射手之誓", "鸦羽弓", "翡玉法球", "讨龙英杰谭", "魔导绪论", "黑缨枪", "以理服人", "沐浴龙血的剑", "铁影阔剑",
     "飞天御剑", "黎明神剑", "冷刃"]
len_three_star = len(three_star)

# 全局变量
four_star_counter = 1
five_star_counter = 1
last_four_up = True
last_five_up = True


# 五星权重函数 W(x) >可修改<
def weight_five(x: int) -> int:
    if x <= 73:
        return 60
    elif x >= 74:
        return 60 + 600 * (x - 73)


# 四星权重函数 W(x) >可修改<
def weight_four(x: int) -> int:
    if x <= 8:
        return 510
    elif x >= 9:
        return 510 + 5100 * (x - 8)


# 星级选择器
async def star_selector() -> tuple:
    global five_star_counter
    global four_star_counter
    five = weight_five(five_star_counter)
    four = weight_four(four_star_counter)
    three = 9430  # 三星权重 >可修改<
    ceil = 10000  # 权重限制 >可修改<
    wsum = five + four + three  # 权重和
    random_num = randint(1, min(wsum, ceil))  # 随机数生成
    if 1 <= random_num <= five:
        result = (5, five_star_counter)
        four_star_counter += 1
        five_star_counter = 1
        return result
    elif five + 1 <= random_num <= five + four:
        result = (4, four_star_counter)
        four_star_counter = 1
        five_star_counter += 1
        return result
    elif five + four + 1 <= random_num <= five + four + three:
        result = (3, -1)
        four_star_counter += 1
        five_star_counter += 1
        return result


# UP选择器
async def up_selector(star: int) -> bool:
    global last_four_up
    global last_five_up
    if star == 4:
        if last_four_up:
            random_num = randint(1, 100)
            if 1 <= random_num <= 50:  # UP概率 >可修改<
                last_four_up = True
                return True  # 四星UP
            else:
                last_four_up = False
                return False  # 四星歪
        else:
            last_four_up = True
            return True  # 四星保底UP
    elif star == 5:
        if last_five_up:
            random_num = randint(1, 100)
            if 1 <= random_num <= 50:  # UP概率 >可修改<
                last_five_up = True
                return True  # 五星UP
            else:
                last_five_up = False
                return False  # 五星歪
        else:
            last_five_up = True
            return True  # 五星保底UP


# 四星类别选择器 True-角色 False-武器
async def four_star_type_selector() -> bool:
    if 0 <= randint(0, len_four_star_character + len_four_star_weapon - 1) <= len_four_star_character - 1:
        return True
    else:
        return False


# 结果选择器
async def result_selector(star: int, up: bool, gacha_typ: int, typ: bool) -> str:
    if star == 3:
        return three_star[randint(0, len_three_star - 1)]
    elif star == 4:
        if up:
            return four_star_up[randint(0, len_four_star_up - 1)]
        else:
            if typ:
                return four_star_character[randint(0, len_four_star_character - 1)]
            else:
                return four_star_weapon[randint(0, len_four_star_weapon - 1)]
    elif star == 5:
        if up:
            return five_star_up[gacha_typ]
        else:
            return five_star_standard[randint(0, len_five_star_standard - 1)]


async def cew(gacha_typ: bool) -> list:
    five_star_list = []  # 五星角色列表
    four_star_character_list = []  # 四型角色列表
    four_star_weapon_list = []  # 四星武器列表
    three_star_list = []  # 三星武器列表
    for i in range(0, 10):
        star_with_cnt = await star_selector()  # 星数选择器返回列表
        star = star_with_cnt[0]  # 星数
        cnt = star_with_cnt[1]  # 抽数
        is_up = await up_selector(star)  # 是否UP
        is_character = True
        if star == 4 and not is_up:
            is_character = await four_star_type_selector()  # 是否为角色
        result = (await result_selector(star, is_up, gacha_typ, is_character), cnt)  # 获取具体结果
        # 结果保存
        if star == 3:
            three_star_list.append(result)
        elif star == 4 and (is_up or is_character):
            four_star_character_list.append(result)
        elif star == 4:
            four_star_weapon_list.append(result)
        elif star == 5:
            five_star_list.append(result)
    # 返回结果 高星级角色＞高星级武器＞低星级角色＞低星级武器＞实际抽取顺序
    return five_star_list + four_star_character_list + four_star_weapon_list + three_star_list
