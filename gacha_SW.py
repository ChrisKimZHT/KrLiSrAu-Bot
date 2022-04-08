from random import randint


# 五星权重函数 W(x) >可修改<
def weight_five(x):
    if x <= 73:
        return 60
    elif x >= 74:
        return 60 + 600 * (x - 73)


# 四星权重函数 W(x) >可修改<
def weight_four(x):
    if x <= 8:
        return 510
    elif x >= 9:
        return 510 + 5100 * (x - 8)


# 四星平稳机制权重函数 W(x) >可修改<
def weight_stabilizer_four_star(x):
    if x <= 17:
        return 255
    elif x >= 18:
        return 255 + 2550 * (x - 17)


# 五星平稳机制权重函数 W(x) >可修改<
def weight_stabilizer_five_star(x):
    if x <= 147:
        return 30
    elif x >= 148:
        return 30 + 300 * (x - 147)


four_star_counter = 1
five_star_counter = 1


# 星级选择器
def star_selector():
    global five_star_counter
    global four_star_counter
    five = weight_five(five_star_counter)
    four = weight_four(four_star_counter)
    three = 9430  # 三星权重 >可修改<
    ceil = 10000  # 权重限制 >可修改<
    wsum = five + four + three  # 权重和
    random_num = randint(1, min(wsum, ceil))  # 随机数生成
    if 1 <= random_num <= five:
        temp = [5, four_star_counter, five_star_counter]
        four_star_counter += 1
        five_star_counter = 1
        return temp
    elif five + 1 <= random_num <= five + four:
        temp = [4, four_star_counter, five_star_counter]
        four_star_counter = 1
        five_star_counter += 1
        return temp
    elif five + four + 1 <= random_num <= five + four + three:
        temp = [3, four_star_counter, five_star_counter]
        four_star_counter += 1
        five_star_counter += 1
        return temp


last_four_star_character = 1
last_four_star_weapon = 1
last_five_star_character = 1
last_five_star_weapon = 1


# 四星类别选择器 True-角色 False-武器
def four_star_type_selector():
    global last_four_star_character
    global last_four_star_weapon
    character = weight_stabilizer_four_star(last_four_star_character)
    weapon = weight_stabilizer_four_star(last_four_star_weapon)
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


# 五星类别选择器 True-角色 False-武器
def five_star_type_selector():
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


# 结果字典
five_star_character = \
    ["刻晴", "莫娜", "七七", "迪卢克", "琴"]
five_star_weapon = \
    ["阿莫斯之弓", "天空之翼", "四风原典", "天空之卷", "和璞鸢",
     "天空之脊", "狼的末路", "天空之傲", "天空之刃", "风鹰剑"]
four_star_character = \
    ["云堇", "九条裟罗", "五郎", "早柚", "托马",
     "烟绯", "罗莎莉亚", "辛焱", "砂糖", "迪奥娜",
     "重云", "诺艾尔", "班尼特", "菲谢尔", "凝光",
     "行秋", "北斗", "香菱", "安柏", "雷泽",
     "凯亚", "芭芭拉", "丽莎"]
four_star_weapon = \
    ["弓藏", "祭礼弓", "绝弦", "西风猎弓",
     "昭心", "祭礼残章", "流浪乐章", "西风秘典",
     "西风长枪", "匣里灭辰", "雨裁", "祭礼大剑",
     "钟剑", "西风大剑", "匣里龙吟", "祭礼剑",
     "笛剑", "西风剑"]
three_star = \
    ["弹弓", "神射手之誓", "鸦羽弓", "翡玉法球",
     "讨龙英杰谭", "魔导绪论", "黑缨枪", "以理服人",
     "沐浴龙血的剑", "铁影阔剑", "飞天御剑", "黎明神剑",
     "冷刃"]


# 结果选择器
def result_selector(star, typ):
    global last_four_star_weapon
    global last_four_star_character
    global last_five_star_weapon
    global last_five_star_character
    if star == 3:
        last_four_star_weapon += 1
        last_four_star_character += 1
        last_five_star_weapon += 1
        last_five_star_character += 1
        return three_star[randint(0, len(three_star) - 1)]
    elif star == 4:
        if typ:
            last_four_star_weapon += 1
            last_four_star_character = 1
            return four_star_character[randint(0, len(four_star_character) - 1)]
        else:
            last_four_star_weapon = 1
            last_four_star_character += 1
            return four_star_weapon[randint(0, len(four_star_weapon) - 1)]
    elif star == 5:
        if typ:
            last_five_star_weapon += 1
            last_five_star_character = 1
            return five_star_character[randint(0, len(five_star_character) - 1)]
        else:
            last_five_star_weapon = 1
            last_five_star_character += 1
            return five_star_weapon[randint(0, len(five_star_weapon) - 1)]


def sw():
    string = ""
    temp = star_selector()  # 星数选择器返回列表
    star = temp[0]  # 星数
    four_star_order = temp[1]  # 4星所在序号
    five_star_order = temp[2]  # 5星所在序号
    typ = None
    if star == 4:
        typ = four_star_type_selector()  # 是否为武器
    elif star == 5:
        typ = five_star_type_selector()
    result = result_selector(star, typ)
    # 结果字符串拼接
    if star == 3:
        string += "★★★☆☆ "
    elif star == 4:
        string += "★★★★☆ "
    elif star == 5:
        string += "★★★★★ "
    string += result
    if star == 4:
        string += f" #{four_star_order}"
    elif star == 5:
        string += f" #{five_star_order}"
    return string
