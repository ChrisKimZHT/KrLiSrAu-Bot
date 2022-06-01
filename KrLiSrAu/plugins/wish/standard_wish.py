from random import randint

# 结果字典
five_star_character = \
    ["刻晴", "莫娜", "七七", "迪卢克", "琴"]
len_five_star_character = len(five_star_character)
five_star_weapon = \
    ["阿莫斯之弓", "天空之翼", "四风原典", "天空之卷", "和璞鸢", "天空之脊", "狼的末路", "天空之傲", "天空之刃", "风鹰剑"]
len_five_star_weapon = len(five_star_weapon)
four_star_character = \
    ["云堇", "九条裟罗", "五郎", "早柚", "托马", "烟绯", "罗莎莉亚", "辛焱", "砂糖", "迪奥娜",
     "重云", "诺艾尔", "班尼特", "菲谢尔", "凝光", "行秋", "北斗", "香菱", "安柏", "雷泽",
     "凯亚", "芭芭拉", "丽莎"]
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
last_four_star_character = 1
last_four_star_weapon = 1
last_five_star_character = 1
last_five_star_weapon = 1


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


# 四星平稳机制权重函数 W(x) >可修改<
def weight_stabilizer_four_star(x: int) -> int:
    if x <= 17:
        return 255
    elif x >= 18:
        return 255 + 2550 * (x - 17)


# 五星平稳机制权重函数 W(x) >可修改<
def weight_stabilizer_five_star(x: int) -> int:
    if x <= 147:
        return 30
    elif x >= 148:
        return 30 + 300 * (x - 147)


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


# 四星类别选择器 True-角色 False-武器
async def four_star_type_selector() -> bool:
    global last_four_star_character
    global last_four_star_weapon
    character = weight_stabilizer_four_star(last_four_star_character)
    weapon = weight_stabilizer_four_star(last_four_star_weapon)
    ceil = 10000  # 权重限制 >可修改<
    wsum = character + weapon  # 权重和
    rnd = randint(1, min(wsum, ceil))  # 随机数生成
    if character == weapon:
        if 1 <= rnd <= character:
            return True
        elif character + 1 <= rnd <= character + weapon:
            return False
    elif character > weapon:
        if 1 <= rnd <= character:
            return True
        elif character + 1 <= rnd <= character + weapon:
            return False
    elif weapon > character:
        if 1 <= rnd <= weapon:
            return False
        elif weapon + 1 <= rnd <= weapon + character:
            return True


# 五星类别选择器 True-角色 False-武器
async def five_star_type_selector() -> bool:
    global last_five_star_character
    global last_five_star_weapon
    character = weight_stabilizer_five_star(last_five_star_character)
    weapon = weight_stabilizer_five_star(last_five_star_weapon)
    ceil = 10000  # 权重限制 >可修改<
    wsum = character + weapon  # 权重和
    random_num = randint(1, min(wsum, ceil))  # 随机数生成
    if character == weapon:
        if 1 <= random_num <= character:
            return True
        elif character + 1 <= random_num <= character + weapon:
            return False
    elif character > weapon:
        if 1 <= random_num <= character:
            return True
        elif character + 1 <= random_num <= character + weapon:
            return False
    elif weapon > character:
        if 1 <= random_num <= weapon:
            return False
        elif weapon + 1 <= random_num <= weapon + character:
            return True


# 结果选择器
async def result_selector(star: int, typ: bool) -> str:
    global last_four_star_weapon
    global last_four_star_character
    global last_five_star_weapon
    global last_five_star_character
    if star == 3:
        last_four_star_weapon += 1
        last_four_star_character += 1
        last_five_star_weapon += 1
        last_five_star_character += 1
        return three_star[randint(0, len_three_star - 1)]
    elif star == 4:
        if typ:
            last_four_star_weapon += 1
            last_four_star_character = 1
            return four_star_character[randint(0, len_four_star_character - 1)]
        else:
            last_four_star_weapon = 1
            last_four_star_character += 1
            return four_star_weapon[randint(0, len_four_star_weapon - 1)]
    elif star == 5:
        if typ:
            last_five_star_weapon += 1
            last_five_star_character = 1
            return five_star_character[randint(0, len_five_star_character - 1)]
        else:
            last_five_star_weapon = 1
            last_five_star_character += 1
            return five_star_weapon[randint(0, len_five_star_weapon - 1)]


async def sw() -> list:
    five_star_character_list = []  # 五星角色列表
    five_star_weapon_list = []  # 五星武器列表
    four_star_character_list = []  # 四型角色列表
    four_star_weapon_list = []  # 四星武器列表
    three_star_list = []  # 三星武器列表
    for i in range(0, 10):
        star_with_cnt = await star_selector()  # 星数选择器返回列表
        star = star_with_cnt[0]  # 星数
        cnt = star_with_cnt[1]  # 抽数
        is_character = True
        if star == 4:
            is_character = await four_star_type_selector()  # 是否为角色
        elif star == 5:
            is_character = await five_star_type_selector()  # 是否为角色
        result = (await result_selector(star, is_character), cnt)  # 获取具体结果
        # 结果保存
        if star == 3:
            three_star_list.append(result)
        elif star == 4 and is_character:
            four_star_character_list.append(result)
        elif star == 4:
            four_star_weapon_list.append(result)
        elif star == 5 and is_character:
            five_star_character_list.append(result)
        elif star == 5:
            five_star_weapon_list.append(result)
    # 返回结果 高星级角色＞高星级武器＞低星级角色＞低星级武器＞实际抽取顺序
    return five_star_character_list + five_star_weapon_list + four_star_character_list + four_star_weapon_list + three_star_list